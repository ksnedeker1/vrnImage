import numpy as np


def sample_coordinates(heatmap, num_points, linearity_power=1):
    """
    Sample coordinates from a heatmap.
    :param heatmap: 2D array where the 'importance' of a coord is expressed between 0 and 1.
    :param num_points: Number of coordinates to sample.
    :returns: List of (y, x) coordinates sampled from the heatmap.
    """
    # Flatten and normalize to make a proper probability distribution
    flat = heatmap.flatten().astype(np.float64) ** linearity_power
    flat /= flat.sum()
    # Sampling and conversion back to 2D
    sampled_flat = np.random.choice(len(flat), size=num_points, replace=False, p=flat)
    sampled_coords = np.unravel_index(sampled_flat, heatmap.shape)
    sampled_coords = list(zip(*sampled_coords))
    return sampled_coords
