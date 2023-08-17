import cv2
import numpy as np


def generate_voronoi_img(shape, vor):
    """
    Create an array representing an RGB image edges of Voronoi cells colored white.
    """
    output = np.zeros(shape, dtype=np.uint8)
    # For each bounded cell, draw the edges of the polygon defined by the vertices of that cell
    for cell in vor.regions:
        if -1 not in cell:
            polygon = [vor.vertices[i] for i in cell]
            if polygon:
                polygon_reshaped = np.array(polygon, np.int32)
                color = (np.random.randint(0, 255), 255, np.random.randint(0, 255))
                cv2.fillPoly(output, [polygon_reshaped], color)
    return output
