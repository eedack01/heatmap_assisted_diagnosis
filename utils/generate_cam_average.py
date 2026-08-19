import os
import numpy as np
import torch
from torchcam.utils import overlay_mask
from PIL import Image
import cv2
import torch
import numpy as np
from PIL import Image
import cv2
import torch.nn.functional as F

# ========== CAM Generation ==========
def generate_cam_average(model, input_tensor, output_path, model_name='eva', threshold=0.5, alpha=0.5):
    model.eval()
    for param in model.parameters():
        param.requires_grad_(True)

    # Patch size and block access differ per architecture
    if model_name == 'chexzero':
        patch_size = 32
        target_block_indices = [2, 5, 8, 11]
        target_layers = [model.transformer.resblocks[i].ln_1 for i in target_block_indices]
        def get_scores(model, input_tensor):
            features = model(input_tensor)
            return model.head(features)
    elif model_name == 'raddino':
        patch_size = 14  # RAD-DINO uses ViT-B/14
        target_block_indices = [2, 5, 8, 11]
        target_layers = [model.encoder.layer[i].norm1 for i in target_block_indices]
        def get_scores(model, input_tensor):
            outputs = model(pixel_values=input_tensor)
            features = outputs.last_hidden_state[:, 0, :]
            return model.head(features)
    else:  # eva
        patch_size = 16
        target_block_indices = [2, 5, 8, 11]
        target_layers = [model.blocks[i].norm1 for i in target_block_indices]
        def get_scores(model, input_tensor):
            return model(input_tensor)

    H_feat = W_feat = input_tensor.shape[-1] // patch_size

    # Per-layer hook storage
    saved = {i: {"feat": None, "grad": None} for i in target_block_indices}

    hooks = []
    for i, layer in zip(target_block_indices, target_layers):
        def make_fwd(idx):
            def fwd_hook(module, input, output):
                # CLIP returns (seq_len, batch, dim) — need to handle both
                out = output[0] if isinstance(output, tuple) else output
                if out.dim() == 3 and out.shape[0] != 1:
                    out = out.permute(1, 0, 2)  # (S, B, D) → (B, S, D) for CLIP
                saved[idx]["feat"] = out[:, 1:, :].detach()
            return fwd_hook

        def make_bwd(idx):
            def bwd_hook(module, grad_in, grad_out):
                grad = grad_out[0]
                if grad.dim() == 3 and grad.shape[0] != 1:
                    grad = grad.permute(1, 0, 2)  # (S, B, D) → (B, S, D) for CLIP
                saved[idx]["grad"] = grad[:, 1:, :]
            return bwd_hook

        hooks.append(layer.register_forward_hook(make_fwd(i)))
        hooks.append(layer.register_full_backward_hook(make_bwd(i)))

    input_tensor = input_tensor.requires_grad_(True)
    scores = get_scores(model, input_tensor)

    probs = torch.sigmoid(scores)
    positive_classes = (probs > threshold).squeeze().nonzero(as_tuple=True)[0].tolist()
    if len(positive_classes) == 0:
        positive_classes = [torch.argmax(probs).item()]

    print(f"Positive classes: {positive_classes}")

    # Prepare PIL image for overlay
    img_np = input_tensor.squeeze(0).detach().cpu().numpy()
    if img_np.shape[0] == 1:
        img_np = img_np[0]
    elif img_np.shape[0] == 3:
        img_np = np.transpose(img_np, (1, 2, 0))
    img_np = (img_np - img_np.min()) / (img_np.max() - img_np.min() + 1e-8)
    pil_img = Image.fromarray((img_np * 255).astype(np.uint8)).convert("RGB")

    base, ext = os.path.splitext(output_path)

    for class_idx in positive_classes:
        for i in target_block_indices:
            saved[i]["grad"] = None
        model.zero_grad()
        scores[0, class_idx].backward(retain_graph=True)

        activation_maps = []

        for i in target_block_indices:
            feat = saved[i]["feat"]
            grad = saved[i]["grad"]

            if feat is None or grad is None:
                print(f"Warning: hooks did not fire for block {i}, skipping")
                continue

            cam = (feat * grad).sum(dim=-1)
            cam = F.relu(cam).squeeze(0)
            cam = cam.reshape(H_feat, W_feat)
            cam = cam.detach().cpu().numpy()
            cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
            activation_maps.append(cam)

        if not activation_maps:
            print(f"No CAMs computed for class {class_idx}, skipping")
            continue

        avg_cam = np.mean(np.stack(activation_maps), axis=0)
        avg_cam = (avg_cam - avg_cam.min()) / (avg_cam.max() - avg_cam.min() + 1e-8)

        cam_resized = cv2.resize(avg_cam, (input_tensor.shape[-1], input_tensor.shape[-2]))
        result = overlay_mask(pil_img, Image.fromarray(cam_resized, mode='F'), alpha=alpha)
        result.save(f"{base}_class{class_idx}{ext}")
        print(f"Saved averaged CAM for class {class_idx} → {base}_class{class_idx}{ext}")

    for h in hooks:
        h.remove()