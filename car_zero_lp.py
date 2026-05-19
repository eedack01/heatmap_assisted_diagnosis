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
from sklearn.metrics import f1_score, balanced_accuracy_score

from heatmap_assisted_diagnosis.CARZero.CARZero.CARZero import load_CARZero
from heatmap_assisted_diagnosis.dataset import ChestXrayDataset


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
    backbone = load_CARZero(name="/storage/homefs/ed22q093/heatmap_assisted_diagnosis/models/CARZero_best_model.ckpt", device=device)
    print(backbone)
    exit()
    model = LinearProbe(backbone, logit_dim=768, num_classes=args.num_classes).to(device)

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total     = sum(p.numel() for p in model.parameters())
    print(f"Trainable params: {trainable:,} / {total:,}")

    # Step 3: Loss — BCE instead of CrossEntropy for multi-label
    loss_fn     = nn.BCEWithLogitsLoss()  # expects float labels [B, num_classes]
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
            print(preds.shape)            # [B, num_classes] logits
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
            all_preds, all_labels = [], []

            for step, (images, labels) in enumerate(val_loader):
                images = images.to(device)
                labels = labels.float().to(device)

                with torch.no_grad():
                    logits = model(images)                        # [B, num_classes]
                    l = val_loss_fn(logits, labels)
                    val_epoch_loss += l.item()

                    # Threshold at 0.5 after sigmoid for binary predictions
                    preds_binary = (torch.sigmoid(logits) > 0.5).cpu().numpy()
                    all_preds.extend(preds_binary)
                    all_labels.extend(labels.cpu().numpy())

            val_epoch_loss = val_epoch_loss / (step + 1)

            # Use macro F1 for multi-label — treats each class equally
            f1           = f1_score(all_labels, all_preds, average='macro', zero_division=0)
            f1_per_class = f1_score(all_labels, all_preds, average=None,    zero_division=0)

            print(f"val_loss: {val_epoch_loss:.4f} | macro F1: {f1:.4f}")
            print(f"per-class F1: {f1_per_class}")

            tensorboard_writer.add_scalar("val_loss", val_epoch_loss, epoch)
            tensorboard_writer.add_scalar("f1_macro", f1, epoch)
            for i, f in enumerate(f1_per_class):
                tensorboard_writer.add_scalar(f"f1_class_{i}", f, epoch)

            torch.save(model.head.state_dict(), trained_last_path)

            if f1 > best_f1:
                best_f1 = f1
                torch.save(model.head.state_dict(), trained_best_path)
                print(f"New best macro F1: {best_f1:.4f} — saved to {trained_best_path}")


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="[%(asctime)s.%(msecs)03d][%(levelname)5s](%(name)s) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()