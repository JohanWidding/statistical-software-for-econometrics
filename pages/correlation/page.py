import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QScrollArea, QPushButton, QComboBox


class Page(QWidget):

    def __init__(self):
        super().__init__()

        # Load DataFrame from CSV file
        self.df = pd.read_csv('data/dataset.csv')

        # First view: QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_label = QLabel("Grid Layout Contents")
        self.grid_layout.addWidget(self.grid_label, 0, 0)
        # Add more widgets to the grid layout as needed
        self.populate_grid_layout()  # You can create a method to populate the grid layout
        self.grid_widget = QWidget()  # Creating a widget to hold the grid layout
        self.grid_widget.setLayout(self.grid_layout)

        # Second view: QScrollArea
        self.scroll_layout = QVBoxLayout()
        self.scroll_label = QLabel("Scroll View Contents")
        self.scroll_layout.addWidget(self.scroll_label)
        # Add more widgets to the scroll layout as needed
        self.populate_scroll_layout()  # You can create a method to populate the scroll layout
        self.scroll_widget = QWidget()  # Creating a widget to hold the scroll layout
        self.scroll_widget.setLayout(self.scroll_layout)

        # Main layout for the page
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.grid_widget)
        self.main_layout.addWidget(self.scroll_widget)

    def populate_grid_layout(self):
        # Add dropdown menu with header items from DataFrame
        self.dropdown_group_label = QLabel("Select Column:")
        self.grid_layout.addWidget(self.dropdown_group_label, 0, 0)
        self.dropdown_group = QComboBox()
        self.dropdown_group.addItems(self.df.columns)
        self.grid_layout.addWidget(self.dropdown_group, 0, 1)

        self.dropdown_timevar_label = QLabel("Select Column:")
        self.grid_layout.addWidget(self.dropdown_timevar_label, 1, 0)
        self.dropdown_timevar = QComboBox()
        self.dropdown_timevar.addItems(self.df.columns)
        self.grid_layout.addWidget(self.dropdown_timevar, 1, 1)


    def populate_scroll_layout(self):
        # Add widgets to the scroll layout
        pass  # Placeholder, replace with actual code