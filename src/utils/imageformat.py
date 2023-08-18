import numpy as np
import skimage.color


def rgb_to_cielab(image):
    """
    Converts an RGB image array to CIELAB.
    """
    cielab_array = skimage.color.rgb2lab(np.array(image))
    return cielab_array
