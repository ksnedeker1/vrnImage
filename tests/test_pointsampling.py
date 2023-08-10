import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import cv2

from src.utils.imageformat import rgb_to_cielab
from src.utils.fileio import import_image
from src.processing.edgedetection import SobelEdgeDetection
from src.processing.pointsampling import sample_coordinates


img_rgb = import_image('../images/ireland1.jpg')
print(img_rgb)
print(len(img_rgb), len(img_rgb[0]))
img = rgb_to_cielab(img_rgb)

det = SobelEdgeDetection()
(grads, combined), time = det.run(img)

coords = sample_coordinates(combined, 50000)
sampled_img = np.zeros_like(img_rgb)

# set sampled coords to white
for coord in coords:
    sampled_img[coord[0], coord[1]] = [255, 255, 255]

fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

# Orig
ax0 = plt.subplot(gs[0])
ax0.imshow(cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB))
ax0.axis('off')
ax0.set_title('Original Image')

# Sampled points
ax1 = plt.subplot(gs[1])
ax1.imshow(cv2.cvtColor(sampled_img, cv2.COLOR_BGR2RGB))
ax1.axis('off')
ax1.set_title('Sampled Points')

plt.tight_layout()
plt.show()
