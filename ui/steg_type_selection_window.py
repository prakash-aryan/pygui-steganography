from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from ui.encode_window import EncodeWindow
from ui.decode_window import DecodeWindow

class StegTypeSelectionWindow(QWidget):
    def __init__(self, mode, parent):
        super().__init__()
        loadUi('ui/steg_type_selection.ui', self)
        self.mode = mode
        self.parent = parent
        self.btnText.clicked.connect(self.openStegWindow)
        self.btnImage.clicked.connect(self.openStegWindow)
        self.btnBinary.clicked.connect(self.openStegWindow)
        self.btnBack.clicked.connect(self.goBack)

    def openStegWindow(self):
        steg_type = self.sender().text()
        if self.mode == 'Encode':
            self.stegWindow = EncodeWindow(steg_type, self)
        else:
            self.stegWindow = DecodeWindow(steg_type, self)
        self.stegWindow.show()
        self.hide()

    def goBack(self):
        self.parent.show()
        self.close()