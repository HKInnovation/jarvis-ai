import sys
from PyQt5.QtWidgets import QApplication
from ui.jarvis_window import JarvisWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisWindow()
    window.show()
    sys.exit(app.exec_())   