import torch
import torch.nn as nn
import torch
import torch.nn as nn
import clip
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import sys
sys.path.insert(0, "/storage/homefs/ed22q093/heatmap_assisted_diagnosis/dinov2")

import sys

import torch
from transformers import AutoModel
from timm.models.swin_transformer import SwinTransformer

from monai.networks.nets import ViT

class ViTClassifier_b_16(nn.Module):
    def __init__(self, num_classes=4):
        super(ViTClassifier_b_16, self).__init__()
        self.vit = ViT(
                        in_channels=3,           # grayscale
                        img_size=[224, 224],     # 2D image size
                        patch_size=[16, 16],     # common choice, results in 14x14 patches
                        classification=True,     # enable classification head
                        num_classes=num_classes,           # your number of classes
                        spatial_dims=2,          # important: set to 2 for 2D images
                    )

    def forward(self, x):
        return self.vit(x)

def convert_models_to_fp32(model): 
    for p in model.parameters():
        if p is not None:
            p.data = p.data.float()
            if p.grad is not None:
                p.grad.data = p.grad.data.float()
    return model


def load_checkpoint(model, checkpoint_path, device, strict=False):
    checkpoint = torch.load(checkpoint_path, map_location=device)

    if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    elif isinstance(checkpoint, dict) and 'model' in checkpoint:
        state_dict = checkpoint['model']
    else:
        state_dict = checkpoint

    model.load_state_dict(state_dict, strict=strict)
    return model


def build_model(model_name, num_classes, device, checkpoint_path=None):
    """
    Args:
        model_name      : one of 'eva', 'chexzero', 'raddino'
        num_classes     : number of output classes
        device          : torch device
        checkpoint_path : path to finetuned checkpoint to load after model init.
                          For chexzero this should be the pretrained CLIP checkpoint.
                          For eva/raddino the pretrained weights are loaded internally.
    Returns:
        model ready for training/inference
    """
    if model_name == 'eva':
        from eva_x.eva_x import eva_x_base_patch16
        model = eva_x_base_patch16(
            pretrained="/storage/homefs/ed22q093/heatmap_assisted_diagnosis/models/eva_x_base_patch16_merged520k_mim.pt"
        ).to(device)
        model.head = nn.Linear(768, num_classes).to(device)

    elif model_name == 'chexzero':
        assert checkpoint_path is not None, "chexzero requires a checkpoint_path"
        model, _ = clip.load('ViT-B/32', device=device, jit=False)
        # model.load_state_dict(torch.load(checkpoint_path, map_location=device), strict=True)
        model = convert_models_to_fp32(model)
        model = model.visual
        model.head = nn.Linear(512, num_classes).to(device)
        model = model.to(device)
        return model  # already has pretrained weights, skip load_checkpoint below

    elif model_name == 'raddino':
        model = AutoModel.from_pretrained("microsoft/rad-dino").to(device)
        model.head = nn.Linear(768, num_classes).to(device)

    elif model_name == 'ark':
        model = SwinTransformer(
        num_classes=num_classes,
        img_size=224,
        patch_size=4,
        window_size=7,           # 7 for 224px input (vs 12 for 768px)
        embed_dim=128,           # Swin-Base uses 128 (vs 192 for Large)
        depths=(2, 2, 18, 2),
        num_heads=(4, 8, 16, 32) # Swin-Base num_heads (vs (6,12,24,48) for Large)
    )
        # Load the checkpoint
        checkpoint = torch.load('/storage/homefs/ed22q093/heatmap_assisted_diagnosis/models/ark6_swinbase_224_ep200.pth.tar', map_location="cpu")
        state_dict = checkpoint['teacher']

        # Remove "module." prefix if present
        state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}

        # Identify and delete unnecessary keys
        k_del = [k for k in state_dict.keys() if "attn_mask" in k] + ['head.weight', 'head.bias']
        print(f"Removing key(s) {k_del} from pretrained checkpoint for scaled input size")

        # Delete identified keys
        for k in k_del:
            if k in state_dict:  # Ensure the key exists
                del state_dict[k]

        # Load the model weights
        msg = model.load_state_dict(state_dict, strict=False)
        print('Loaded with msg:', msg)
        model = model.to(device)
    
    elif model_name == 'ark_large':
        model = SwinTransformer(
            num_classes=num_classes,
            img_size=768,
            patch_size=4,
            window_size=12,
            embed_dim=192,
            depths=(2, 2, 18, 2),
            num_heads=(6, 12, 24, 48)
        )
        # Load the checkpoint
        checkpoint = torch.load('/storage/homefs/ed22q093/heatmap_assisted_diagnosis/models/Ark6_swinLarge768_ep50.pth.tar', map_location="cpu")
        state_dict = checkpoint['teacher']

        # Remove "module." prefix if present
        state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}

        # Identify and delete unnecessary keys
        k_del = [k for k in state_dict.keys() if "attn_mask" in k] + ['head.weight', 'head.bias']
        print(f"Removing key(s) {k_del} from pretrained checkpoint for scaled input size")

        # Delete identified keys
        for k in k_del:
            if k in state_dict:  # Ensure the key exists
                del state_dict[k]

        # Load the model weights
        msg = model.load_state_dict(state_dict, strict=False)
        print('Loaded with msg:', msg)
        model = model.to(device)

    elif model_name == 'from_scratch':
        model = ViTClassifier_b_16(num_classes=num_classes).to(device)

    else:
        raise ValueError(f"Unknown model_name '{model_name}'. Choose from: eva, chexzero, raddino")

    # Load finetuned checkpoint if provided
    if checkpoint_path is not None:
        model = load_checkpoint(model, checkpoint_path, device, strict=True)
        print(f"Loaded checkpoint from {checkpoint_path}")

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total     = sum(p.numel() for p in model.parameters())
    print(f"[{model_name}] Trainable params: {trainable:,} / {total:,}")

    return model