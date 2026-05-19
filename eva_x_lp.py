import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import argparse
import json
import logging
import sys
from pathlib import Path
from torch.utils.data import DataLoader

import torch
import torch.nn as nn
from monai.utils import set_determinism
from torch.utils.tensorboard import SummaryWriter
from heatmap_assisted_diagnosis.utils.custom_scheduler import CosineAnnealingWarmupRestarts
from heatmap_assisted_diagnosis.utils.focal_loss import FocalLoss
from sklearn.metrics import f1_score, hamming_loss, roc_auc_score, average_precision_score

from heatmap_assisted_diagnosis.eva_x.eva_x import eva_x_base_patch16
from heatmap_assisted_diagnosis.dataset import ChestXrayDataset
import numpy as np


class LinearProbe(nn.Module):
    """Frozen backbone + single linear classification head."""
    def __init__(self, backbone, logit_dim, num_classes):
        super().__init__()
        self.backbone = backbone

        for param in self.backbone.parameters():
            param.requires_grad = False

        self.head = nn.Linear(logit_dim, num_classes)

    def forward(self, x):
        with torch.no_grad():
            features = self.backbone(x)  # [B, logit_dim]
        return self.head(features)           # [B, num_classes] — classes


def main():
    parser = argparse.ArgumentParser(description="Linear Probe Training (Multi-Label)")
    parser.add_argument(
        "-c",
        "--config-file",
        default="/storage/homefs/ed22q093/heatmap_assisted_diagnosis/configs/eva.json",
    )
    args = parser.parse_args()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    torch.cuda.set_device(device)
    print(f"Using {device}")

    torch.backends.cudnn.benchmark = True
    torch.set_num_threads(4)

    config_dict = json.load(open(args.config_file, "r"))
    for k, v in config_dict.items():
        setattr(args, k, v)

    set_determinism(42)

    # Step 1: Data loaders
    # NOTE: Your ChestXrayDataset labels must now return float tensors of
    # shape [num_classes] with 0/1 values, e.g. tensor([1., 0., 1.])
    train_set = ChestXrayDataset(args.train['csv_path'], args.train['image_folder'], transform=args.train['mode'])
    val_set   = ChestXrayDataset(args.val['csv_path'],   args.val['image_folder'],   transform=args.val['mode'])

    train_loader = DataLoader(train_set, batch_size=args.train['batch_size'], shuffle=True,
                              num_workers=args.train['num_workers'], pin_memory=True)
    val_loader   = DataLoader(val_set,   batch_size=args.val['batch_size'],   shuffle=False,
                              num_workers=args.val['num_workers'], pin_memory=True)

    # Step 2: Model
    backbone = eva_x_base_patch16(
        pretrained="/storage/homefs/ed22q093/heatmap_assisted_diagnosis/models/eva_x_base_patch16_merged520k_mim.pt"
    )
    model = LinearProbe(backbone, logit_dim=768, num_classes=args.num_classes).to(device)

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total     = sum(p.numel() for p in model.parameters())
    print(f"Trainable params: {trainable:,} / {total:,}")

    # Step 3: Loss — BCE instead of CrossEntropy for multi-label
    # loss_fn     = nn.BCEWithLogitsLoss()  # expects float labels [B, num_classes]
    loss_fn     = FocalLoss(alpha=0.25, gamma=2.0)
    val_loss_fn = nn.BCEWithLogitsLoss()

    # Step 4: Optimizer — head only
    optimizer = torch.optim.AdamW(
        params=model.head.parameters(),
        lr=args.train["learning_rate"],
        weight_decay=args.train["weight_decay"]
    )

    n_epochs      = args.train["num_epochs"]
    val_interval  = args.check_val_every_n_epoch
    total_step    = 0
    best_f1       = 0
    best_auroc = 0.0

    total_iters = len(train_loader) * n_epochs
    lr_scheduler = CosineAnnealingWarmupRestarts(
        optimizer,
        first_cycle_steps=total_iters,
        cycle_mult=1.0,
        max_lr=args.train["learning_rate"],
        min_lr=0.0,
        warmup_steps=int(total_iters * 0.05),
        gamma=1.0
    )

    logs_path         = args.logs_path
    model_name        = args.model_name
    trained_best_path = os.path.join(logs_path, model_name + '_best.pth')
    trained_last_path = os.path.join(logs_path, model_name + '_last.pth')

    Path(logs_path).mkdir(parents=True, exist_ok=True)
    tensorboard_writer = SummaryWriter(logs_path)

    # Step 5: Training loop
    for epoch in range(n_epochs):
        print(f"Epoch {epoch}")
        model.train()
        model.backbone.eval()

        for step, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.float().to(device)  # [B, num_classes] float for BCE

            optimizer.zero_grad(set_to_none=True)
            preds = model(images)   
            l = loss_fn(preds, labels)
            l.backward()
            optimizer.step()
            lr_scheduler.step()

            total_step += 1
            tensorboard_writer.add_scalar("train_loss_iter", l, total_step)

        # Validation
        if epoch % val_interval == 0:
            model.eval()
            val_epoch_loss = 0.0
            all_preds, all_probs, all_labels = [], [], []

            for step, (images, labels) in enumerate(val_loader):
                images = images.to(device)
                labels = labels.float().to(device)

                with torch.no_grad():
                    logits = model(images)
                    l = val_loss_fn(logits, labels)
                    val_epoch_loss += l.item()

                    probs = torch.sigmoid(logits).cpu().numpy()
                    preds_binary = (probs > 0.5)

                    all_probs.extend(probs)
                    all_preds.extend(preds_binary)
                    all_labels.extend(labels.cpu().numpy())

            val_epoch_loss = val_epoch_loss / (step + 1)

            all_labels = np.array(all_labels)  # [N, num_classes]
            all_probs  = np.array(all_probs)   # [N, num_classes]
            all_preds  = np.array(all_preds)   # [N, num_classes]

            f1           = f1_score(all_labels, all_preds, average='macro', zero_division=0)
            f1_per_class = f1_score(all_labels, all_preds, average=None,    zero_division=0)
            hamming      = hamming_loss(all_labels, all_preds)

            # AUROC and AUPRC per class
            num_classes = all_labels.shape[1]
            auroc_per_class = []
            auprc_per_class = []

            for c in range(num_classes):
                # Skip classes with no positive samples in validation set
                if all_labels[:, c].sum() == 0:
                    print(f"Warning: class {c} has no positive samples, skipping AUROC/AUPRC")
                    auroc_per_class.append(float('nan'))
                    auprc_per_class.append(float('nan'))
                else:
                    auroc_per_class.append(roc_auc_score(all_labels[:, c], all_probs[:, c]))
                    auprc_per_class.append(average_precision_score(all_labels[:, c], all_probs[:, c]))

            # Macro average ignoring nan (classes with no positive samples)
            mean_auroc = np.nanmean(auroc_per_class)
            mean_auprc = np.nanmean(auprc_per_class)

            print(f"val_loss: {val_epoch_loss:.4f} | macro F1: {f1:.4f} | hamming: {hamming:.4f} | AUROC: {mean_auroc:.4f} | AUPRC: {mean_auprc:.4f}")
            print(f"per-class AUROC: {np.round(auroc_per_class, 4)}")
            print(f"per-class AUPRC: {np.round(auprc_per_class, 4)}")
            print(f"per-class F1:    {np.round(f1_per_class, 4)}")

            tensorboard_writer.add_scalar("val_loss",    val_epoch_loss, epoch)
            tensorboard_writer.add_scalar("f1_macro",    f1,             epoch)
            tensorboard_writer.add_scalar("auroc_macro", mean_auroc,     epoch)
            tensorboard_writer.add_scalar("auprc_macro", mean_auprc,     epoch)
            tensorboard_writer.add_scalar("hamming_loss", hamming,       epoch)

            for i, (f, auroc, auprc) in enumerate(zip(f1_per_class, auroc_per_class, auprc_per_class)):
                tensorboard_writer.add_scalar(f"f1_class_{i}",    f,     epoch)
                tensorboard_writer.add_scalar(f"auroc_class_{i}", auroc, epoch)
                tensorboard_writer.add_scalar(f"auprc_class_{i}", auprc, epoch)

            torch.save(model.head.state_dict(), trained_last_path)

            if mean_auroc > best_auroc:
                best_auroc = mean_auroc
                torch.save(model.head.state_dict(), trained_best_path)
                print(f"New best AUROC: {best_auroc:.4f} — saved to {trained_best_path}")


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="[%(asctime)s.%(msecs)03d][%(levelname)5s](%(name)s) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()