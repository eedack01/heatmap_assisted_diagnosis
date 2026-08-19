# Heatmap-Assisted Diagnosis

Code and study materials for evaluating whether Grad-CAM heatmaps from fine-tuned
chest X-ray classifiers help radiologists during diagnosis. Models are trained and
evaluated on two datasets — **VinDr-CXR** (28 findings) and **ChestDR** (19 findings)
— and the resulting heatmaps are used in a reader study comparing radiologists'
diagnoses with and without heatmap assistance.

## Repository layout

Only the directories below are tracked in git; everything else (raw data, model
checkpoints, logs, experiment archives) stays local — see [.gitignore](.gitignore).

```
.
├── *.py                     # training, evaluation, and heatmap generation scripts
├── utils/                   # helper functions used by the top-level scripts
├── configs/                 # JSON configs (one per model/dataset run)
├── final/                   # final heatmaps used in the reader study, per dataset
└── cxr_heatmap_reader_app/  # web app used to run the radiologist reader study
```

### Top-level scripts

| File | Purpose |
|---|---|
| `train.py` | Trains a classifier (Ark, EVA, RadDINO, CheXzero, or from-scratch) on VinDr-CXR or ChestDR, driven by a config from `configs/`. |
| `eval.py` | Evaluates a trained checkpoint against a config-specified dataset (F1, Hamming loss, AUROC, average precision). |
| `heatmap_final.py` | Generates the final Grad-CAM heatmaps from a trained checkpoint — the source of the images in `final/`. |
| `plot_checkpoint_comparison.py` | Builds ROC and AUROC comparison plots across checkpoints. |
| `stats.py` | Computes per-dataset image mean/std for normalization. |
| `dataset.py` | PyTorch `Dataset` for VinDr-CXR (28 classes). |
| `dataset_chestdr.py` | PyTorch `Dataset` for ChestDR (19 classes). |

### `utils/`

| File | Purpose |
|---|---|
| `model_selection.py` | Builds/loads the backbone models (Ark, EVA, RadDINO, dinov2, CLIP-based). |
| `custom_scheduler.py` | Cosine-annealing warm-up-restart LR scheduler. |
| `focal_loss.py` | Focal loss for multi-label classification. |
| `generate_cam.py` | Grad-CAM generation for a single model/image. |
| `generate_cam_average.py` | Grad-CAM generation averaged across models, for a batch. |
| `generate_cam_average_single_image.py` | Averaged Grad-CAM generation for a single image. |
| `save_image.py` | Saves a heatmap/array as an image file. |
| `build_heatmap_csv.py` | Builds the CSV manifests used to drive heatmap generation. |

### `configs/`

JSON configs consumed by `train.py`, `eval.py`, and `heatmap_final.py` — one per
model/dataset combination (e.g. `ark.json` / `ark_chestdr.json`,
`eva_ft.json` / `eva_ft_chestdr.json`, `rad_dino_ft.json`, `chexzero_ft.json`,
`from_scratch.json`), plus `eval.json` and `heatmap.json` for evaluation and
heatmap-generation runs.

### `final/`

The final Grad-CAM heatmaps used in the reader study, split by dataset
(`chestdr/`, `vindr/`) and then by model (`ark/`, `eva/`, `raddino/`, plus `raw/`
for the unannotated source images), with a per-model CSV of case-level info.

### `cxr_heatmap_reader_app/`

The standalone web app used to run the radiologist reader study
(`Open_CXR_Heatmap_Reader_Study.html`). For each case, a radiologist gives an
initial diagnosis from the chest X-ray alone, then is shown the Grad-CAM heatmaps
from all three models and gives a second diagnosis, confidence rating, and
heatmap-helpfulness rating. Includes the case manifest, image assets,
`tools/make_manifest.py` to regenerate the manifest from a results CSV, and a
`Radiologist_Quick_Start_Manual.txt` for study participants.
