from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, QSize

class ShowSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.rating_list = QListWidget(self)
        self.layout.addWidget(self.rating_list)


    def update_data(self, name):
        self.name = name



    def on_rating_changed(self, string):
        print(string)