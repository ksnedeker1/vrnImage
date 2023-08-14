import os
import cv2


def array_to_image(img_array, path='./', filename='result_tmp.jpg'):
    """Saves an array of RGB values as an image at 'path' with 'filename' (incl. extension)."""
    cv2.imwrite(os.path.join(path, filename), cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))
