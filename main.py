import sys
from PyQt5.QtWidgets import QApplication
from ui.mode_selection_window import ModeSelectionWindow
from ui.styles import message_box_style

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Apply the style sheet
    app.setStyleSheet(message_box_style)

    modeSelectionWindow = ModeSelectionWindow()
    modeSelectionWindow.show()

    sys.exit(app.exec_())