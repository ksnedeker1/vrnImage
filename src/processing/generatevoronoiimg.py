import cv2
import numpy as np


def generate_voronoi_img(shape, vor):
    """
    Create a representation of the Voronoi diagram with color bins corresponding to cell size quartiles.
    """
    # Approximate all areas, find 25th, 50th, 75th percentile values
    areas = [shoelace([vor.vertices[i] for i in cell]) if -1 not in cell else 0 for cell in vor.regions]
    q25, q50, q75 = np.percentile(areas, [25, 50, 75])
    # For each bounded cell, draw the edges of the polygon defined by the vertices of that cell
    output = np.zeros(shape, dtype=np.uint8)
    for index, cell in enumerate(vor.regions):
        if -1 not in cell:
            polygon = [vor.vertices[i] for i in cell]
            if polygon:
                # Color scheme dependent on size class of cell
                if areas[index] < q25:
                    color = (np.random.randint(127, 255), 0, np.random.randint(127, 255))
                elif areas[index] < q50:
                    color = (np.random.randint(127, 255), np.random.randint(127, 255), 0)
                elif areas[index] < q75:
                    color = (0, np.random.randint(127, 255), np.random.randint(127, 255))
                else:
                    val = np.random.randint(0, 127)
                    color = (val, val, val)
                polygon_reshaped = np.array(polygon, np.int32)
                cv2.fillPoly(output, [polygon_reshaped], color)
    return output


def shoelace(polygon):
    """
    Quick shoelace approximation
    """
    x = [p[0] for p in polygon]
    y = [p[1] for p in polygon]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
