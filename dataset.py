import os
import pandas as pd
from PIL import Image

import torch
from torch.utils.data import Dataset
from torchvision import transforms


CLASS_NAMES = [
    "Aortic enlargement", "Atelectasis", "Calcification", "Cardiomegaly",
    "Clavicle fracture", "Consolidation", "Edema", "Emphysema", "Enlarged PA",
    "ILD", "Infiltration", "Lung Opacity", "Lung cavity", "Lung cyst",
    "Mediastinal shift", "Nodule/Mass", "Pleural effusion", "Pleural thickening",
    "Pneumothorax", "Pulmonary fibrosis", "Rib fracture", "Other lesion", "COPD",
    "Lung tumor", "Pneumonia", "Tuberculosis", "Other diseases", "No finding"
]

# X-ray specific stats — replace with your computed mean/std if available
XRAY_MEAN = [0.548959, 0.548959, 0.548959]
XRAY_STD  = [0.268389, 0.268389, 0.268389]

def get_transforms(mode="train", img_size=224, img_crop=224):
    """
    Args:
        mode: "train" or "val"
    """
    if mode == "train":
        return transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.CenterCrop((img_crop, img_crop)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            # transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=XRAY_MEAN, std=XRAY_STD),
        ])
    else:
        return transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.CenterCrop((img_crop, img_crop)),
            transforms.ToTensor(),
            transforms.Normalize(mean=XRAY_MEAN, std=XRAY_STD),
        ])


class ChestXrayDataset(Dataset):
    def __init__(self, csv_path, images_dir, transform="train", img_size=224, img_crop=224):
        """
        Args:
            csv_path   : path to csv file
            images_dir : folder containing the JPEG images
            transform  : "train" or "val" string, or a torchvision transform object
            img_size   : image size (default 224)
        """
        self.df          = pd.read_csv(csv_path)
        self.images_dir  = images_dir
        self.class_names = CLASS_NAMES

        # Accept either a mode string from the config or a pre-built transform
        if isinstance(transform, str):
            self.transform = get_transforms(mode=transform, img_size=img_size, img_crop=img_crop)
        else:
            self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        img_path = os.path.join(self.images_dir, f"{row['image_id']}.jpg")
        try:
            image = Image.open(img_path).convert("RGB")
        except Exception as e:
            raise RuntimeError(f"Could not load image {img_path}: {e}")

        if self.transform:
            image = self.transform(image)

        labels = torch.tensor(
            row[self.class_names].values.astype(float),
            dtype=torch.float32  # float32 required by BCEWithLogitsLoss
        )

        return image, labels