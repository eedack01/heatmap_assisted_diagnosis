import os
import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from monai.utils import set_determinism
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from sklearn.metrics import f1_score, hamming_loss, roc_auc_score, average_precision_score

from utils.custom_scheduler import CosineAnnealingWarmupRestarts
from utils.focal_loss import FocalLoss
from utils.model_selection import build_model


def get_loaders(args):
    # Detect dataset from explicit config key or fall back to num_classes
    dataset = getattr(args, "dataset", "chestdr" if args.num_classes == 19 else "vindr")

    if dataset == "chestdr":
        from dataset_chestdr import ChestXrayDataset
        train_set = ChestXrayDataset(
            args.train["csv_path"], args.train["image_folder"],
            transform="train", img_size=args.image_size, img_crop=args.image_crop,
            split="train"
        )
        val_set = ChestXrayDataset(
            args.val["csv_path"], args.val["image_folder"],
            transform="val", img_size=args.image_size, img_crop=args.image_crop,
            split="val"
        )
    else:
        from dataset import ChestXrayDataset
        train_set = ChestXrayDataset(
            args.train["csv_path"], args.train["image_folder"],
            transform=args.train["mode"], img_size=args.image_size, img_crop=args.image_crop
        )
        val_set = ChestXrayDataset(
            args.val["csv_path"], args.val["image_folder"],
            transform=args.val["mode"], img_size=args.image_size, img_crop=args.image_crop
        )

    train_loader = DataLoader(
        train_set, batch_size=args.train["batch_size"], shuffle=True,
        num_workers=args.train["num_workers"], pin_memory=True
    )
    val_loader = DataLoader(
        val_set, batch_size=args.val["batch_size"], shuffle=False,
        num_workers=args.val["num_workers"], pin_memory=True
    )
    return train_loader, val_loader


def forward(model, images, model_name):
    if model_name == "raddino":
        outputs = model(pixel_values=images)
        features = outputs.last_hidden_state[:, 0, :]
        return model.head(features)
    elif model_name == "chexzero":
        features = model(images)
        return model.head(features)
    elif model_name == "from_scratch":
        logits, _ = model(images)
        return logits
    else:
        return model(images)


def compute_metrics(all_labels, all_preds, all_probs):
    f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    f1_per_class = f1_score(all_labels, all_preds, average=None, zero_division=0)
    hamming = hamming_loss(all_labels, all_preds)

    auroc_per_class, auprc_per_class = [], []
    for c in range(all_labels.shape[1]):
        if all_labels[:, c].sum() == 0:
            print(f"  Warning: class {c} has no positive samples, skipping AUROC/AUPRC")
            auroc_per_class.append(float("nan"))
            auprc_per_class.append(float("nan"))
        else:
            auroc_per_class.append(roc_auc_score(all_labels[:, c], all_probs[:, c]))
            auprc_per_class.append(average_precision_score(all_labels[:, c], all_probs[:, c]))

    return f1, f1_per_class, hamming, auroc_per_class, auprc_per_class


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", required=True)
    args = parser.parse_args()

    config = json.load(open(args.config_file))
    for k, v in config.items():
        setattr(args, k, v)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    torch.cuda.set_device(device)
    torch.backends.cudnn.benchmark = True
    torch.set_num_threads(4)
    set_determinism(42)
    print(f"Using {device}")

    train_loader, val_loader = get_loaders(args)

    model = build_model(args.model_name, num_classes=args.num_classes, device=device)

    freeze_backbone = getattr(args, "freeze_backbone", False)
    if freeze_backbone:
        for name, param in model.named_parameters():
            if "head" not in name:
                param.requires_grad = False
        optimizer_params = [p for p in model.parameters() if p.requires_grad]
    else:
        optimizer_params = list(model.parameters())

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"Trainable params: {trainable:,} / {total:,}")

    loss_fn = FocalLoss(alpha=0.25, gamma=2.0)
    val_loss_fn = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.AdamW(
        optimizer_params,
        lr=args.train["learning_rate"],
        weight_decay=args.train["weight_decay"]
    )

    n_epochs = args.train["num_epochs"]
    val_interval = args.check_val_every_n_epoch
    total_iters = len(train_loader) * n_epochs

    lr_scheduler = CosineAnnealingWarmupRestarts(
        optimizer,
        first_cycle_steps=total_iters,
        cycle_mult=1.0,
        max_lr=args.train["learning_rate"],
        min_lr=0.0,
        warmup_steps=int(total_iters * 0.1),
        gamma=1.0
    )

    logs_path = args.logs_path
    Path(logs_path).mkdir(parents=True, exist_ok=True)
    writer = SummaryWriter(logs_path)

    best_path = os.path.join(logs_path, f"{args.model_name}_best.pth")
    last_path = os.path.join(logs_path, f"{args.model_name}_last.pth")

    best_auroc = 0.0
    total_step = 0

    for epoch in range(n_epochs):
        print(f"Epoch {epoch}")
        model.train()
        if freeze_backbone:
            for name, module in model.named_modules():
                if "head" not in name:
                    module.eval()

        for step, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.float().to(device)

            optimizer.zero_grad(set_to_none=True)
            logits = forward(model, images, args.model_name)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()
            lr_scheduler.step()

            total_step += 1
            writer.add_scalar("train_loss_iter", loss, total_step)

        if epoch % val_interval != 0:
            continue

        model.eval()
        val_loss = 0.0
        all_preds, all_probs, all_labels = [], [], []

        for step, (images, labels) in enumerate(val_loader):
            images = images.to(device)
            labels = labels.float().to(device)

            with torch.no_grad():
                logits = forward(model, images, args.model_name)
                val_loss += val_loss_fn(logits, labels).item()

            probs = torch.sigmoid(logits).cpu().numpy()
            all_probs.extend(probs)
            all_preds.extend(probs > 0.5)
            all_labels.extend(labels.cpu().numpy())

        val_loss /= step + 1
        all_labels = np.array(all_labels)
        all_probs = np.array(all_probs)
        all_preds = np.array(all_preds)

        f1, f1_per_class, hamming, auroc_per_class, auprc_per_class = compute_metrics(
            all_labels, all_preds, all_probs
        )
        mean_auroc = np.nanmean(auroc_per_class)
        mean_auprc = np.nanmean(auprc_per_class)

        print(f"val_loss: {val_loss:.4f} | macro F1: {f1:.4f} | hamming: {hamming:.4f} | AUROC: {mean_auroc:.4f} | AUPRC: {mean_auprc:.4f}")
        print(f"per-class AUROC: {np.round(auroc_per_class, 4)}")
        print(f"per-class AUPRC: {np.round(auprc_per_class, 4)}")
        print(f"per-class F1:    {np.round(f1_per_class, 4)}")

        writer.add_scalar("val_loss", val_loss, epoch)
        writer.add_scalar("f1_macro", f1, epoch)
        writer.add_scalar("auroc_macro", mean_auroc, epoch)
        writer.add_scalar("auprc_macro", mean_auprc, epoch)
        writer.add_scalar("hamming_loss", hamming, epoch)
        for i, (f, auroc, auprc) in enumerate(zip(f1_per_class, auroc_per_class, auprc_per_class)):
            writer.add_scalar(f"f1_class_{i}", f, epoch)
            writer.add_scalar(f"auroc_class_{i}", auroc, epoch)
            writer.add_scalar(f"auprc_class_{i}", auprc, epoch)

        torch.save(model.state_dict(), last_path)

        if mean_auroc > best_auroc:
            best_auroc = mean_auroc
            torch.save(model.state_dict(), best_path)
            print(f"New best AUROC: {best_auroc:.4f} — saved to {best_path}")


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="[%(asctime)s.%(msecs)03d][%(levelname)5s](%(name)s) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()
