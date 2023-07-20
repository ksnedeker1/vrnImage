import numpy as np
import cv2
from src.utils.timer import timer


class SobelEdgeDetection:
    """
    Sobel edge detection using open-cv.
    TODO: add channel weights for Sobel edge detection
    """
    def __init__(self, ksize=3, scale=3.5, delta=0, ddepth=cv2.CV_16S):
        self.ksize = ksize
        self.scale = scale
        self.delta = delta
        self.ddepth = ddepth

    @timer
    def run(self, cielab_img):
        """
        Run Sobel edge detection on all channels (L*, A*, B*) before combining the results.
        Functional structure informed by 'Sobel Derivatives' tutorial from OpenCV's documentation.
        """
        channels = cv2.split(cielab_img)
        grads = []
        for chan in channels:
            grad_x = cv2.Sobel(chan, self.ddepth, 1, 0, ksize=self.ksize,
                               scale=self.scale, borderType=cv2.BORDER_DEFAULT)
            grad_y = cv2.Sobel(chan, self.ddepth, 0, 1, ksize=self.ksize,
                               scale=self.scale, borderType=cv2.BORDER_DEFAULT)
            grad_x = cv2.convertScaleAbs(grad_x)
            grad_y = cv2.convertScaleAbs(grad_y)
            grad = cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0)
            grads.append(grad)
        combined = np.maximum.reduce(grads)
        return grads, combined
