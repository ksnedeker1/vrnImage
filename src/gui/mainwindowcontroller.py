from PyQt5 import QtWidgets, QtCore, QtGui
import os.path
import numpy as np

from src.gui.mainwindow import Ui_MainWindow
from src.gui.resources.htmlstrings import *
from src.gui.resources.statusbarmessages import *
from src.utils.fileio import import_image, array_to_image
from src.utils.imageformat import rgb_to_cielab
from src.processing.demonstrationworker import DemonstrationWorker
from src.compression.compressionparams import CompressionParams
from src.compression.compressionworker import CompressionWorker
from src.metrics.requester import call_metrics_microservice


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    cw_set_params = QtCore.pyqtSignal(object, object, object)
    dw_set_shape = QtCore.pyqtSignal(object)
    dw_on_heatmap_ready = QtCore.pyqtSignal(object)
    dw_on_coords_ready = QtCore.pyqtSignal(object)
    dw_on_voronoi_ready = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(MainWindowController, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.init_element_states()
        self.init_clickable_elements_general()
        self.init_process_state()
        self.init_demonstrative_elements()
        self.init_compression_worker()
        self.init_demonstration_worker()

    def init_element_states(self):
        """
        Sets default states and contents of various elements.
        """
        self.setWindowIcon(QtGui.QIcon('./src/gui/resources/icon.svg'))
        # Set stylesheet
        stylesheet = "./src/gui/resources/stylesheet.qss"
        with open(stylesheet, "r") as f:
            self.setStyleSheet(f.read())
        # Set default "Generate Demonstrative Elements" checkbox state
        self.toggleDemonstrativeElements.setChecked(True)
        # Set initial textDisplay contents and state
        self.textDisplay.setHtml(td_welcome)
        self.textDisplay.setReadOnly(True)
        # Set default visibility of parameters and metrics
        self.samplesLabel.setVisible(False)
        self.samplesValue.setVisible(False)
        self.edgeStrengthLabel.setVisible(False)
        self.edgeStrengthValue.setVisible(False)
        self.colorSalienceLabel.setVisible(False)
        self.colorSalienceValue.setVisible(False)
        self.samplingLinearityLabel.setVisible(False)
        self.samplingLinearityValue.setVisible(False)
        self.seedLabel.setVisible(False)
        self.seedValue.setVisible(False)
        self.toggleDemonstrativeElements.setVisible(False)
        self.mCompressionRatioLabel.setVisible(False)
        self.mCompressionRatioValue.setVisible(False)
        self.mProcessTimeLabel.setVisible(False)
        self.mProcessTimeValue.setVisible(False)
        self.mSSIMLabel.setVisible(False)
        self.mSSIMValue.setVisible(False)
        self.mMSELabel.setVisible(False)
        self.mMSEValue.setVisible(False)
        self.mPMSELabel.setVisible(False)
        self.mPMSEValue.setVisible(False)
        self.mSNRLabel.setVisible(False)
        self.mSNRValue.setVisible(False)
        self.mPSNRLabel.setVisible(False)
        self.mPSNRValue.setVisible(False)
        self.line_7.setVisible(False)
        # Set validators and default values for parameter entry QLineEdits
        self.paramInputs = [self.samplesValue, self.edgeStrengthValue, self.colorSalienceValue,
                            self.samplingLinearityValue, self.seedValue]
        for widget in self.paramInputs[:-1]:
            widget.setValidator(QtGui.QDoubleValidator(0.0, 1.0, 2))
            widget.setText('1.0')
        self.samplesValue.setValidator(QtGui.QDoubleValidator(3, 1000000, 0))
        self.samplesValue.setText('100000')
        self.samplingLinearityValue.setValidator(QtGui.QDoubleValidator(0.01, 10.0, 2))
        self.samplingLinearityValue.setText('1.0')
        self.seedValue.setValidator(QtGui.QDoubleValidator(0, 999999999, 0))
        self.seedValue.setText(str(np.random.randint(0, 9999)))

    def init_clickable_elements_general(self):
        """
        Initialize general purpose clickable GUI elements.
        """
        # Section show/hide buttons
        self.showGeneralSettings.clicked.connect(self.on_click_section_toggle)
        self.showAdvancedSettings.clicked.connect(self.on_click_section_toggle)
        self.showGeneralMetrics.clicked.connect(self.on_click_section_toggle)
        self.showAdvancedMetrics.clicked.connect(self.on_click_section_toggle)
        # Image selection button
        self.selectImage.clicked.connect(self.show_select_image_menu)
        # Process control
        self.processToggle.clicked.connect(self.process_toggle_handler)
        # Text display
        self.textDisplayNext.clicked.connect(self.next_text_display)
        self.textDisplayPrev.clicked.connect(self.prev_text_display)

    def init_process_state(self):
        """
        Initialize compression process state.
        """
        self.processActive = False
        # Compression items and paths
        self.currDir = os.path.dirname(os.path.abspath(__file__))
        self.activeImagePath = None
        self.activeImageRGB = None
        self.activeImageCIELAB = None
        self.activeImageHeatmap = None
        self.activeImageCoords = None
        self.activeImageVoronoi = None
        self.activeImageAvgColors = None
        self.activeImageReconstructed = None
        self.activeImageReconstructedDir = os.path.abspath(os.path.join(self.currDir, '..', '..', 'images', 'results'))
        self.activeImageReconstructedFileName = 'result_tmp.jpg'
        if not os.path.isdir(self.activeImageReconstructedDir):
            os.mkdir(self.activeImageReconstructedDir)
        # Initialize CompressionParams object
        self.currParams = CompressionParams(*[None for _ in self.paramInputs])

    def init_demonstrative_elements(self):
        """
        Initialize demonstrative GUI elements.
        """
        self.demonstrative = True
        self.processStepsGenerated = False
        self.viewSelectorPathDict = {self.viewSelector.itemText(i): None for i in range(self.viewSelector.count())}
        self.viewSelector.currentIndexChanged.connect(self.update_graphics_view)
        self.toggleDemonstrativeElements.stateChanged.connect(self.toggle_demonstrative_element_generation)
        self.currentText = 0
        self.textDisplayList = [(td_original_image, 0), (td_heatmap, 2), (td_sampled_points, 3),
                                (td_voronoi_diagram, 4), (td_compressed_image, 1)]

    def init_metrics_display(self):
        """
        Initialize metrics text.
        """
        self.mProcessTimeValue.setText('Waiting...')
        self.mCompressionRatioValue.setText('Waiting...')
        self.mMSEValue.setText('Waiting...')
        self.mPSNRValue.setText('Waiting...')
        self.mSNRValue.setText('Waiting...')
        self.mPMSEValue.setText('Waiting...')
        self.mSSIMValue.setText('Waiting...')

    def init_compression_worker(self):
        """
        Initialize CompressionWorker(QThread) object and connect request/response signals.
        """
        self.compression_worker = CompressionWorker()
        # Request signal
        self.cw_set_params.connect(self.compression_worker.set_params)
        # Response signals
        self.compression_worker.heatmap_ready.connect(self.on_heatmap_ready)
        self.compression_worker.coords_ready.connect(self.on_coords_ready)
        self.compression_worker.voronoi_ready.connect(self.on_voronoi_ready)
        self.compression_worker.compression_done.connect(self.on_compression_done)
        self.compression_worker.image_reconstructed.connect(self.on_image_reconstructed)

    def init_demonstration_worker(self):
        """
        Initialize DemonstrationWorker(QThread) object and connect request/response signals.
        """
        self.demonstration_worker = DemonstrationWorker()
        # Request signals
        self.dw_set_shape.connect(self.demonstration_worker.set_image_shape)
        self.dw_on_heatmap_ready.connect(self.demonstration_worker.handle_heatmap)
        self.dw_on_coords_ready.connect(self.demonstration_worker.handle_coords)
        self.dw_on_voronoi_ready.connect(self.demonstration_worker.handle_voronoi)
        # Response signals
        self.demonstration_worker.heatmap_converted.connect(self.on_heatmap_converted)
        self.demonstration_worker.coords_converted.connect(self.on_coords_converted)
        self.demonstration_worker.voronoi_converted.connect(self.on_voronoi_converted)

    def on_click_section_toggle(self):
        """
        Toggles visibility of a section of UI elements based on the signal sender (button object).
        """
        # Get calling object
        obj = self.sender()
        # Toggle General Settings section
        if obj is self.showGeneralSettings:
            button_text = self.showGeneralSettings.text()
            self.showGeneralSettings.setText(('Hide' if button_text[:4] == 'Show' else 'Show') + button_text[4:])
            self.samplesLabel.setVisible(not self.samplesLabel.isVisible())
            self.samplesValue.setVisible(not self.samplesValue.isVisible())
            self.samplingLinearityLabel.setVisible(not self.samplingLinearityLabel.isVisible())
            self.samplingLinearityValue.setVisible(not self.samplingLinearityValue.isVisible())
            self.edgeStrengthLabel.setVisible(not self.edgeStrengthLabel.isVisible())
            self.edgeStrengthValue.setVisible(not self.edgeStrengthValue.isVisible())
        # Toggle Advanced Settings section
        elif obj is self.showAdvancedSettings:
            button_text = self.showAdvancedSettings.text()
            self.showAdvancedSettings.setText(('Hide' if button_text[:4] == 'Show' else 'Show') + button_text[4:])
            self.colorSalienceLabel.setVisible(not self.colorSalienceLabel.isVisible())
            self.colorSalienceValue.setVisible(not self.colorSalienceValue.isVisible())
            self.seedLabel.setVisible(not self.seedLabel.isVisible())
            self.seedValue.setVisible(not self.seedValue.isVisible())
            self.toggleDemonstrativeElements.setVisible(not self.toggleDemonstrativeElements.isVisible())
        # Toggle General Metrics section
        elif obj is self.showGeneralMetrics:
            button_text = self.showGeneralMetrics.text()
            self.showGeneralMetrics.setText(('Hide' if button_text[:4] == 'Show' else 'Show') + button_text[4:])
            self.mCompressionRatioLabel.setVisible(not self.mCompressionRatioLabel.isVisible())
            self.mCompressionRatioValue.setVisible(not self.mCompressionRatioValue.isVisible())
            self.mProcessTimeLabel.setVisible(not self.mProcessTimeLabel.isVisible())
            self.mProcessTimeValue.setVisible(not self.mProcessTimeValue.isVisible())
            self.mSSIMLabel.setVisible(not self.mSSIMLabel.isVisible())
            self.mSSIMValue.setVisible(not self.mSSIMValue.isVisible())
        # Toggle Advanced Metrics section
        elif obj is self.showAdvancedMetrics:
            button_text = self.showAdvancedMetrics.text()
            self.showAdvancedMetrics.setText(('Hide' if button_text[:4] == 'Show' else 'Show') + button_text[4:])
            self.mMSELabel.setVisible(not self.mMSELabel.isVisible())
            self.mMSEValue.setVisible(not self.mMSEValue.isVisible())
            self.mPMSELabel.setVisible(not self.mPMSELabel.isVisible())
            self.mPMSEValue.setVisible(not self.mPMSEValue.isVisible())
            self.mSNRLabel.setVisible(not self.mSNRLabel.isVisible())
            self.mSNRValue.setVisible(not self.mSNRValue.isVisible())
            self.mPSNRLabel.setVisible(not self.mPSNRLabel.isVisible())
            self.mPSNRValue.setVisible(not self.mPSNRValue.isVisible())
            self.line_7.setVisible(not self.line_7.isVisible())

    def toggle_demonstrative_element_generation(self, state):
        """
        Toggle whether demonstrative elements will be generated and/or displayed hereafter.
        """
        if state == QtCore.Qt.Checked:
            self.demonstrative = True
            self.textDisplay.setHtml(td_welcome)
        else:
            self.demonstrative = False
            self.clear_td()

    def next_text_display(self):
        """
        Handle display of 'next' text display item.
        """
        if self.processStepsGenerated:
            self.currentText += 1
            self.currentText %= len(self.textDisplayList)
            self.update_text_display()

    def prev_text_display(self):
        """
        Handle display of 'prev' text display item.
        """
        if self.processStepsGenerated:
            self.currentText -= 1
            self.currentText %= len(self.textDisplayList)
            self.update_text_display()

    def update_text_display(self):
        """
        Display the HTML text string at the current index and update the graphics
        view to match the description being shown.
        """
        if self.processStepsGenerated:
            item = self.textDisplayList[self.currentText]
            self.textDisplay.setHtml(item[0])
            self.viewSelector.setCurrentIndex(item[1])
            self.update_graphics_view()

    def show_select_image_menu(self):
        """
        Secondary selection for 'Select Image'. User can choose images included with the application, or from their
        computer.
        """
        menu = QtWidgets.QMenu(self)
        option1 = QtWidgets.QAction('Choose from examples', self)
        option2 = QtWidgets.QAction('Choose my own', self)
        option1.triggered.connect(self.choose_included_image)
        option2.triggered.connect(self.choose_image_on_disk)
        menu.addAction(option1)
        menu.addAction(option2)
        # Position selection menu below 'Select Image' button
        button_geometry = self.selectImage.geometry()
        global_button_position = self.selectImage.mapToGlobal(QtCore.QPoint(0, button_geometry.height()))
        menu.exec_(global_button_position)

    def update_graphics_view(self):
        """
        Updates the contents of the QGraphicsView to the current selection of viewSelector.
        """
        current_text = self.viewSelector.currentText()
        selected_image = self.viewSelectorPathDict.get(current_text, None)
        # Handle selections with no associated image
        if selected_image is None:
            if self.viewGraphics.scene():
                self.viewGraphics.scene().clear()
            return
        h, w, _ = selected_image.shape
        bytes_per = 3 * w
        q_img = QtGui.QImage(selected_image.data, w, h, bytes_per, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        # Create a QGraphicsScene, add QGraphicsPixmapItem
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(pixmap_item)
        # Set scene in the QGraphicsView and scale
        self.viewGraphics.setScene(scene)
        self.viewGraphics.fitInView(pixmap_item, mode=QtCore.Qt.KeepAspectRatio)

    def choose_included_image(self):
        """
        Creates and displays a dialog for the user to select an image included with the application.
        Loads the image on selection.
        """
        # Create dialog and list widget
        images_dialog = QtWidgets.QDialog(self)
        images_dialog.setWindowTitle("Select an example image")
        images_dialog.resize(400, 300)
        layout = QtWidgets.QVBoxLayout(images_dialog)
        list_widget = QtWidgets.QListWidget(images_dialog)
        layout.addWidget(list_widget)
        # Read filenames in images dir and add them to the QList
        image_directory = "images"
        image_files = os.listdir(image_directory)
        for name in image_files:
            item = QtWidgets.QListWidgetItem(name)
            list_widget.addItem(item)
        load_button = QtWidgets.QPushButton("Load", images_dialog)
        layout.addWidget(load_button)
        load_button.clicked.connect(images_dialog.accept)
        # Show the dialog and wait for the user to press the button
        if images_dialog.exec() == QtWidgets.QDialog.Accepted:
            selection = list_widget.currentItem()
            # Load image on button click
            if selection:
                file_name = selection.text()
                self.activeImagePath = os.path.join(self.currDir, '../../images', file_name)
                self.activeImageRGB = import_image(self.activeImagePath)
                self.activeImageCIELAB = rgb_to_cielab(self.activeImageRGB)
                self.viewSelectorPathDict['Original Image'] = self.activeImageRGB
                self.load_image(0)

    def choose_image_on_disk(self):
        """
        Launch a file dialog to allow the user to select and image file from their machine.
        """
        # Start the file dialog at the user's home directory, store the path this dialog returns
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose image file...", os.path.expanduser("~"))
        if file_name:
            self.activeImagePath = file_name
            self.activeImageRGB = import_image(self.activeImagePath)
            self.activeImageCIELAB = rgb_to_cielab(self.activeImageRGB)
            self.viewSelectorPathDict['Original Image'] = self.activeImageRGB
            self.load_image(0)

    def load_image(self, idx):
        """
        Load the image at path activeImagePath and show it as a preview in the graphics view.
        """
        old_idx = self.viewSelector.currentIndex()
        self.viewSelector.setCurrentIndex(idx)
        if old_idx == idx:
            self.update_graphics_view()
            self.statusbar.showMessage(*sb_image_loaded)
        if self.demonstrative:
            pass
            # TODO: add HTML for load message/info

    def process_toggle_handler(self):
        """
        Switch process to opposite current state and call appropriate method.
        """
        # Handle process termination
        if self.processActive:
            self.processActive = False
            self.processToggle.setText('Start')
            self.statusbar.showMessage(*sb_stop_process)
        # Handle process initiation
        else:
            # Check a path was actually selected before the user exited the dialog
            if self.activeImagePath is None:
                self.statusbar.showMessage(*sb_no_image_selected)
                return
            # Abort start if any parameters are invalid and highlight them
            invalid_input = False
            for widget in self.paramInputs:
                if not widget.hasAcceptableInput():
                    invalid_input = True
                    widget.setStyleSheet("border: 1px solid #F83934;")
                else:
                    widget.setStyleSheet("")
            if invalid_input:
                self.statusbar.showMessage(*sb_invalid_parameters)
                return
            # Else, start process with current parameters
            try:
                params = CompressionParams(
                    int(self.samplesValue.text()),
                    float(self.edgeStrengthValue.text()),
                    float(self.colorSalienceValue.text()),
                    float(self.samplingLinearityValue.text()),
                    int(self.seedValue.text())
                )
                self.currParams = params
            except ValueError:
                self.statusbar.showMessage(*sb_invalid_parameters)
                return
            # Update GUI elements and call start_process()
            self.processActive = True
            self.processStepsGenerated = False
            self.processToggle.setText('Stop')
            self.start_process(params)

    def start_process(self, params: CompressionParams):
        """
        Start compression thread and connect signals.
        """
        self.init_metrics_display()
        self.textDisplay.setHtml(td_process_running)
        self.statusbar.showMessage(
            sb_process_status.format(image=self.activeImagePath.replace('\\', '/').split('/')[-1],
                                     samples=self.currParams.samples, linearity=self.currParams.sampling_linearity,
                                     task=sb_task_heatmap))
        # Send CompressionWorker current images and params
        self.cw_set_params.emit(self.activeImageRGB, self.activeImageCIELAB, params)
        self.compression_worker.start()
        # Send DemonstrationWorker current img shape
        self.dw_set_shape.emit(self.activeImageRGB.shape)
        self.demonstration_worker.start()

    def on_heatmap_ready(self, heatmap):
        """
        Handle heatmap_ready signal
        """
        if self.processActive:
            self.dw_on_heatmap_ready.emit(heatmap)
            self.statusbar.showMessage(
                sb_process_status.format(image=self.activeImagePath.replace('\\', '/').split('/')[-1],
                                         samples=self.currParams.samples, linearity=self.currParams.sampling_linearity,
                                         task=sb_task_coords))

    def on_coords_ready(self, coords):
        """
        Handle coords_ready signal
        """
        if self.processActive:
            self.dw_on_coords_ready.emit(coords)
            self.statusbar.showMessage(
                sb_process_status.format(image=self.activeImagePath.replace('\\', '/').split('/')[-1],
                                         samples=self.currParams.samples, linearity=self.currParams.sampling_linearity,
                                         task=sb_task_voronoi))

    def on_voronoi_ready(self, voronoi):
        """
        Handle voronoi_ready signal
        """
        if self.processActive:
            self.dw_on_voronoi_ready.emit(voronoi)
            self.statusbar.showMessage(
                sb_process_status.format(image=self.activeImagePath.replace('\\', '/').split('/')[-1],
                                         samples=self.currParams.samples, linearity=self.currParams.sampling_linearity,
                                         task=sb_task_compressed))

    def on_compression_done(self, compressed_size, duration):
        """
        Handle compression_done signal
        """
        if self.processActive:
            orig_size = len(self.activeImageRGB) * len(self.activeImageRGB[0]) * len(self.activeImageRGB[0][0])
            size_diff = orig_size - compressed_size
            size_percent = 100 * compressed_size / orig_size
            self.update_metrics(size_diff=size_diff, size_percent=size_percent,
                                compressed_size=compressed_size, duration=duration)
            self.statusbar.showMessage(
                sb_process_status.format(image=self.activeImagePath.replace('\\', '/').split('/')[-1],
                                         samples=self.currParams.samples, linearity=self.currParams.sampling_linearity,
                                         task=sb_task_reconstruct))

    def on_image_reconstructed(self, image):
        """
        Handle image_reconstructed signal, update GUI (process finished).
        """
        if self.processActive:
            self.activeImageReconstructed = image
            # Store in format compatible with microservice
            array_to_image(self.activeImageReconstructed, self.activeImageReconstructedDir,
                           self.activeImageReconstructedFileName)
            # Request metrics for the compression operation
            image_path1 = os.path.join(self.activeImagePath)
            image_path2 = os.path.join(self.activeImageReconstructedDir, self.activeImageReconstructedFileName)
            result = call_metrics_microservice(image_path1, image_path2)
            _, _, mse, psnr = result.split(',')
            # Update GUI elements
            self.update_metrics(mse=mse, psnr=psnr)
            # Reconsider approach to viewSelectorPathDict initialization
            self.viewSelectorPathDict['Compressed Image'] = self.activeImageReconstructed
            self.viewSelector.setCurrentIndex(1)
            self.processActive = False
            self.processToggle.setText('Start')
            self.update_graphics_view()
            self.statusbar.showMessage(*sb_process_complete)
            self.processStepsGenerated = True
            self.currentText = 4
            self.update_text_display()

    def on_heatmap_converted(self, heatmap_img):
        """
        Display generated heatmap.
        """
        if self.processActive:
            self.viewSelectorPathDict['Heatmap'] = heatmap_img
            self.load_image(2)

    def on_coords_converted(self, coords_img):
        """
        Display sampled coords.
        """
        if self.processActive:
            self.viewSelectorPathDict['Sampled Points'] = coords_img
            self.load_image(3)

    def on_voronoi_converted(self, voronoi_img):
        """
        Display generated Voronoi diagram.
        """
        if self.processActive:
            self.viewSelectorPathDict['Voronoi Diagram'] = voronoi_img
            self.load_image(4)

    def update_metrics(self, mse=None, psnr=None, size_diff=None, size_percent=None,
                       compressed_size=None, duration=None):
        """
        Update value labels for metrics display in GUI.
        """
        if mse is not None:
            mse = str(round(float(mse), 2))
            self.mMSEValue.setText(mse)
        if psnr is not None:
            psnr = str(round(float(psnr), 2))
            self.mPSNRValue.setText(psnr)
        if None not in (size_diff, size_percent, compressed_size):
            sign = '+' if size_percent > 100 else ''
            self.mCompressionRatioValue.setText(f'{size_percent:.2f}%, {sign}{-size_diff/1000000:.2f}MB, '
                                                f'{compressed_size/1000000:.2f}MB')
        if duration is not None:
            self.mProcessTimeValue.setText(f'{duration:.2f}s')

    def clear_td(self):
        """
        Clears text display area.
        """
        self.textDisplay.setHtml('')


def start_gui():
    app = QtWidgets.QApplication([])
    window = MainWindowController()
    window.show()
    app.exec_()
