"""
Plot comparison figures across checkpoints, using the .npz file produced by
run_eval_all_checkpoints.py.

Produces:
  1. roc_comparison.png   - one ROC curve per checkpoint (micro-averaged
                             across classes) overlaid on a single plot.
  2. auroc_bar_comparison.png - bar chart of mean AUROC (macro-averaged
                             across classes) per checkpoint.

Usage:
    python plot_checkpoint_comparison.py --npz /path/to/all_checkpoint_results.npz --output-dir /path/to/save/plots
"""
import os
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")  # safe for headless / cluster environments
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

parser = argparse.ArgumentParser(description="Plot ROC and AUROC comparison across checkpoints")
parser.add_argument("--npz", required=True, help="Path to all_checkpoint_results.npz")
parser.add_argument("--output-dir", required=True, help="Where to save the plots")
args = parser.parse_args()

os.makedirs(args.output_dir, exist_ok=True)

data = np.load(args.npz, allow_pickle=True)
checkpoint_labels = list(data["checkpoint_labels"])
model_names = list(data["model_names"])
datasets = list(data["datasets"])
mean_auroc = data["mean_auroc"]
mean_auprc = data["mean_auprc"]

# Exclude ark_large from all comparisons
keep_idx = [i for i, m in enumerate(model_names) if m != "ark_large"]
checkpoint_labels = [checkpoint_labels[i] for i in keep_idx]
model_names = [model_names[i] for i in keep_idx]
datasets = [datasets[i] for i in keep_idx]
mean_auroc = mean_auroc[keep_idx]
mean_auprc = mean_auprc[keep_idx]

unique_datasets = sorted(set(datasets))

# ---------------------------------------------------------------------------
# 1. Overlaid ROC curves (micro-averaged across classes per model), one plot
#    per dataset so the 3-models-x-2-datasets comparison stays readable.
# ---------------------------------------------------------------------------
for dataset_name in unique_datasets:
    plt.figure(figsize=(8, 7))

    for ckpt_label, model_name, ds in zip(checkpoint_labels, model_names, datasets):
        if ds != dataset_name:
            continue

        labels = data[f"labels__{ckpt_label}"]   # [N, num_classes]
        probs  = data[f"probs__{ckpt_label}"]    # [N, num_classes]

        # Micro-average: flatten across all classes/samples, treating every
        # (sample, class) pair as one binary prediction. This gives a single
        # ROC curve per model that's comparable even with class imbalance.
        labels_flat = labels.ravel()
        probs_flat = probs.ravel()

        fpr, tpr, _ = roc_curve(labels_flat, probs_flat)
        roc_auc_val = auc(fpr, tpr)

        plt.plot(fpr, tpr, lw=2, label=f"{model_name} (AUC = {roc_auc_val:.3f})")

    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", lw=1)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Comparison Across Models — {dataset_name} (micro-averaged)")
    plt.legend(loc="lower right", fontsize=9)
    plt.tight_layout()

    roc_path = os.path.join(args.output_dir, f"roc_comparison_{dataset_name}.png")
    plt.savefig(roc_path, dpi=200)
    plt.close()
    print(f"Saved ROC comparison plot to {roc_path}")

# ---------------------------------------------------------------------------
# 2. Bar chart of mean (macro) AUROC, grouped by dataset, one bar per model
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.edgecolor": "0.3",
    "axes.linewidth": 0.8,
})

fig, ax = plt.subplots(figsize=(8, 5))

unique_models = sorted(set(model_names))
x = np.arange(len(unique_models))
bar_width = 0.8 / len(unique_datasets)

# A muted, print-friendly palette (colorblind-safe)
palette = ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377"]

for i, dataset_name in enumerate(unique_datasets):
    values = []
    for model_name in unique_models:
        match = [
            mean_auroc[j] for j in range(len(checkpoint_labels))
            if model_names[j] == model_name and datasets[j] == dataset_name
        ]
        values.append(match[0] if match else np.nan)

    offset = (i - (len(unique_datasets) - 1) / 2) * bar_width
    bars = ax.bar(
        x + offset, values, width=bar_width * 0.9,
        label=dataset_name, color=palette[i % len(palette)],
        edgecolor="white", linewidth=0.6, zorder=3,
    )

    for bar, val in zip(bars, values):
        if not np.isnan(val):
            ax.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.012,
                f"{val:.3f}", ha="center", va="bottom",
                fontsize=8, color="0.2",
            )

# Clean up axes
ax.set_xticks(x)
ax.set_xticklabels(unique_models, rotation=0, ha="center", fontsize=10.5)
ax.set_ylabel("Mean AUROC (macro)", fontsize=11)
ax.set_ylim([0.0, 1.0])
ax.set_title("Mean AUROC by Model and Dataset", fontsize=13, pad=14, weight="bold")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.yaxis.grid(True, linestyle="-", linewidth=0.6, color="0.85", zorder=0)
ax.set_axisbelow(True)
ax.tick_params(left=False, bottom=False)

legend = ax.legend(
    title="Dataset", frameon=False, loc="upper center",
    bbox_to_anchor=(0.5, -0.12), ncol=len(unique_datasets), fontsize=9.5,
    title_fontsize=10,
)

plt.tight_layout()

bar_path = os.path.join(args.output_dir, "auroc_bar_comparison.png")
plt.savefig(bar_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved AUROC bar chart to {bar_path}")

print("\n✅ Done plotting.")