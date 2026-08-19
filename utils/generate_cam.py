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
def generate_cam(model, input_tensor, output_path, threshold=0.5):
    model.eval()

    # Enable gradients for all parameters
    for param in model.parameters():
        param.requires_grad_(True)

    H_feat = W_feat = input_tensor.shape[-1] // 16

    hooks = []
    saved = {"feat": None, "grad": None}

    # Target the norm layer inside the last block for better localization
    target_layer = model.blocks[-1].norm1

    def fwd_hook(module, input, output):
        saved["feat"] = output[:, 1:, :].detach()  # detach feat, only grad needs graph

    def bwd_hook(module, grad_in, grad_out):
        saved["grad"] = grad_out[0][:, 1:, :]

    hooks.append(target_layer.register_forward_hook(fwd_hook))
    hooks.append(target_layer.register_full_backward_hook(bwd_hook))

    # Forward pass — no use_no_grad argument anymore since model is not LinearProbe
    input_tensor = input_tensor.requires_grad_(True)
    scores = model(input_tensor)

    probs = torch.sigmoid(scores)
    positive_classes = (probs > threshold).squeeze().nonzero(as_tuple=True)[0].tolist()
    if len(positive_classes) == 0:
        positive_classes = [torch.argmax(probs).item()]

    print(f"Positive classes: {positive_classes}, probs: {probs.squeeze()[positive_classes].tolist()}")

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
        # Reset grad capture before each backward
        saved["grad"] = None
        model.zero_grad()

        scores[0, class_idx].backward(retain_graph=True)

        feat = saved["feat"]   # [1, num_tokens, hidden_dim]
        grad = saved["grad"]   # [1, num_tokens, hidden_dim]

        if feat is None or grad is None:
            print(f"Warning: hooks did not fire for class {class_idx}, skipping")
            continue

        # Correct GradCAM: average weights over feature dim, then weight tokens
        cam = (feat * grad).sum(dim=-1)          # [1, num_tokens] — element-wise then sum over features
        cam = F.relu(cam).squeeze(0)             # [num_tokens]
        cam = cam.reshape(H_feat, W_feat)        # [H_feat, W_feat]

        cam = cam.detach().cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        cam_resized = cv2.resize(cam, (input_tensor.shape[-1], input_tensor.shape[-2]))

        result = overlay_mask(pil_img, Image.fromarray(cam_resized, mode='F'), alpha=0.5)
        result.save(f"{base}_class{class_idx}{ext}")
        print(f"  Saved CAM for class {class_idx} → {base}_class{class_idx}{ext}")

    for h in hooks:
        h.remove()
