import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from dashboard.dashboard import Dashboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Sample data for initialization
        data = {'counterparties': ['Counterparty 1', 'Counterparty 2', 'Counterparty 3']}

        # Create the Dashboard instance
        self.dashboard = Dashboard(data)

        # Set up the main window
        self.setWindowTitle("Dashboard Demo")
        self.setCentralWidget(self.dashboard)
        self.setGeometry(100, 100, 800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
