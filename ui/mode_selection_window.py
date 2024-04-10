from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from .steg_type_selection_window import StegTypeSelectionWindow

class ModeSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/mode_selection.ui', self)
        self.btnEncode.clicked.connect(self.openStegTypeSelectionWindow)
        self.btnDecode.clicked.connect(self.openStegTypeSelectionWindow)

    def openStegTypeSelectionWindow(self):
        mode = self.sender().text()
        self.stegTypeSelectionWindow = StegTypeSelectionWindow(mode, self)
        self.stegTypeSelectionWindow.show()
        self.hide()