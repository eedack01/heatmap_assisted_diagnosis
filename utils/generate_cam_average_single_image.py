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
def generate_cam_average(model, input_tensor, output_path, model_name='eva', threshold=0.5, alpha=0.5, label_map=None):
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
    elif model_name == 'ark':
        patch_size = 4
        target_block_indices = [
            (0, 1),
            (1, 1),
            (2, 17),
            (3, 1),
        ]
        stage_feat_sizes = {0: 56, 1: 28, 2: 14, 3: 7}

        # Hook the full block output, not norm1 (which fires mid-attention reshape)
        target_layers = [
            model.layers[stage].blocks[block]  # hook entire block output
            for stage, block in target_block_indices
        ]
        def get_scores(model, input_tensor):
            return model(input_tensor)
    elif model_name == 'ark_large':
        patch_size = 4
        target_block_indices = [
            (0, 1),
            (1, 1),
            (2, 17),
            (3, 1),
        ]
        # img_size=768, patch_size=4 -> initial feature map = 768/4 = 192
        # halved at each subsequent stage via patch merging
        stage_feat_sizes = {0: 192, 1: 96, 2: 48, 3: 24}

        # Hook the full block output, not norm1 (which fires mid-attention reshape)
        target_layers = [
            model.layers[stage].blocks[block]  # hook entire block output
            for stage, block in target_block_indices
        ]
        def get_scores(model, input_tensor):
            return model(input_tensor)
    elif model_name == 'from_scratch':
        patch_size = 16
        target_block_indices = [2, 5, 8, 11]
        target_layers = [model.vit.blocks[i].norm1 for i in target_block_indices]
        def get_scores(model, input_tensor):
            preds, _ = model(input_tensor)  # MONAI ViT returns (logits, hidden_states)
            return preds
    else:  # eva
        patch_size = 16
        target_block_indices = [2, 5, 8, 11]
        target_layers = [model.blocks[i].norm1 for i in target_block_indices]
        def get_scores(model, input_tensor):
            return model(input_tensor)
        
    # stage_feat_sizes = {0: 56, 1: 28, 2: 14, 3: 7}  # only used for ark, safe to define always

    H_feat = W_feat = input_tensor.shape[-1] // patch_size
    # Per-layer hook storage
    saved = {i: {"feat": None, "grad": None} for i in range(len(target_block_indices))}

    hooks = []
    for hook_idx, layer in enumerate(target_layers):
        def make_fwd(idx):
            def fwd_hook(module, input, output):
                out = output[0] if isinstance(output, tuple) else output
                if model_name != 'ark' and model_name != 'ark_large':
                    if out.dim() == 3 and out.shape[0] != 1:
                        out = out.permute(1, 0, 2)
                    saved[idx]["feat"] = out[:, 1:, :].detach()
                else:
                    saved[idx]["feat"] = out.detach()
            return fwd_hook

        def make_bwd(idx):
            def bwd_hook(module, grad_in, grad_out):
                grad = grad_out[0] if isinstance(grad_out, tuple) else grad_out
                if model_name != 'ark' and model_name != 'ark_large':
                    if grad.dim() == 3 and grad.shape[0] != 1:
                        grad = grad.permute(1, 0, 2)
                    saved[idx]["grad"] = grad[:, 1:, :]
                else:
                    saved[idx]["grad"] = grad
            return bwd_hook

        hooks.append(layer.register_forward_hook(make_fwd(hook_idx)))
        hooks.append(layer.register_full_backward_hook(make_bwd(hook_idx)))

    input_tensor = input_tensor.requires_grad_(True)
    scores = get_scores(model, input_tensor)

    probs = torch.sigmoid(scores)
    positive_classes = (probs > threshold).squeeze().nonzero(as_tuple=True)[0].tolist()
    positive_class_names = [label_map[i] for i in positive_classes] if label_map else positive_classes
    print(f"Positive classes: {positive_class_names}")
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

    all_class_cams = []

    for class_idx in positive_classes:
        for i in range(len(target_block_indices)):
            saved[i]["grad"] = None
        model.zero_grad()
        scores[0, class_idx].backward(retain_graph=True)

        activation_maps = []

        for hook_idx, layer_idx in enumerate(target_block_indices):
                    feat = saved[hook_idx]["feat"]
                    grad = saved[hook_idx]["grad"]

                    if feat is None or grad is None:
                        print(f"Warning: hooks did not fire for block {layer_idx}, skipping")
                        continue

                    cam = (feat * grad).sum(dim=-1)
                    cam = F.relu(cam).squeeze(0)

                    if model_name == 'ark' or model_name == 'ark_large':
                        stage = layer_idx[0]
                        hw = stage_feat_sizes[stage]
                    else:
                        hw = H_feat

                    cam = cam.reshape(hw, hw)
                    cam = cam.detach().cpu().numpy()
                    cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)

                    # Resize all CAMs to a common size before stacking
                    target_hw = input_tensor.shape[-1] // 4  # e.g. 56 for 224px input
                    if cam.shape[0] != target_hw:
                        cam = cv2.resize(cam, (target_hw, target_hw))

                    activation_maps.append(cam)

        if not activation_maps:
            print(f"No CAMs computed for class {class_idx}, skipping")
            continue

        avg_cam = np.mean(np.stack(activation_maps), axis=0)
        all_class_cams.append(avg_cam)

    if not all_class_cams:
            print("No CAMs computed, skipping output.")
            return positive_class_names  # still return even if no CAM saved
    else:
        merged_cam = np.mean(np.stack(all_class_cams), axis=0)
        merged_cam = (merged_cam - merged_cam.min()) / (merged_cam.max() - merged_cam.min() + 1e-8)

        cam_resized = cv2.resize(merged_cam, (input_tensor.shape[-1], input_tensor.shape[-2]))
        result = overlay_mask(pil_img, Image.fromarray(cam_resized, mode='F'), alpha=alpha)
        # result.save(output_path)

        # base, ext = os.path.splitext(output_path)
        result_large = result.resize((518, 518), Image.LANCZOS)
        result_large.save(output_path)
        print(f"Saved merged CAM ({len(all_class_cams)} classes) → {output_path}")

    for h in hooks:
        h.remove()

    return positive_class_names