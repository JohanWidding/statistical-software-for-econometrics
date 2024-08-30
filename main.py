import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow

from dashboard.dashboard import Dashboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the Dashboard instance
        self.dashboard = Dashboard()

        # Set up the main window
        self.setWindowTitle("Dashboard Demo")
        self.setCentralWidget(self.dashboard)
        self.setGeometry(100, 100, 800, 600)

        # Set standard font size
        font = QFont()
        font.setPointSize(12)  # Adjust the point size as needed
        self.setFont(font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
