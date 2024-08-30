import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QScrollArea, QPushButton, QComboBox, QSlider, \
    QHBoxLayout, QFrame, QMessageBox, QFormLayout

from functions.apply_transformation import apply_transformation
from functions.group_by_method import group_by_method
from widgets.plot_histogram import PlotHistogram
from widgets.plot_ridgeline import PlotRidgeline
from widgets.plot_twoway import PlotTwoWay
from widgets.toggle_by_multilple_options_button import ToggleByMultipleOptionsButton


class Page(QWidget):

    def __init__(self):
        super().__init__()

        # Load DataFrame from CSV file
        self.df = pd.read_csv('data/dataset.csv')
        # Identify non-numeric columns
        non_numeric_columns = self.df.select_dtypes(exclude=['number']).columns
        # Drop non-numeric columns
        self.df.drop(columns=non_numeric_columns, inplace=True)

        self.groupvar = self.df.columns[0]
        self.group_state = "Mean"
        self.yvar = self.df.columns[0]
        self.yvar_state = "Normal"
        self.xvar = self.df.columns[0]
        self.xvar_state = "Normal"

        # First view: QGridLayout
        self.grid_layout = QGridLayout()
        # Add more widgets to the grid layout as needed
        self.populate_grid_layout()  # You can create a method to populate the grid layout
        self.grid_widget = QWidget()  # Creating a widget to hold the grid layout
        self.grid_widget.setLayout(self.grid_layout)

        # Frame to contain the scrollable results
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)  # Set frame shape
        frame_layout = QVBoxLayout(frame)

        # Container widget for scrollable results
        self.result_display = QWidget()
        self.scroll_layout = QFormLayout()
        self.result_display.setLayout(self.scroll_layout)
        self.populate_scroll_layout()

        # Scroll area widget
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setWidget(self.result_display)

        # Add scroll area to frame layout
        frame_layout.addWidget(self.scroll_area)

        # Add more widgets to the scroll layout as needed
        # You can create a method to populate the scroll layout

        # Main layout for the page
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.grid_widget)
        self.main_layout.addWidget(frame)  # Add the scroll area to the main layout

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
        self.dropdown_group.setCurrentText(self.groupvar)
        group_layout.addWidget(self.dropdown_group)


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

        self.dropdown_yvar_label = QLabel("Select time variable:")
        yvar_layout.addWidget(self.dropdown_yvar_label)

        self.dropdown_yvar = QComboBox()
        self.dropdown_yvar.addItems(self.df.columns)
        self.dropdown_yvar.setCurrentText(self.yvar)
        yvar_layout.addWidget(self.dropdown_yvar)


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

        self.dropdown_xvar_label = QLabel("Select variable to check:")
        xvar_layout.addWidget(self.dropdown_xvar_label)

        self.dropdown_xvar = QComboBox()
        self.dropdown_xvar.addItems(self.df.columns)
        self.dropdown_xvar.setCurrentText(self.xvar)
        xvar_layout.addWidget(self.dropdown_xvar)

        self.xvar_mode = ToggleByMultipleOptionsButton(
            ["Normal", "ln(x)", "x^2", "√x", "\n", "∛x", "e^x", "1/x", "arcsin(√x)", "x -> rank(x)"])
        self.xvar_mode.set_state(self.xvar_state)
        self.xvar_mode.stateChanged.connect(self.update_state_xvar)
        xvar_layout.addWidget(self.xvar_mode)

        # Add xvar frame to grid layout
        self.grid_layout.addWidget(xvar_frame, 0, 5)

        self.dropdown_group.currentIndexChanged.connect(self.update_data_to_show)
        self.dropdown_yvar.currentIndexChanged.connect(self.update_data_to_show)
        self.dropdown_xvar.currentIndexChanged.connect(self.update_data_to_show)

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

        self.var_histogram = PlotHistogram()


        # Add the histograms to the histograms layout
        histograms_layout.addWidget(self.var_histogram)

        self.var_ridgeline = PlotRidgeline()

        histograms_frame.setFixedHeight(600)


        # Add the grid layout to the scroll layout
        self.scroll_layout.addWidget(histograms_frame)

        self.scroll_layout.addWidget(self.var_ridgeline)

        # Add widgets to the scroll layout
        pass  # Placeholder, replace with actual code

    def update_data_to_show(self):


        # Selecting three headers/columns from the original DataFrame
        selected_columns = [self.dropdown_group.currentText(), self.dropdown_yvar.currentText(), self.dropdown_xvar.currentText()]

        # Creating a sub DataFrame with only the selected columns
        sub_df = self.df[selected_columns].copy()

        # Check if the name at the 0th position is different from the names at 1st and 2nd positions
        if not (selected_columns[0] != selected_columns[1] and selected_columns[0] != selected_columns[2]):
            return

        sub_df = apply_transformation(sub_df, selected_columns[2], self.xvar_state)

        # Check if sub_df is None
        if sub_df is None:
            # Handle the case where sub_df is None (possibly due to an error in the transformation functions)
            QMessageBox.warning(self, "Error", "Error in the group by function")
            return
        # Check for infinite values
        if sub_df.isin([np.inf, -np.inf]).any().any():
            QMessageBox.warning(self, "Error", "Data contains infinite values.")
            return

        self.var_histogram.updateData(sub_df, selected_columns[2])
        self.var_ridgeline.updateData(sub_df, selected_columns[1], selected_columns[2])

        new_height = 600 * len([str(cat) for cat in np.unique(sub_df[selected_columns[1]])])
        # Set the minimum height of the frame to the new calculated height
        self.var_ridgeline.setFixedHeight(new_height)




    def update_state_xvar(self, state):
        self.xvar_state = state
        self.update_data_to_show()