import os
import cv2
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from lsb.lsb_steg import LSBSteg



class EncodeWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        loadUi('ui/encode_window.ui', self)
        self.parent = parent
        self.setupUi()

    def setupUi(self):
        self.btnSelectInput.clicked.connect(self.selectInputImage)
        self.btnSelectFile.clicked.connect(self.selectFileToHide)
        self.btnEncode.clicked.connect(self.encodeData)
        self.btnViewEncodedImage.clicked.connect(self.viewEncodedImage)
        self.btnBack.clicked.connect(self.goBack)

    def selectInputImage(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Input Image", "", "Image Files (*.png *.bmp)")
        if fileName:
            self.txtInputImage.setText(fileName)

    def selectFileToHide(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File to Hide", "", "All Files (*)")
        if fileName:
            self.txtFileToHide.setText(fileName)


    def encodeData(self):
        inputImage = self.txtInputImage.text()
        fileToHide = self.txtFileToHide.text()
        if inputImage and fileToHide:
            try:
                steg = LSBSteg(cv2.imread(inputImage))
                data = open(fileToHide, "rb").read()
                encodedImagePath = "encoded_image.png"
                encodedImage = steg.encode_binary(data)
                cv2.imwrite(encodedImagePath, encodedImage)
                self.txtEncodedImagePath.setText(os.path.abspath(encodedImagePath))
                QMessageBox.information(self, "Success", "Data encoded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Incomplete Data", "Please provide all the necessary information.")


    def viewEncodedImage(self):
        encodedImagePath = self.txtEncodedImagePath.text()
        if encodedImagePath:
            encodedImage = QPixmap(encodedImagePath)
            if not encodedImage.isNull():
                dialog = QDialog(self)
                dialog.setWindowTitle("Encoded Image")
                dialog.setFixedSize(800, 600)

                label = QLabel(dialog)
                label.setPixmap(encodedImage)
                label.setScaledContents(True)

                layout = QVBoxLayout()
                layout.addWidget(label)
                dialog.setLayout(layout)

                dialog.exec_()
            else:
                QMessageBox.warning(self, "Error", "Failed to load the encoded image.")
        else:
            QMessageBox.warning(self, "Error", "No encoded image found.")

    def goBack(self):
        self.parent.show()
        self.close()