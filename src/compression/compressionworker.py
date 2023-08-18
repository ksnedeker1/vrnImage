from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from scipy.spatial import Voronoi
from timeit import default_timer

from src.processing.edgedetection import SobelEdgeDetection
from src.processing.pointsampling import sample_coordinates
from src.processing.voronoiaveraging import voronoi_average_color_by_cell, reconstruct_image
from src.compression.vrnfilehandler import vrn_compress


class CompressionWorker(QThread):
    """QThread process for handling image compression."""
    heatmap_ready = pyqtSignal(object)
    coords_ready = pyqtSignal(object)
    voronoi_ready = pyqtSignal(object)
    compression_done = pyqtSignal(object, object)
    image_reconstructed = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.activeImageRGB = None
        self.activeImageCIELAB = None
        self.sampleSize = None
        self.linearityPower = None
        self.seed = None

    @pyqtSlot(object, object, object)
    def set_params(self, img_RGB, img_CIELAB, params):
        """
        Load parameters for compression process
        """
        self.activeImageRGB = img_RGB
        self.activeImageCIELAB = img_CIELAB
        self.sampleSize = params.samples
        self.linearityPower = params.sampling_linearity
        self.seed = params.seed

    def run(self):
        """
        Start compression process. Send signals at various stages of completion.
        """
        start = default_timer()
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
        compressed_size = vrn_compress(self.activeImageRGB, active_image_voronoi, active_image_avg_colors,
                                       'compressed_image', directory='./')
        duration = default_timer() - start
        self.compression_done.emit(compressed_size, duration)
        # Reconstruct image
        active_image_reconstructed = reconstruct_image(active_image_voronoi, active_image_avg_colors,
                                                     self.activeImageRGB.shape)
        self.image_reconstructed.emit(active_image_reconstructed)
