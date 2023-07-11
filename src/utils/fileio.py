import os
import numpy as np
import skimage.color
from PIL import Image


class ImagePathError(Exception):
    def __init__(self, path):
        self.path = str(path)

    def __str__(self):
        return f'Path does not exist or is invalid: {type(self.path)} {self.path} '


def import_image(path: str, split: bool = False):
    """
    Imports the image file at the specified path. Supports most common file types.
    :param path: relative or absolute path to the file
    :param split: whether output splits luminance and color channels or not
    :return: numpy array containing CIELAB values representing the imported image
    """
    # Ensure path is a string which is valid and exists
    if not type(path) == str or not os.path.isfile(path):
        raise ImagePathError(path)
    # Open image with PIL
    image = Image.open(path)
    # Convert to np.array of image converted to CIELAB color space
    cielab_array = skimage.color.rgb2lab(np.array(image))
    return (cielab_array[:, :, 0], cielab_array[:, :, 1:]) if split else cielab_array
