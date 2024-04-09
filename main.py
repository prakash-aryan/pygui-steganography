import sys
from PyQt5.QtWidgets import QApplication
from ui.mode_selection_window import ModeSelectionWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    modeSelectionWindow = ModeSelectionWindow()
    modeSelectionWindow.show()
    sys.exit(app.exec_())