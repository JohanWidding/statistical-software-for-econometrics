import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QScrollArea, QPushButton, QComboBox, QSlider, \
    QHBoxLayout, QFrame

from functions.apply_transformation import apply_transformation
from functions.group_by_method import group_by_method
from widgets.plot_histogram import PlotHistogram
from widgets.toggle_by_multilple_options_button import ToggleByMultipleOptionsButton


class Page(QWidget):

    def __init__(self):
        super().__init__()

        # Load DataFrame from CSV file
        self.df = pd.read_csv('data/dataset.csv')

        self.groupvar = self.df.columns[0]
        self.groupvar_mode = "Mean"
        self.yvar = self.df.columns[0]
        self.yvar_mode = "Normal"
        self.xvar = self.df.columns[0]
        self.xvar_mode = "Normal"

        # First view: QGridLayout
        self.grid_layout = QGridLayout()
        # Add more widgets to the grid layout as needed
        self.populate_grid_layout()  # You can create a method to populate the grid layout
        self.grid_widget = QWidget()  # Creating a widget to hold the grid layout
        self.grid_widget.setLayout(self.grid_layout)

        # Second view: QScrollArea
        self.scroll_layout = QVBoxLayout()

        # Add more widgets to the scroll layout as needed
        self.populate_scroll_layout()  # You can create a method to populate the scroll layout
        self.scroll_widget = QWidget()  # Creating a widget to hold the scroll layout
        self.scroll_widget.setLayout(self.scroll_layout)

        # Main layout for the page
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.grid_widget)
        self.main_layout.addWidget(self.scroll_widget)

    def populate_grid_layout(self):
        # Groupvar Section
        # -----------------
        group_frame = QFrame()
        group_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        group_layout = QVBoxLayout()
        group_frame.setLayout(group_layout)

        self.dropdown_group_label = QLabel("Select groupvar:")
        group_layout.addWidget(self.dropdown_group_label)

        self.dropdown_group = QComboBox()
        self.dropdown_group.addItems(self.df.columns)
        group_layout.addWidget(self.dropdown_group)

        self.group_mode = ToggleByMultipleOptionsButton(
            ["Mean", "Median", "Mode", "\n", "First variable", "Last variable"])
        self.group_mode.stateChanged.connect(self.update_state_group)
        group_layout.addWidget(self.group_mode)

        # Add group frame to grid layout
        self.grid_layout.addWidget(group_frame, 0, 0)

        # Spacer
        self.spacer1 = QLabel("")
        self.grid_layout.addWidget(self.spacer1, 0, 2)

        # Yvar Section
        # ------------
        yvar_frame = QFrame()
        yvar_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        yvar_layout = QVBoxLayout()
        yvar_frame.setLayout(yvar_layout)

        self.dropdown_yvar_label = QLabel("Select y-axis var:")
        yvar_layout.addWidget(self.dropdown_yvar_label)

        self.dropdown_yvar = QComboBox()
        self.dropdown_yvar.addItems(self.df.columns)
        yvar_layout.addWidget(self.dropdown_yvar)

        self.yvar_mode = ToggleByMultipleOptionsButton(
            ["Normal", "ln(x)", "x^2", "√x", "\n", "∛x", "e^x", "1/x", "arcsin(√x)", "x -> rank(x)"])
        self.yvar_mode.stateChanged.connect(self.update_state_yvar)
        yvar_layout.addWidget(self.yvar_mode)

        # Add yvar frame to grid layout
        self.grid_layout.addWidget(yvar_frame, 0, 3)

        # Spacer
        self.spacer2 = QLabel("")
        self.grid_layout.addWidget(self.spacer2, 0, 4)

        # Xvar Section
        # ------------
        xvar_frame = QFrame()
        xvar_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        xvar_layout = QVBoxLayout()
        xvar_frame.setLayout(xvar_layout)

        self.dropdown_xvar_label = QLabel("Select x-axis var:")
        xvar_layout.addWidget(self.dropdown_xvar_label)

        self.dropdown_xvar = QComboBox()
        self.dropdown_xvar.addItems(self.df.columns)
        xvar_layout.addWidget(self.dropdown_xvar)

        self.xvar_mode = ToggleByMultipleOptionsButton(
            ["Normal", "ln(x)", "x^2", "√x", "\n", "∛x", "e^x", "1/x", "arcsin(√x)", "x -> rank(x)"])
        self.xvar_mode.stateChanged.connect(self.update_state_xvar)
        xvar_layout.addWidget(self.xvar_mode)

        # Add xvar frame to grid layout
        self.grid_layout.addWidget(xvar_frame, 0, 5)

    def update_labels(self):
        value = self.slider.value()
        for val, label in self.labels.items():
            label.setStyleSheet("")  # Clear previous styling
            if val == value:
                label.setStyleSheet("font-weight: bold")  # Highlight current value


    def populate_scroll_layout(self):
        # Create a frame for both histograms
        histograms_frame = QFrame()
        histograms_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        # Create a layout for the histograms frame
        histograms_layout = QHBoxLayout(histograms_frame)
        histograms_frame.setLayout(histograms_layout)

        self.yvar_histogram = PlotHistogram()
        self.xvar_histogram = PlotHistogram()

        # Add the histograms to the histograms layout
        histograms_layout.addWidget(self.yvar_histogram)
        histograms_layout.addWidget(self.xvar_histogram)

        # Add the grid layout to the scroll layout
        self.scroll_layout.addWidget(histograms_frame)

        # Add widgets to the scroll layout
        pass  # Placeholder, replace with actual code

    def update_data_to_show(self):
        # Selecting three headers/columns from the original DataFrame
        selected_columns = [self.dropdown_group.currentText(), self.dropdown_yvar.currentText(), self.dropdown_xvar.currentText()]

        # Creating a sub DataFrame with only the selected columns
        sub_df = self.df[selected_columns].copy()
        sub_df = apply_transformation(sub_df, selected_columns[1], self.yvar_mode)
        sub_df = apply_transformation(sub_df, selected_columns[2], self.xvar_mode)
        sub_df = group_by_method(sub_df, selected_columns[0], self.group_mode)

        self.yvar_histogram.updateData(sub_df, selected_columns[1])
        self.xvar_histogram.updateData(sub_df, selected_columns[2])




    def update_state_group(self, state):
        self.group_mode = state
        self.update_data_to_show()

    def update_state_xvar(self, state):
        self.xvar_mode = state
        self.update_data_to_show()

    def update_state_yvar(self, state):
        self.yvar_mode = state
        self.update_data_to_show()