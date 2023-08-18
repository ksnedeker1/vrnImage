import numpy as np
import cv2


def voronoi_average_color_by_cell(img, vor):
    """
    Find average color of pixels in each Voronoi cell in CIELAB space.
    :param img: RGB image to be processed.
    :param vor: scipy.spatial.Voronoi(sampled coords)
    :returns: List of average colors for coordinate, associated by order with vor.
    """
    rows, cols = img.shape[:2]
    region_membership = np.zeros((rows, cols), dtype=np.int32)
    # Iterate through valid regions
    for idx, region in enumerate(vor.regions):
        if -1 not in region and len(region) > 1:
            # Define the polygon and clamp vertices to image bounds
            polygon = np.array([vor.vertices[i] for i in region], dtype=np.int32)
            polygon[:, 0] = np.clip(polygon[:, 0], 0, cols - 1)
            polygon[:, 1] = np.clip(polygon[:, 1], 0, rows - 1)
            try:
                # Fill pixels in the current polygon (region) with the value of idx
                cv2.fillPoly(region_membership, [polygon.reshape((-1, 1, 2))], idx)
            except Exception as e:
                print(f"Exception in region {idx}: {e}")
                print("With vertices:", polygon)
    # Lists to store color val accumulators and counts.
    color_sums = np.zeros((len(vor.points)+1, 3))
    counts = np.zeros((len(vor.points)+1,))
    # Iterate through all pixels. For each coordinate, take its value in region_membership defining
    # the idx of the cell it belongs too. Add this pixel's color to that idx of color_sums
    # and increment that idx of counts. This is the reduction of img to averages using
    # region_membership as a map of pixels to Voronoi cells.
    for i in range(rows):
        for j in range(cols):
            idx = region_membership[i, j]
            color_sums[idx] += img[i, j]
            counts[idx] += 1
    # Use the color value accumulator and counts to find averages for each region.
    averages = [(color_sum / count).astype(np.uint8) if count != 0
                else np.zeros(3) for color_sum, count in zip(color_sums, counts)]
    return averages


def reconstruct_image(vor, averages, img_shape):
    """
    Reconstruct vrn image using average colors and coords of Voronoi cells.
    :param vor: scipy.spatial.Voronoi(sampled coords)
    :param averages: List of average colors for coordinate, associated by order with vor.
    :param img_shape: Shape of the original image (height, width, channels).
    :returns: Reconstructed image as np.array.
    """
    reconstructed = np.zeros(img_shape, dtype=np.uint8)
    rows, cols = img_shape[:2]
    # Iterate through valid regions
    for idx, region in enumerate(vor.regions):
        if -1 not in region and len(region) > 1:
            # Define the polygon and clamp vertices to image bounds
            polygon = np.array([vor.vertices[i] for i in region], dtype=np.int32)
            polygon[:, 0] = np.clip(polygon[:, 0], 0, cols - 1)
            polygon[:, 1] = np.clip(polygon[:, 1], 0, rows - 1)
            # Extract average RGB color
            avg_color_rgb = averages[idx].astype(np.uint8)
            # Fill pixels in the current polygon (region) with RGB average extracted from averages[idx]
            cv2.fillPoly(reconstructed, [polygon.reshape((-1, 1, 2))], color=(int(avg_color_rgb[0]), int(avg_color_rgb[1]), int(avg_color_rgb[2])))
    return reconstructed
