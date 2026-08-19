import os
import torch
from torch.utils.data import DataLoader
import argparse
import json
from utils.model_selection import build_model
import numpy as np
from sklearn.metrics import (
    f1_score, hamming_loss, roc_auc_score, average_precision_score
)

parser = argparse.ArgumentParser(description="GradCAM Heatmap Generation")
parser.add_argument("-c", "--config-file",
    default="/storage/homefs/ed22q093/heatmap_assisted_diagnosis/configs/eval.json")
args = parser.parse_args()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
torch.cuda.set_device(device)
torch.backends.cudnn.benchmark = True
torch.set_num_threads(4)
print(f"Using {device}")

config_dict = json.load(open(args.config_file, "r"))
for k, v in config_dict.items():
    setattr(args, k, v)

rad_dino_chestdr_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/rad_dino/chestdr/rad_dino_last.pth"
rad_dino_vindr_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/rad_dino/vindr/rad_dino_last.pth"

eva_x_chestdr_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/eva/chestdr/eva_x_last.pth"
eva_x_vindr_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/eva/vindr_lr_1e-5/eva_x_last.pth"

ark_224_vindr_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark_224/vindr_1e4/eva_x_last.pth"
ark_224_chestdr_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark_224/chestdr_1e4/eva_x_last.pth"

ark_large_vindr_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark/vindr/eva_x_best.pth"
ark_large_chestdr_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark/chestdr/eva_x_best.pth"

# ---------------------------------------------------------------------------
# NOTE: this was referenced below but never defined in the original script.
# Build the list of checkpoints to evaluate here. Adjust to taste — e.g. you
# might want a config-driven list instead, or only the checkpoints matching
# args.dataset (vindr vs chestdr).
# ---------------------------------------------------------------------------
if args.dataset == "vindr":
    checkpoint_paths = [
        # rad_dino_vindr_path,
        # eva_x_vindr_path,
        # ark_224_vindr_path,
        ark_large_vindr_path
    ]
else:
    checkpoint_paths = [
        # rad_dino_chestdr_path,
        # eva_x_chestdr_path,
        # ark_224_chestdr_path,
        ark_large_chestdr_path
    ]

# Build dataset once — it's the same for all checkpoints
if args.dataset == "vindr":
    from dataset import ChestXrayDataset
    print("Loading vindr dataset...")
    val_set = ChestXrayDataset(
        args.vindr_csv_path, args.vindr_image_folder,
        transform=args.val['mode'], img_size=args.image_size,
        img_crop=args.image_crop
    )
else:
    from dataset_chestdr import ChestXrayDataset
    print("Loading chestdr dataset...")
    val_set = ChestXrayDataset(
        args.chestdr_csv_path, args.chestdr_image_folder,
        transform="val", split="val", img_size=args.image_size,
        img_crop=args.image_crop
    )

val_loader = DataLoader(
    val_set, batch_size=args.val['batch_size'], shuffle=False,
    num_workers=args.val['num_workers'], pin_memory=True
)

output_dir = args.output_dir
os.makedirs(output_dir, exist_ok=True)

# Collect results across all checkpoints here so we can compare/plot AUCs afterward
all_results = {}

# Loop through each checkpoint and evaluate
for checkpoint_path in checkpoint_paths:
    checkpoint_label = os.path.relpath(checkpoint_path)
    print(f"\n{'='*70}")
    print(f"Checkpoint: {checkpoint_label}")
    print(f"{'='*70}")

    model = build_model(
        args.model_name, num_classes=args.num_classes,
        device=device, checkpoint_path=checkpoint_path
    )
    model.eval()

    val_epoch_loss = 0.0
    all_preds, all_probs, all_labels = [], [], []

    for step, (images, labels) in enumerate(val_loader):
        images = images.to(device)
        labels = labels.float().to(device)

        with torch.no_grad():
            if args.model_name == "raddino":
                outputs = model(pixel_values=images)
                features = outputs.last_hidden_state[:, 0, :]  # CLS token → [B, 768]
                logits = model.head(features)

            elif args.model_name == "chexzero":
                features = model(images)                        # [B, 512]
                logits = model.head(features)

            elif args.model_name == "from_scratch":
                logits, _ = model(images)

            else:
                logits = model(images)

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

    num_classes = all_labels.shape[1]
    auroc_per_class = []
    auprc_per_class = []

    for c in range(num_classes):
        if all_labels[:, c].sum() == 0:
            print(f"  Warning: class {c} has no positive samples, skipping AUROC/AUPRC")
            auroc_per_class.append(float('nan'))
            auprc_per_class.append(float('nan'))
        else:
            auroc_per_class.append(roc_auc_score(all_labels[:, c], all_probs[:, c]))
            auprc_per_class.append(average_precision_score(all_labels[:, c], all_probs[:, c]))

    mean_auroc = np.nanmean(auroc_per_class)
    mean_auprc = np.nanmean(auprc_per_class)

    print(f"val_loss: {val_epoch_loss:.4f} | macro F1: {f1:.4f} | hamming: {hamming:.4f} | AUROC: {mean_auroc:.4f} | AUPRC: {mean_auprc:.4f}")
    print(f"per-class AUROC: {np.round(auroc_per_class, 4)}")
    print(f"per-class AUPRC: {np.round(auprc_per_class, 4)}")
    print(f"per-class F1:    {np.round(f1_per_class, 4)}")

    # ---- Store everything needed to build a combined AUC/ROC comparison later ----
    # Key by (model_name, dataset) rather than checkpoint path. You're running
    # this script 6 times total (3 models x 2 datasets), one checkpoint active
    # per run, so this key is what you actually want to group/plot by later —
    # it stays stable even if you ever point to a renamed/relocated checkpoint.
    result_key = f"{args.model_name}__{args.dataset}"

    all_results[result_key] = {
        "model_name": args.model_name,
        "dataset": args.dataset,
        "checkpoint_path": checkpoint_path,
        "checkpoint_label": checkpoint_label,
        "val_loss": float(val_epoch_loss),
        "macro_f1": float(f1),
        "f1_per_class": np.round(f1_per_class, 4).tolist(),
        "hamming_loss": float(hamming),
        "mean_auroc": float(mean_auroc),
        "mean_auprc": float(mean_auprc),
        "auroc_per_class": auroc_per_class,
        "auprc_per_class": auprc_per_class,
        # raw labels/probs kept as lists so the whole thing is JSON-serializable;
        # needed to redraw ROC curves (per-class or micro-averaged) later.
        "labels": all_labels.tolist(),
        "probs": all_probs.tolist(),
    }

    # Free GPU memory before loading the next checkpoint's model
    del model
    torch.cuda.empty_cache()

# ---------------------------------------------------------------------------
# Persist results — merge with any existing results file so multiple eval
# runs (e.g. evaluating different checkpoints in separate jobs) accumulate
# into one combined comparison instead of overwriting each other.
# Re-running on the SAME checkpoint label will overwrite just that entry.
# ---------------------------------------------------------------------------
results_json_path = os.path.join(output_dir, "all_checkpoint_results.json")

combined_results = {}
if os.path.exists(results_json_path):
    try:
        with open(results_json_path, "r") as f:
            combined_results = json.load(f)
        print(f"Loaded {len(combined_results)} existing checkpoint result(s) from {results_json_path}")
    except (json.JSONDecodeError, OSError) as e:
        print(f"  Warning: could not read existing results file ({e}), starting fresh")
        combined_results = {}

combined_results.update(all_results)  # new/updated checkpoints take precedence

with open(results_json_path, "w") as f:
    json.dump(combined_results, f)
print(f"Saved combined results ({len(combined_results)} checkpoint(s) total) to {results_json_path}")

# Also save a compact .npz (labels/probs/scores only) — faster to reload for plotting
npz_path = os.path.join(output_dir, "all_checkpoint_results.npz")
np.savez(
    npz_path,
    checkpoint_labels=list(combined_results.keys()),
    model_names=[v["model_name"] for v in combined_results.values()],
    datasets=[v["dataset"] for v in combined_results.values()],
    mean_auroc=[v["mean_auroc"] for v in combined_results.values()],
    mean_auprc=[v["mean_auprc"] for v in combined_results.values()],
    **{f"labels__{k}": np.array(v["labels"]) for k, v in combined_results.items()},
    **{f"probs__{k}": np.array(v["probs"]) for k, v in combined_results.items()},
)
print(f"Saved compact arrays ({len(combined_results)} checkpoint(s) total) to {npz_path}")

print("\n✅ Done.")