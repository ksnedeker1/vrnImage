import matplotlib.pyplot as plt
import numpy as np


def generate_heatmap_img(heatmap, colormap="inferno"):
    """
    Create an array representing an RGB image with pixels colored based on their
    value from [0, 255] in heatmap.
    """
    heatmap_normalized = heatmap / 255
    heatmap_colored = (plt.get_cmap(colormap)(heatmap_normalized)[:, :, :3] * 255).astype(np.uint8)
    return heatmap_colored
