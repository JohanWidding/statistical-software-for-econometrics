import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget

class Page(QWidget):

    def __init__(self):
        super().__init__()

        # Load the DataFrame from CSV file
        self.dataframe = pd.read_csv('data/dataset.csv')

        print(list(self.dataframe.head()))

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Table contents")
        self.layout.addWidget(self.label)