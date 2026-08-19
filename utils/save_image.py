import numpy as np
import matplotlib.pyplot as plt

# ========== Save Utilities ==========
def save_image(array, path, cmap='gray'):
    # Normalize to [0, 1] for display
    array = array.astype(np.float32)
    array = (array - array.min()) / (array.max() - array.min() + 1e-8)

    if array.ndim == 3 and array.shape[0] == 3:
        array = np.transpose(array, (1, 2, 0))
        plt.imsave(path, array)
    elif array.ndim == 2:
        plt.imsave(path, array, cmap=cmap)
    elif array.ndim == 3 and array.shape[0] == 1:
        plt.imsave(path, array[0], cmap=cmap)
    else:
        raise ValueError(f"Unexpected shape {array.shape}")
