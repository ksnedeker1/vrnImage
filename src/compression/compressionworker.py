from PyQt5.QtCore import QThread, pyqtSignal
from scipy.spatial import Voronoi

from src.processing.edgedetection import SobelEdgeDetection
from src.processing.pointsampling import sample_coordinates
from src.processing.voronoiaveraging import voronoi_average_color_by_cell, reconstruct_image
from src.compression.vrnfilehandler import vrn_compress


class CompressionWorker(QThread):
    heatmap_ready = pyqtSignal(object)
    coords_ready = pyqtSignal(object)
    voronoi_ready = pyqtSignal(object)
    image_reconstructed = pyqtSignal(object)

    def __init__(self, active_image_RGB, active_image_CIELAB, sample_size, linearity_power, seed):
        super().__init__()
        self.activeImageRGB = active_image_RGB
        self.activeImageCIELAB = active_image_CIELAB
        self.sampleSize = sample_size
        self.linearityPower = linearity_power
        self.seed = seed

    def run(self):
        # Gather heatmap
        det = SobelEdgeDetection()
        (_, activeImageHeatmap), time = det.run(self.activeImageCIELAB)
        self.heatmap_ready.emit(activeImageHeatmap)
        # Sample coords from heatmap
        active_image_coords = sample_coordinates(activeImageHeatmap, self.sampleSize,
                                               linearity_power=self.linearityPower, seed=self.seed)
        self.coords_ready.emit(active_image_coords)
        # Get Voronoi diagram
        active_image_voronoi = Voronoi(active_image_coords)
        self.voronoi_ready.emit(active_image_voronoi)
        active_image_avg_colors = voronoi_average_color_by_cell(self.activeImageRGB, active_image_voronoi)
        # Store compressed image
        vrn_compress(self.activeImageRGB, active_image_voronoi, active_image_avg_colors,
                     'compressed_image', directory='./')
        # Reconstruct image
        active_image_reconstructed = reconstruct_image(active_image_voronoi, active_image_avg_colors,
                                                     self.activeImageRGB.shape)
        self.image_reconstructed.emit(active_image_reconstructed)
