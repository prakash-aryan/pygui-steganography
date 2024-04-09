from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from .encode_window import EncodeWindow
from .decode_window import DecodeWindow

class ModeSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/mode_selection.ui', self)
        self.btnEncode.clicked.connect(self.openEncodeWindow)
        self.btnDecode.clicked.connect(self.openDecodeWindow)

    def openEncodeWindow(self):
        self.encodeWindow = EncodeWindow(self)
        self.encodeWindow.show()
        self.hide()

    def openDecodeWindow(self):
        self.decodeWindow = DecodeWindow(self)
        self.decodeWindow.show()
        self.hide()