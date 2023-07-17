from PyQt5 import QtWidgets, QtCore, QtGui
import os.path
from src.gui.mainwindow import Ui_MainWindow
from src.gui.resources.htmlstrings import *
from src.gui.resources.statusbarmessages import *
from src.utils.fileio import import_image
from src.compression.compressionparams import CompressionParams
# from src.process.image_formatting import rgb_to_cielab


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowController, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./src/resources/icon.svg'))

        self.paramInputs = [self.compressionLevelValue, self.edgeStrengthValue, self.colorSalienceValue,
                            self.samplingUniformityValue, self.seedValue]

        self.init_element_states()

        # Section show/hide buttons
        self.showGeneralSettings.clicked.connect(self.on_click_section_toggle)
        self.showAdvancedSettings.clicked.connect(self.on_click_section_toggle)
        self.showGeneralMetrics.clicked.connect(self.on_click_section_toggle)
        self.showAdvancedMetrics.clicked.connect(self.on_click_section_toggle)

        # Image selection button
        self.selectImage.clicked.connect(self.show_select_image_menu)

        # Process control
        self.processToggle.clicked.connect(self.process_toggle_handler)
        self.processActive = False

        self.activeImagePath = None
        self.activeImage = None

        # Demonstrative elements
        self.demonstrative = True
        self.toggleDemonstrativeElements.stateChanged.connect(self.toggle_demonstrative_element_generation)

    def init_element_states(self):
        """
        Sets default states and contents of various elements.
        """
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
        self.compressionLevelLabel.setVisible(False)
        self.compressionLevelValue.setVisible(False)
        self.edgeStrengthLabel.setVisible(False)
        self.edgeStrengthValue.setVisible(False)
        self.colorSalienceLabel.setVisible(False)
        self.colorSalienceValue.setVisible(False)
        self.samplingUniformityLabel.setVisible(False)
        self.samplingUniformityValue.setVisible(False)
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
        for widget in self.paramInputs[:-1]:
            widget.setValidator(QtGui.QDoubleValidator(0.0, 1.0, 2))
            widget.setText('1.0')
        self.seedValue.setValidator(QtGui.QDoubleValidator(0, 999999999, 0))
        self.seedValue.setText('0')

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
            self.compressionLevelLabel.setVisible(not self.compressionLevelLabel.isVisible())
            self.compressionLevelValue.setVisible(not self.compressionLevelValue.isVisible())
            self.edgeStrengthLabel.setVisible(not self.edgeStrengthLabel.isVisible())
            self.edgeStrengthValue.setVisible(not self.edgeStrengthValue.isVisible())
            self.colorSalienceLabel.setVisible(not self.colorSalienceLabel.isVisible())
            self.colorSalienceValue.setVisible(not self.colorSalienceValue.isVisible())
        # Toggle Advanced Settings section
        elif obj is self.showAdvancedSettings:
            button_text = self.showAdvancedSettings.text()
            self.showAdvancedSettings.setText(('Hide' if button_text[:4] == 'Show' else 'Show') + button_text[4:])
            self.samplingUniformityLabel.setVisible(not self.samplingUniformityLabel.isVisible())
            self.samplingUniformityValue.setVisible(not self.samplingUniformityValue.isVisible())
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
                self.activeImagePath = os.path.join(image_directory, file_name)
                self.load_image()

    def choose_image_on_disk(self):
        """
        Launch a file dialog to allow the user to select and image file from their machine.
        """
        # Start the file dialog at the user's home directory, store the path this dialog returns
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose image file...", os.path.expanduser("~"))
        if file_name:
            self.activeImagePath = file_name
            self.load_image()

    def load_image(self):
        """
        Load the image at path activeImagePath and show it as a preview in the graphics view.
        """
        self.activeImage = import_image(self.activeImagePath)
        h, w, _ = self.activeImage.shape
        bytes_per = 3 * w    # 3 color channels
        q_img = QtGui.QImage(self.activeImage.data, w, h, bytes_per, QtGui.QImage.Format_RGB888)
        # Create a QPixmap from the QImage, add it as a QGraphicsPixmapItem for display in QGraphicsView
        pixmap = QtGui.QPixmap.fromImage(q_img)
        pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        # Create a QGraphicsScene, add QGraphicsPixmapItem
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(pixmap_item)
        # Set scene in the QGraphicsView and scale
        self.viewGraphics.setScene(scene)
        self.viewGraphics.fitInView(pixmap_item, mode=QtCore.Qt.KeepAspectRatio)
        if self.demonstrative:
            pass
            # TODO: add HTML for load message/info

    def process_toggle_handler(self):
        """
        Switch process to opposite current state and call appropriate method.
        """
        if self.processActive:
            self.processActive = not self.processActive
            self.stop_process()
            self.processToggle.setText('Start')
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
            try:
                params = CompressionParams(
                    float(self.compressionLevelValue.text()),
                    float(self.edgeStrengthValue.text()),
                    float(self.colorSalienceValue.text()),
                    float(self.samplingUniformityValue.text()),
                    int(self.seedValue.text())
                )
            except ValueError:
                self.statusbar.showMessage(*sb_invalid_parameters)
                return
            # Update GUI elements and call start_process()
            self.clear_td()
            self.processActive = not self.processActive
            self.processToggle.setText('Stop')
            self.start_process(params)

    def start_process(self, params: CompressionParams):
        """
        TODO: handle compression process init
        """
        pass

    def stop_process(self):
        """
        TODO: handle compression process cancellation
        """
        pass

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


if __name__ == '__main__':
    start_gui()
