import os
import torch
import argparse
import json
from utils.generate_cam_average_single_image import generate_cam_average
from utils.save_image import save_image
from utils.model_selection import build_model
import pandas as pd
from PIL import Image

import torch
from torchvision import transforms
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser(description="GradCAM Heatmap Generation")
parser.add_argument("-c", "--config-file",
    default="/storage/homefs/ed22q093/heatmap_assisted_diagnosis/configs/heatmap.json")
args = parser.parse_args()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
torch.cuda.set_device(device)
torch.backends.cudnn.benchmark = True
torch.set_num_threads(4)
print(f"Using {device}")

df = pd.read_csv("/storage/homefs/ed22q093/heatmap_assisted_diagnosis/combined_100_samples.csv")

classes = [
    "TB",
    "atelectasis",
    "calcification",
    "consolidation",
    "fibrosis",
    "nodule",
    "pleural_effusion",
    "pneumonia",
    "pneumothorax",
    "thickened_pleura",
    "Lung Opacity",
    "Lung cavity",
    "pulmonary_edema"
]

config_dict = json.load(open(args.config_file, "r"))
for k, v in config_dict.items():
    setattr(args, k, v)

if args.dataset == 'vindr':
    XRAY_MEAN = [0.548959, 0.548959, 0.548959]
    XRAY_STD  = [0.268389, 0.268389, 0.268389]
    
    df = df[df['dataset']=="vindr"]

    image_ids = df['image_id']

    image_df = pd.read_csv("/storage/homefs/ed22q093/heatmap_assisted_diagnosis/data/image_labels_test.csv")
    image_df = image_df[image_df['image_id'].isin(image_ids)]

    image_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/data/test"

    image_df['image_path'] = image_df['image_id'].apply(
    lambda x: os.path.join(image_path, x + ".jpg")
)

    df = df.merge(
        image_df[['image_id', 'image_path']],
        on='image_id',
        how='left'
    )

    label_map = {
    0:  "Aortic enlargement",
    1:  "atelectasis",
    2:  "calcification",
    3:  "Cardiomegaly",
    4:  "Clavicle fracture",
    5:  "consolidation",
    6:  "pulmonary_edema",
    7:  "Emphysema",
    8:  "Enlarged PA",
    9:  "ILD",
    10: "Infiltration",
    11: "Lung Opacity",
    12: "Lung cavity",
    13: "Lung cyst",
    14: "Mediastinal shift",
    15: "nodule",
    16: "pleural_effusion",
    17: "thickened_pleura",
    18: "pneumothorax",
    19: "fibrosis",
    20: "Rib fracture",
    21: "Other lesion",
    22: "COPD",
    23: "Lung tumor",
    24: "pneumonia",
    25: "TB",
    26: "Other diseases",
    27: "No finding",
}
else:
    XRAY_MEAN = [0.517730, 0.517730, 0.517730]
    XRAY_STD  = [0.257968, 0.257968, 0.257968]

    df = df[df['dataset']=="chestdr"]

    image_ids = df['image_id']

    image_df = pd.read_csv("/storage/homefs/ed22q093/heatmap_assisted_diagnosis/chestdr/chestdr_published_19d.csv")

    _, chest_df = train_test_split(
            df, test_size=0.2, random_state=42
        )
    image_df = image_df[image_df['img_id'].isin(image_ids)]

    image_path = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/chestdr/images"
    image_df['image_path'] = image_df['img_id'].apply(
    lambda x: os.path.join(image_path, x)
)

    df = df.merge(
        image_df[['img_id', 'image_path']],
        left_on='image_id',
        right_on='img_id',
        how='left'
    )
    label_map = {
    0:  "pleural_effusion",
    1:  "nodule",
    2:  "pneumonia",
    3:  "cardiomegaly",
    4:  "hilar_enlargement",
    5:  "fracture_old",
    6:  "fibrosis",
    7:  "aortic_calcification",
    8:  "tortuous_aorta",
    9:  "thickened_pleura",
    10: "TB",
    11: "pneumothorax",
    12: "emphysema",
    13: "atelectasis",
    14: "calcification",
    15: "pulmonary_edema",
    16: "increased_lung_markings",
    17: "elevated_diaphragm",
    18: "consolidation",
}

transform = transforms.Compose([
            transforms.Resize((args.image_size, args.image_size)),
            transforms.CenterCrop((args.image_crop, args.image_crop)),
            transforms.ToTensor(),
            transforms.Normalize(mean=XRAY_MEAN, std=XRAY_STD),
        ])

# Build single model from config
model = build_model(args.model_name, num_classes=args.num_classes, device=device,
                    checkpoint_path=args.checkpoint_path)

# Output dir per model to avoid overwrites
output_dir = args.output_dir
raw_output = "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/heatmaps/final/chestdr/raw"
os.makedirs(output_dir, exist_ok=True)

MAX_SAMPLES = 50
sample_count = 0

# store dataframe rows
results = []

print(f"Generating Grad-CAMs for {MAX_SAMPLES} val samples [{args.model_name}]...")

for _, row in df.iterrows():

    if sample_count >= MAX_SAMPLES:
        break
    print(row['image_path'])
    # img = Image.open(row['image_path']).convert('RGB')
    # input_save_path = os.path.join(
    #     raw_output,
    #     f"sample_{sample_count:04d}_input.png"
    # )
    # save_image(input_tensor.squeeze(0).cpu().numpy(), input_save_path)

    img = Image.open(row['image_path']).convert('RGB')

    # resize to 518x518
    # img = img.resize((518, 518))

    # input_save_path = os.path.join(
    #     raw_output,
    #     f"sample_{sample_count:04d}_input.png"
    # )

    # # save resized image
    # img.save(input_save_path)


    input_tensor = transform(img).unsqueeze(0).to(device)


    cam_save_path = os.path.join(
        output_dir,
        f"sample_{sample_count:04d}_cam.png"
    )

    predicted = generate_cam_average(
        model,
        input_tensor,
        cam_save_path,
        model_name=args.model_name,
        label_map=label_map
    )

    print(predicted)

    # initialize row
    sample_row = {
        "image_id": row["image_id"],
        "sample_count": sample_count,
        "dataset": row["dataset"],
        "model": args.model_name
    }

    # multi-label one-hot encoding
    for cls in classes:
        sample_row[cls] = int(cls.lower() in predicted)

    results.append(sample_row)

    sample_count += 1

    print(f"  [{sample_count}/{MAX_SAMPLES}] saved to {cam_save_path}")


# create dataframe
results_df = pd.DataFrame(results)

results_df.to_csv(args.csv_save_path, index=False)

print(results_df.head())

# models = {
#     "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark_224/vindr/eva_x_best.pth":
#         "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/heatmaps/visual_test/ark/vindr/5e5_best",

#     "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark_224/vindr/eva_x_last.pth":
#         "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/heatmaps/visual_test/ark/vindr/5e5_last",

#     "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark_224/vindr_1e4/eva_x_best.pth":
#         "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/heatmaps/visual_test/ark/vindr/1e4_best",

#     "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark_224/vindr_1e4/eva_x_last.pth":
#         "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/heatmaps/visual_test/ark/vindr/1e4_last",

#     "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark_224/vindr_1e5/eva_x_best.pth":
#         "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/heatmaps/visual_test/ark/vindr/1e5_best",

#     "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/logs/ark_224/vindr_1e5/eva_x_last.pth":
#         "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/heatmaps/visual_test/ark/vindr/1e5_last"
# }

# MAX_SAMPLES = 5

# # store all models together
# all_results = []

# for checkpoint_path, output_dir in models.items():

#     print("=" * 80)
#     print(f"Loading model: {checkpoint_path}")

#     os.makedirs(output_dir, exist_ok=True)

#     # Build model for this checkpoint
#     model = build_model(
#         args.model_name,
#         num_classes=args.num_classes,
#         device=device,
#         checkpoint_path=checkpoint_path
#     )

#     sample_count = 0
#     results = []

#     print(f"Generating Grad-CAMs for {MAX_SAMPLES} samples...")

#     for _, row in df.iterrows():

#         if sample_count >= MAX_SAMPLES:
#             break

#         print(row['image_path'])

#         img = Image.open(row['image_path']).convert('RGB')

#         input_tensor = transform(img).unsqueeze(0).to(device)

#         cam_save_path = os.path.join(
#             output_dir,
#             f"sample_{sample_count:04d}_cam.png"
#         )

#         predicted = generate_cam_average(
#             model,
#             input_tensor,
#             cam_save_path,
#             model_name=args.model_name,
#             label_map=label_map
#         )

#         print(predicted)

#         sample_row = {
#             "image_id": row["image_id"],
#             "sample_count": sample_count,
#             "dataset": row["dataset"],
#             "model": args.model_name,
#             "checkpoint": os.path.basename(checkpoint_path),
#             "output_dir": output_dir
#         }

#         # multi-label one-hot encoding
#         predicted_lower = [p.lower() for p in predicted]

#         for cls in classes:
#             sample_row[cls] = int(cls.lower() in predicted_lower)

#         results.append(sample_row)

#         sample_count += 1

#         print(f"[{sample_count}/{MAX_SAMPLES}] saved to {cam_save_path}")

#     # dataframe for current model
#     results_df = pd.DataFrame(results)

#     # optional save per model
#     csv_name = os.path.join(
#         output_dir,
#         "predictions.csv"
#     )

#     results_df.to_csv(csv_name, index=False)

#     print(results_df.head())

#     # accumulate all models
#     all_results.append(results_df)

# # final combined dataframe
# final_results_df = pd.concat(all_results, ignore_index=True)

# # optional combined csv
# final_results_df.to_csv("all_model_predictions.csv", index=False)

# print(final_results_df.head())