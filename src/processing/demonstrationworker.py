from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

from src.processing.generatecoordsimg import generate_coords_img
from src.processing.generateheatmapimg import generate_heatmap_img
from src.processing.generatevoronoiimg import generate_voronoi_img


class DemonstrationWorker(QThread):
    """
    QThread process for generating demonstrative elements representing
    stages of the compression process.
    """
    heatmap_converted = pyqtSignal(object)
    coords_converted = pyqtSignal(object)
    voronoi_converted = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.image_shape = None

    @pyqtSlot(object)
    def set_image_shape(self, shape):
        self.image_shape = shape

    @pyqtSlot(object)
    def handle_heatmap(self, data):
        self.heatmap_converted.emit(generate_heatmap_img(data))

    @pyqtSlot(object)
    def handle_coords(self, data):
        self.coords_converted.emit(generate_coords_img(self.image_shape, data))

    @pyqtSlot(object)
    def handle_voronoi(self, data):
        self.voronoi_converted.emit(generate_voronoi_img(self.image_shape, data))
