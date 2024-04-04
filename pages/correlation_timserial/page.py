import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QScrollArea, QPushButton, QComboBox, QSlider, \
    QHBoxLayout

from widgets.toggle_by_multilple_options_button import ToggleByMultipleOptionsButton


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
        self.dropdown_group_label = QLabel("Select groupvar:")
        self.grid_layout.addWidget(self.dropdown_group_label, 0, 0)
        self.dropdown_group = QComboBox()
        self.dropdown_group.addItems(self.df.columns)
        self.grid_layout.addWidget(self.dropdown_group, 0, 1)

        self.dropdown_timevar_label = QLabel("Select timevariable (t):")
        self.grid_layout.addWidget(self.dropdown_timevar_label, 3, 0)
        self.dropdown_timevar = QComboBox()
        self.dropdown_timevar.addItems(self.df.columns)
        self.grid_layout.addWidget(self.dropdown_timevar, 3, 1)

        self.spacer1 = QLabel("")
        self.grid_layout.addWidget(self.spacer1, 0, 2)

        self.dropdown_yvar_label = QLabel("Select y-axis var:")
        self.grid_layout.addWidget(self.dropdown_yvar_label, 0, 3)
        self.dropdown_yvar = QComboBox()
        self.dropdown_yvar.addItems(self.df.columns)
        self.grid_layout.addWidget(self.dropdown_yvar, 1, 3)
        self.yvar_mode = ToggleByMultipleOptionsButton(["Nothing", "Somthing", "time"])
        self.yvar_mode.stateChanged.connect(self.update_state_label)

        self.grid_layout.addWidget(self.yvar_mode, 2, 3)
        # Create a slider
        self.slider = QSlider()
        self.slider.setOrientation(1)  # Set slider orientation to vertical
        self.slider.setMinimum(-5)  # Set minimum value
        self.slider.setMaximum(5)  # Set maximum value
        self.slider.setValue(0)  # Set initial value
        self.slider.setTickInterval(1)  # Set tick interval
        self.slider.setTickPosition(QSlider.TicksBothSides)  # Set tick position
        self.slider.valueChanged.connect(self.update_labels)
        self.grid_layout.addWidget(self.slider, 4, 3)

        # Create a central widget
        central_widget = QWidget()
        # Create a layout for the central widget
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)
        self.grid_layout.addWidget(central_widget, 5, 3)

        # Create labels for ticks
        self.labels = {}
        for value in range(-5, 6):
            label = QLabel(str(value))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            self.labels[value] = label

    def update_labels(self):
        value = self.slider.value()
        for val, label in self.labels.items():
            label.setStyleSheet("")  # Clear previous styling
            if val == value:
                label.setStyleSheet("font-weight: bold")  # Highlight current value


    def populate_scroll_layout(self):
        # Add widgets to the scroll layout
        pass  # Placeholder, replace with actual code



    def update_state_label(self, state):
        print(state)