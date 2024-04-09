import os
import cv2
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from lsb.lsb_steg import LSBSteg

class DecodeWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        loadUi('ui/decode_window.ui', self)
        self.parent = parent
        self.setupUi()

    def setupUi(self):
        self.btnSelectInput.clicked.connect(self.selectInputImage)
        self.btnDecode.clicked.connect(self.decodeData)
        self.btnBack.clicked.connect(self.goBack)

    def selectInputImage(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Input Image", "", "Image Files (*.png *.bmp)")
        if fileName:
            self.txtInputImage.setText(fileName)

    def decodeData(self):
        inputImage = self.txtInputImage.text()

        if inputImage:
            try:
                steg = LSBSteg(cv2.imread(inputImage))
                data = steg.decode_binary()
                decodedText = data.decode('utf-8', errors='replace')
                self.txtDecodedText.setPlainText(decodedText)

                outputFile = "decoded_text.txt"
                with open(outputFile, "w") as file:
                    file.write(decodedText)
                self.txtDecodedFilePath.setText(os.path.abspath(outputFile))

                QMessageBox.information(self, "Success", "Data decoded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Incomplete Data", "Please select an input image.")

    def goBack(self):
        self.parent.show()
        self.close()