import os
import cv2
import numpy as np
from PIL import Image


class ImagePathError(Exception):
    def __init__(self, path):
        self.path = str(path)

    def __str__(self):
        return f'Path does not exist or is invalid: {type(self.path)} {self.path} '


def import_image(path: str):
    """
    Imports the image file at the specified path. Supports most common file types.
    :param path: relative or absolute path to the file
    :param split: whether output splits luminance and color channels or not
    :return: numpy array containing RGB values representing the imported image
    """
    # Ensure path is a string which is valid and exists
    if not type(path) == str or not os.path.isfile(path):
        raise ImagePathError(path)
    # Open image with PIL
    image = Image.open(path)
    image_rgb = image.convert('RGB')
    # Remove alpha channel if png
    # TODO: handle png alpha channel
    return np.array(image_rgb)


def array_to_image(img_array, path='./images/results', filename='result_tmp.jpg'):
    """Saves an array of RGB values as an image at 'path' with 'filename' (incl. extension)."""
    cv2.imwrite(os.path.join(path, filename), cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))
