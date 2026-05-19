import torch.nn as nn
import torch
import torch.nn.functional as F


class FocalLoss(nn.Module):
    """
    Focal loss for multi-label classification.
    FL(p) = -alpha * (1 - p)^gamma * log(p)
    
    gamma > 0 reduces loss for well-classified examples, focusing on hard ones.
    alpha balances positive/negative samples.
    """
    def __init__(self, alpha=0.25, gamma=2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, logits, targets):
        bce_loss = F.binary_cross_entropy_with_logits(logits, targets, reduction='none')
        probs    = torch.sigmoid(logits)
        # For positive labels: (1-p)^gamma, for negative labels: p^gamma
        p_t      = probs * targets + (1 - probs) * (1 - targets)
        alpha_t  = self.alpha * targets + (1 - self.alpha) * (1 - targets)
        focal_loss = alpha_t * (1 - p_t) ** self.gamma * bce_loss
        return focal_loss.mean()