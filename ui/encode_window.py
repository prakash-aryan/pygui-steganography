import os
import cv2
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QResource
from lsb.lsb_steg import LSBSteg

class EncodeWindow(QMainWindow):
    def __init__(self, steg_type, parent):
        super().__init__()
        loadUi('ui/encode_window.ui', self)
        self.steg_type = steg_type
        self.parent = parent
        self.setupUi()

    def setupUi(self):
        QResource.registerResource("ui/resources.qrc")

        self.btnSelectInput.clicked.connect(self.selectInputImage)
        self.btnSelectInput.setIcon(QIcon(":/icons/encode.png"))
        self.btnSelectData.clicked.connect(self.selectDataToHide)
        self.btnSelectData.setIcon(QIcon(":/icons/encode.png"))
        self.btnEncode.clicked.connect(self.encodeData)
        self.btnEncode.setIcon(QIcon(":/icons/encode.png"))
        self.btnViewEncodedImage.clicked.connect(self.viewEncodedImage)
        self.btnViewEncodedImage.setIcon(QIcon(":/icons/encode.png"))
        self.btnBack.clicked.connect(self.goBack)
        self.btnBack.setIcon(QIcon(":/icons/encode.png"))

    def selectInputImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input Image", "", "Image Files (*.png *.bmp)")
        if file_name:
            self.txtInputImage.setText(file_name)

    def selectDataToHide(self):
        if self.steg_type == 'Text':
            data, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)")
        elif self.steg_type == 'Image':
            data, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.bmp *.jpg)")
        else:
            data, _ = QFileDialog.getOpenFileName(self, "Select Binary File", "", "All Files (*)")
        if data:
            self.txtDataToHide.setText(data)

    def encodeData(self):
        input_image = self.txtInputImage.text()
        data_to_hide = self.txtDataToHide.text()

        if input_image and data_to_hide:
            try:
                steg = LSBSteg(cv2.imread(input_image))
                if self.steg_type == 'Text':
                    with open(data_to_hide, 'r') as file:
                        text_data = file.read()
                    encoded_image = steg.encode_text(text_data)
                elif self.steg_type == 'Image':
                    image_data = cv2.imread(data_to_hide)
                    if image_data is None:
                        raise ValueError("Invalid image format.")
                    encoded_image = steg.encode_image(image_data)
                else:
                    with open(data_to_hide, 'rb') as file:
                        binary_data = file.read()
                    encoded_image = steg.encode_binary(binary_data)

                encoded_image_path = "encoded_image.png"
                cv2.imwrite(encoded_image_path, encoded_image)
                self.txtEncodedImagePath.setText(os.path.abspath(encoded_image_path))
                QMessageBox.information(self, "Success", "Data encoded successfully!")
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Incomplete Data", "Please provide all the necessary information.")

    def viewEncodedImage(self):
        encoded_image_path = self.txtEncodedImagePath.text()
        if encoded_image_path:
            encoded_image = QPixmap(encoded_image_path)
            if not encoded_image.isNull():
                dialog = QDialog(self)
                dialog.setWindowTitle("Encoded Image")
                dialog.setFixedSize(800, 600)

                label = QLabel(dialog)
                label.setPixmap(encoded_image)
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