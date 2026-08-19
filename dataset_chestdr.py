import os
import pandas as pd
from PIL import Image

import torch
from torch.utils.data import Dataset
from torchvision import transforms
from sklearn.model_selection import train_test_split

CLASS_NAMES = [
    "pleural_effusion", "nodule", "pneumonia", "cardiomegaly", "hilar_enlargement",
    "fracture_old", "fibrosis", "aortic_calcification", "tortuous_aorta",
    "thickened_pleura", "TB", "pneumothorax", "emphysema", "atelectasis",
    "calcification", "pulmonary_edema", "increased_lung_markings",
    "elevated_diaphragm", "consolidation"
]

# X-ray specific stats — replace with your computed mean/std if available
XRAY_MEAN = [0.517730, 0.517730, 0.517730]
XRAY_STD  = [0.257968, 0.257968, 0.257968]

def get_transforms(mode="train", img_size=336, img_crop=224):
    if mode == "train":
        return transforms.Compose([
            transforms.Resize((img_size, img_size)),
            # transforms.RandomCrop((224, 224)),
            transforms.CenterCrop((img_crop, img_crop)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ToTensor(),
            transforms.Normalize(mean=XRAY_MEAN, std=XRAY_STD),
        ])
        # return  transforms.Compose([
        # transforms.RandomResizedCrop(size=(224, 224), scale=(0.7, 0.9), ratio=(0.8, 1.2)),
        # transforms.RandomHorizontalFlip(p=0.5),
        # transforms.RandomRotation(degrees=10),
        # transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 1.0)),
        # transforms.RandomAdjustSharpness(sharpness_factor=2, p=0.3),
        # transforms.ToTensor(),
        # transforms.Normalize(mean=XRAY_MEAN, std=XRAY_STD),
    # ])
    else:
        return transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.CenterCrop((img_crop, img_crop)),
            transforms.ToTensor(),
            transforms.Normalize(mean=XRAY_MEAN, std=XRAY_STD),
        ])


class ChestXrayDataset(Dataset):
    def __init__(self, csv_path, images_dir, transform="train", img_size=224, img_crop=224,
                 split="train", val_size=0.2, random_state=42):
        """
        Args:
            csv_path     : path to csv file
            images_dir   : folder containing the images
            transform    : "train" or "val" string, or a torchvision transform object
            img_size     : image size (default 224)
            split        : "train" or "val" — which split to use
            val_size     : fraction of data to use for validation (default 0.2)
            random_state : random seed for reproducible splits
        """
        df = pd.read_csv(csv_path)

        # Rename img_id -> image_id for internal consistency
        if "img_id" in df.columns and "image_id" not in df.columns:
            df = df.rename(columns={"img_id": "image_id"})

        train_df, val_df = train_test_split(
            df, test_size=val_size, random_state=random_state
        )

        self.df          = train_df if split == "train" else val_df
        self.df          = self.df.reset_index(drop=True)
        self.images_dir  = images_dir
        self.class_names = CLASS_NAMES

        if isinstance(transform, str):
            self.transform = get_transforms(mode=transform, img_size=img_size, img_crop=img_crop)
        else:
            self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        # Try .jpg then .png
        img_path = os.path.join(self.images_dir, row['image_id'])

        try:
            image = Image.open(img_path).convert("RGB")
        except Exception as e:
            raise RuntimeError(f"Could not load image {img_path}: {e}")

        if self.transform:
            image = self.transform(image)

        labels = torch.tensor(
            row[self.class_names].values.astype(float),
            dtype=torch.float32
        )

        return image, labels