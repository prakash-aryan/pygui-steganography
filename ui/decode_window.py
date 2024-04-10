import os
import cv2
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QResource
from PyQt5.uic import loadUi
from lsb.lsb_steg import LSBSteg

class DecodeWindow(QMainWindow):
    def __init__(self, steg_type, parent):
        super().__init__()
        loadUi('ui/decode_window.ui', self)
        self.steg_type = steg_type
        self.parent = parent
        self.setupUi()

    def setupUi(self):
        QResource.registerResource("ui/resources.qrc")

        self.btnSelectInput.clicked.connect(self.selectInputImage)
        self.btnSelectInput.setIcon(QIcon(":/icons/decode.png"))
        self.btnDecode.clicked.connect(self.decodeData)
        self.btnDecode.setIcon(QIcon(":/icons/decode.png"))
        self.btnViewDecodedData.clicked.connect(self.viewDecodedData)
        self.btnViewDecodedData.setIcon(QIcon(":/icons/decode.png"))
        self.btnBack.clicked.connect(self.goBack)
        self.btnBack.setIcon(QIcon(":/icons/decode.png"))

    def selectInputImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input Image", "", "Image Files (*.png *.bmp)")
        if file_name:
            self.txtInputImage.setText(file_name)

    def decodeData(self):
        input_image = self.txtInputImage.text()
        if input_image:
            try:
                steg = LSBSteg(cv2.imread(input_image))
                if self.steg_type == 'Text':
                    decoded_data = steg.decode_text()
                    output_file = "decoded_text.txt"
                    with open(output_file, "w") as file:
                        file.write(decoded_data)
                elif self.steg_type == 'Image':
                    decoded_image = steg.decode_image()
                    if decoded_image is None:
                        raise ValueError("Invalid image format.")
                    output_file = "decoded_image.png"
                    cv2.imwrite(output_file, decoded_image)
                else:
                    decoded_data = steg.decode_binary()
                    output_file = "decoded_binary.bin"
                    with open(output_file, "wb") as file:
                        file.write(decoded_data)
                decoded_file_path_edit = self.findChild(QLineEdit, "txtDecodedFilePath")
                if decoded_file_path_edit:
                    decoded_file_path_edit.setText(os.path.abspath(output_file))
                QMessageBox.information(self, "Success", "Data decoded successfully!")
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Incomplete Data", "Please select an input image.")

    def viewDecodedData(self):
        decoded_file_path = self.findChild(QLineEdit, "txtDecodedFilePath").text()
        if decoded_file_path:
            try:
                os.startfile(decoded_file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "No decoded data found.")

    def goBack(self):
        self.parent.show()
        self.close()