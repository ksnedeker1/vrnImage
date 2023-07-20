import matplotlib.pyplot as plt
from matplotlib import gridspec

from src.processing.edgedetection import SobelEdgeDetection
from src.utils.imageformat import rgb_to_cielab
from src.utils.fileio import import_image


img_rgb = import_image('../images/genart1.png')
img = rgb_to_cielab(img_rgb)

det = SobelEdgeDetection()
(grads, combined), time = det.run(img)


def display_images(original, gradients, combined):
    fig = plt.figure(figsize=(15, 10))
    gs = gridspec.GridSpec(2, 3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    ax5 = fig.add_subplot(gs[1, 2])
    ax1.imshow(original)
    ax1.set_title("Original")
    ax1.axis("off")
    ax2.imshow(combined, cmap='gray')
    ax2.set_title("Combined")
    ax2.axis("off")
    ax3.imshow(gradients[0], cmap='gray')
    ax3.set_title("Gradient L*")
    ax3.axis("off")
    ax4.imshow(gradients[1], cmap='gray')
    ax4.set_title("Gradient A*")
    ax4.axis("off")
    ax5.imshow(gradients[2], cmap='gray')
    ax5.set_title("Gradient B*")
    ax5.axis("off")
    plt.tight_layout()
    plt.show()


print(time)
display_images(img_rgb, grads, combined)
