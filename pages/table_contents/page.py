from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget

class Page(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Table contents")
        self.layout.addWidget(self.label)