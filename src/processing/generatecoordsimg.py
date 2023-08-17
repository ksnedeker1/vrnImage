import numpy as np


def generate_coords_img(shape, coords):
    """
    Create an array representing an RGB image with pixels colored based on their
    proximity to a point in coords.
    """
    # Define colors
    white = np.array([170, 170, 170], dtype=np.uint8)
    gray1 = np.array([100, 100, 100], dtype=np.uint8)
    gray2 = np.array([63, 63, 63], dtype=np.uint8)
    gray3 = np.array([35, 35, 35], dtype=np.uint8)
    # Create output array
    result = np.zeros(shape, dtype=np.uint8)
    # Create a binary mask, this will be used to shade points in coords and neighbors
    # initialize with all points in coords set to 1
    mask = np.zeros(result.shape[:2], dtype=np.uint8)
    x_coords, y_coords = zip(*coords)
    mask[y_coords, x_coords] = 1

    # Previous approaches had overflows with uint8 rolling back to 0
    def safe_addition(img, mask, color):
        additive_color = np.expand_dims(mask, axis=-1) * color
        img += np.minimum(additive_color, 255 - img)
        return img

    # Use mask to apply color to all points in coords to their location in result
    result = safe_addition(result, mask, white)
    # Apply again for all neighbors using appropriate color
    for dy, dx, color in [(-1, 0, gray1), (1, 0, gray1), (0, -1, gray1), (0, 1, gray1),
                          (-1, -1, gray2), (-1, 1, gray2), (1, -1, gray2), (1, 1, gray2),
                          (-2, 0, gray3), (2, 0, gray3), (0, -2, gray3), (0, 2, gray3)]:
        # Shift mask of coords to apply to all neighbors with a given offset
        shifted_mask = np.roll(mask, shift=(dy, dx), axis=(0,1))
        result = safe_addition(result, shifted_mask, color)
    return result
