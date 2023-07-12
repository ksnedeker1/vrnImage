import numpy as np
import skimage.color


def rgb_to_cielab(image, split=None):
    """
    Converts an RGB image array to CIELAB.
    :param image: The RGB image array to convert
    :param split: Whether the return should split the CIELAB array between luminance and color channels
    :return: CIELAB version of the image array, see param split
    """
    cielab_array = skimage.color.rgb2lab(np.array(image))
    return (cielab_array[:, :, 0], cielab_array[:, :, 1:]) if split else cielab_array
