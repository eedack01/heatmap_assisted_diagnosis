import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np


# Mapping from vindr column names -> chestdr column names
# mapping_dict = {
#     "Atelectasis": "atelectasis",
#     "Calcification": "calcification",
#     "Consolidation": "consolidation",
#     "Emphysema": "emphysema",
#     "Pleural effusion": "pleural_effusion",
#     "Nodule/Mass": "nodule",
#     "Pneumonia": "pneumonia",
#     "Pulmonary fibrosis": "fibrosis",
#     "Pleural thickening": "thickened_pleura",
#     "Pneumothorax": "pneumothorax",
#     "Tuberculosis": "TB",
# }

mapping_dict = {
    "Atelectasis": "atelectasis",
    "Calcification": "calcification",
    "Consolidation": "consolidation",
    "Pleural effusion": "pleural_effusion",
    "Nodule/Mass": "nodule",
    "Pneumonia": "pneumonia",
    "Pulmonary fibrosis": "fibrosis",
    "Pleural thickening": "thickened_pleura",
    "Pneumothorax": "pneumothorax",
    "Tuberculosis": "TB",
}

# All unique aligned label names across both datasets
shared_classes = sorted(set(mapping_dict.values()))
# vindr_only     = ["ILD", "Infiltration", "Lung Opacity", "Lung cavity", "Lung cyst", "COPD", "Lung tumor"]
# chestdr_only   = ["aortic_calcification", "pulmonary_edema"]
vindr_only     = [ "Lung Opacity", "Lung cavity"]
chestdr_only   = ["pulmonary_edema"]
all_classes    = shared_classes + sorted(vindr_only) + sorted(chestdr_only)


def sample_50(df, classes, dataset_name, image_id_col, random_state=42, max_per_class=None):
    """classes here are the ORIGINAL column names in df (before renaming)."""

    filtered = df[df[classes].any(axis=1)].copy()

    missing = [c for c in classes if filtered[c].sum() == 0]
    if missing:
        print(f"⚠️  [{dataset_name}] No positive samples for: {missing}")

    usable_classes = [c for c in classes if c not in missing]

    # Guarantee at least one sample per class
    one_per_class_indices = set()
    for cls in usable_classes:
        picked = filtered[filtered[cls] == 1].sample(1, random_state=random_state).index[0]
        one_per_class_indices.add(picked)

    one_per_class = filtered.loc[list(one_per_class_indices)]
    remaining = filtered.drop(index=one_per_class.index)
    n_remaining = 50 - len(one_per_class)

    if n_remaining < 0:
        raise ValueError(f"[{dataset_name}] Guaranteed rows ({len(one_per_class)}) exceed 50 slots.")
    if n_remaining > len(remaining):
        raise ValueError(f"[{dataset_name}] Not enough remaining rows ({len(remaining)}) to fill {n_remaining} slots.")

    # ── NEW: cap over-represented classes before random fill ──────────────────
    if max_per_class is not None:
        # Count how many of each class are already guaranteed
        already_counts = {cls: int(one_per_class[cls].sum()) for cls in usable_classes}
        
        # Build a pool that respects the cap per class
        pool_rows = []
        for _, row in remaining.iterrows():
            row_classes = [cls for cls in usable_classes if row[cls] == 1]
            # Accept the row only if at least one of its classes is still under the cap
            if any(already_counts.get(cls, 0) < max_per_class for cls in row_classes):
                pool_rows.append(row.name)
                for cls in row_classes:
                    already_counts[cls] = already_counts.get(cls, 0) + 1
        
        remaining = remaining.loc[pool_rows]
        if n_remaining > len(remaining):
            raise ValueError(
                f"[{dataset_name}] After capping at {max_per_class}/class, only "
                f"{len(remaining)} rows remain but need {n_remaining}."
            )
    # ─────────────────────────────────────────────────────────────────────────

    extra = remaining.sample(n=n_remaining, random_state=random_state)

    result = (
        pd.concat([one_per_class, extra])
        .sample(frac=1, random_state=random_state)
        .reset_index(drop=True)
    )

    result["image_id"] = result[image_id_col]
    result["dataset"]  = dataset_name

    # Coverage check
    print(f"\n[{dataset_name}] {len(result)} samples — class coverage:")
    for cls in usable_classes:
        count  = result[cls].sum()
        status = "✅" if count > 0 else "❌"
        print(f"  {status} {cls}: {int(count)}")

    return result


# ── VinDR ─────────────────────────────────────────────────────────────────────

vindr_df = pd.read_csv("/storage/homefs/ed22q093/heatmap_assisted_diagnosis/data/image_labels_test.csv")

# vindr_classes = [
#     "Atelectasis", "Calcification", "Consolidation", "Emphysema",
#     "ILD", "Infiltration", "Lung Opacity", "Lung cavity", "Lung cyst",
#     "Nodule/Mass", "Pleural effusion", "Pleural thickening", "Pneumothorax",
#     "Pulmonary fibrosis", "COPD", "Lung tumor", "Pneumonia", "Tuberculosis"
# ]

vindr_classes = [
    "Atelectasis", "Calcification", "Consolidation", "Lung Opacity", "Lung cavity",
    "Nodule/Mass", "Pleural effusion", "Pleural thickening", "Pneumothorax",
    "Pulmonary fibrosis", "Pneumonia", "Tuberculosis"
]

vindr_sample = sample_50(vindr_df, vindr_classes, "vindr", "image_id", random_state=42)

# Rename vindr columns -> aligned names, drop unmapped vindr-only cols temporarily
vindr_out = vindr_sample[["image_id", "dataset"] + vindr_classes].copy()
vindr_out = vindr_out.rename(columns=mapping_dict)


# ── ChestDR ───────────────────────────────────────────────────────────────────

chestdr_df = pd.read_csv("/storage/homefs/ed22q093/heatmap_assisted_diagnosis/chestdr/chestdr_published_19d.csv")

if "img_id" in chestdr_df.columns and "image_id" not in chestdr_df.columns:
    chestdr_df = chestdr_df.rename(columns={"img_id": "image_id"})

_, chestdr_df = train_test_split(chestdr_df, test_size=0.2, random_state=42)

# chestdr_classes = [
#     "pleural_effusion", "nodule", "pneumonia", "fibrosis",
#     "aortic_calcification", "thickened_pleura", "TB", "pneumothorax",
#     "emphysema", "atelectasis", "calcification", "pulmonary_edema", "consolidation"
# ]

chestdr_classes = [
    "pleural_effusion", "nodule", "pneumonia", 
    "fibrosis", "thickened_pleura", "TB", "pneumothorax", 
    "atelectasis", "calcification", "pulmonary_edema", "consolidation"
]

chestdr_sample = sample_50(chestdr_df, chestdr_classes, "chestdr", "image_id", random_state=42, max_per_class=15)
chestdr_out = chestdr_sample[["image_id", "dataset"] + chestdr_classes].copy()


# ── Merge with aligned columns ────────────────────────────────────────────────

# concat with align=True fills missing columns with NaN on each side
combined = (
    pd.concat([vindr_out, chestdr_out], ignore_index=True)
    [["image_id", "dataset"] + all_classes]  # consistent column order
    .reset_index(drop=True)
)

# NaN means "this class doesn't exist in that dataset" — make that explicit
combined[all_classes] = combined[all_classes].fillna(-1).astype(int)

print(f"\n{'─'*40}")
print(f"Total samples : {len(combined)}")
print(f"Per dataset   :\n{combined['dataset'].value_counts().to_string()}")
print(f"\nColumns: {combined.columns.tolist()}")

combined.to_csv("combined_100_samples.csv", index=False)
print("\n✅ Saved to combined_100_samples.csv")