from PyQt5 import QtWidgets, QtCore
from mainwindow import Ui_MainWindow
from resources.htmlstrings import *
from resources.statusbarmessages import *
from os.path import expanduser
# from ..utils.fileio import import_image


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowController, self).__init__(*args, **kwargs)
        self.setupUi(self)

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

    def show_select_image_menu(self):
        """
        Secondary selection for 'Select Image'. User can choose images included with the application, or from their
        computer.
        """
        menu = QtWidgets.QMenu()
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
        TODO: implement selection window/dialog for included images
        """
        pass

    def choose_image_on_disk(self):
        """
        Launch a file dialog to allow the user to select and image file from their machine.
        """
        # Start the file dialog at the user's home directory, store the path this dialog returns
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose image file...", expanduser("~"))
        if file_name:
            self.activeImagePath = file_name

    def init_element_states(self):
        """
        Sets default states and contents of various elements.
        """
        self.toggleDemonstrativeElements.setChecked(True)

        self.textDisplay.setHtml(td_welcome_message)

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

    def process_toggle_handler(self):
        """
        Switch process to opposite current state and call appropriate method.
        """
        if self.processActive:
            self.processActive = not self.processActive
            self.stop_process()
            self.processToggle.setText('Start')
        else:
            if self.activeImagePath is None:
                self.statusbar.showMessage(*sb_no_image_selected)
                return
            self.processActive = not self.processActive
            self.processToggle.setText('Stop')
            self.start_process()

    def start_process(self):
        """
        TODO: handle compression process init
        """
        pass

    def stop_process(self):
        """
        TODO: handle compression process cancellation
        """
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindowController()
    window.show()
    app.exec_()
