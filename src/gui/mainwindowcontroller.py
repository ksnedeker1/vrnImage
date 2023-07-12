from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowController, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.showGeneralSettings.clicked.connect(self.on_click_section_toggle)
        self.showAdvancedSettings.clicked.connect(self.on_click_section_toggle)
        self.showGeneralMetrics.clicked.connect(self.on_click_section_toggle)
        self.showAdvancedMetrics.clicked.connect(self.on_click_section_toggle)

        self.init_element_visibilities()

    def init_element_visibilities(self):
        """
        Sets default visibility of various elements.
        """
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
            self.compressionLevelLabel.setVisible(not self.compressionLevelLabel.isVisible())
            self.compressionLevelValue.setVisible(not self.compressionLevelValue.isVisible())
            self.edgeStrengthLabel.setVisible(not self.edgeStrengthLabel.isVisible())
            self.edgeStrengthValue.setVisible(not self.edgeStrengthValue.isVisible())
            self.colorSalienceLabel.setVisible(not self.colorSalienceLabel.isVisible())
            self.colorSalienceValue.setVisible(not self.colorSalienceValue.isVisible())
        # Toggle Advanced Settings section
        elif obj is self.showAdvancedSettings:
            self.samplingUniformityLabel.setVisible(not self.samplingUniformityLabel.isVisible())
            self.samplingUniformityValue.setVisible(not self.samplingUniformityValue.isVisible())
            self.seedLabel.setVisible(not self.seedLabel.isVisible())
            self.seedValue.setVisible(not self.seedValue.isVisible())
            self.toggleDemonstrativeElements.setVisible(not self.toggleDemonstrativeElements.isVisible())
        # Toggle General Metrics section
        elif obj is self.showGeneralMetrics:
            self.mCompressionRatioLabel.setVisible(not self.mCompressionRatioLabel.isVisible())
            self.mCompressionRatioValue.setVisible(not self.mCompressionRatioValue.isVisible())
            self.mProcessTimeLabel.setVisible(not self.mProcessTimeLabel.isVisible())
            self.mProcessTimeValue.setVisible(not self.mProcessTimeValue.isVisible())
            self.mSSIMLabel.setVisible(not self.mSSIMLabel.isVisible())
            self.mSSIMValue.setVisible(not self.mSSIMValue.isVisible())
        # Toggle Advanced Metrics section
        elif obj is self.showAdvancedMetrics:
            self.mMSELabel.setVisible(not self.mMSELabel.isVisible())
            self.mMSEValue.setVisible(not self.mMSEValue.isVisible())
            self.mPMSELabel.setVisible(not self.mPMSELabel.isVisible())
            self.mPMSEValue.setVisible(not self.mPMSEValue.isVisible())
            self.mSNRLabel.setVisible(not self.mSNRLabel.isVisible())
            self.mSNRValue.setVisible(not self.mSNRValue.isVisible())
            self.mPSNRLabel.setVisible(not self.mPSNRLabel.isVisible())
            self.mPSNRValue.setVisible(not self.mPSNRValue.isVisible())
            self.line_7.setVisible(not self.line_7.isVisible())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindowController()
    window.show()
    app.exec_()
