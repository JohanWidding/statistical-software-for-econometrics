import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QScrollArea, QPushButton, QComboBox, QSlider, \
    QHBoxLayout, QFrame, QMessageBox, QSizePolicy
from matplotlib import cm

from functions.apply_transformation import apply_transformation
from functions.group_by_method import group_by_method
from functions.logistic_regression_surface_xyz import logistic_regression_surface
from widgets.plot_histogram import PlotHistogram
from widgets.plot_surface import PlotSurface
from widgets.plot_threeway import PlotThreeWay
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
        self.zvar = self.df.columns[0]
        self.zvar_state = "Normal"

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

        # Set the size policy of the scroll area
        self.scroll_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

        self.group_mode = ToggleByMultipleOptionsButton(
            ["Mean", "Median", "Mode", "\n", "First variable", "Last variable"])
        self.group_mode.set_state(self.group_state)
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
        self.dropdown_yvar.setCurrentText(self.yvar)
        yvar_layout.addWidget(self.dropdown_yvar)

        self.yvar_mode = ToggleByMultipleOptionsButton(
            ["Normal", "ln(x)", "x^2", "√x", "\n", "∛x", "e^x", "1/x", "arcsin(√x)", "x -> rank(x)"])
        self.yvar_mode.set_state(self.yvar_state)
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
        self.dropdown_xvar.setCurrentText(self.xvar)
        xvar_layout.addWidget(self.dropdown_xvar)

        self.xvar_mode = ToggleByMultipleOptionsButton(
            ["Normal", "ln(x)", "x^2", "√x", "\n", "∛x", "e^x", "1/x", "arcsin(√x)", "x -> rank(x)"])
        self.xvar_mode.set_state(self.xvar_state)
        self.xvar_mode.stateChanged.connect(self.update_state_xvar)
        xvar_layout.addWidget(self.xvar_mode)

        # Add xvar frame to grid layout
        self.grid_layout.addWidget(xvar_frame, 0, 5)

        # Spacer
        self.spacer2 = QLabel("")
        self.grid_layout.addWidget(self.spacer2, 0, 6)

        # Zvar Section
        # ------------
        zvar_frame = QFrame()
        zvar_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        zvar_layout = QVBoxLayout()
        zvar_frame.setLayout(zvar_layout)

        self.dropdown_zvar_label = QLabel("Select z-axis var:")
        zvar_layout.addWidget(self.dropdown_zvar_label)

        self.dropdown_zvar = QComboBox()
        self.dropdown_zvar.addItems(self.df.columns)
        self.dropdown_zvar.setCurrentText(self.zvar)
        zvar_layout.addWidget(self.dropdown_zvar)

        self.zvar_mode = ToggleByMultipleOptionsButton(
            ["Normal", "ln(x)", "x^2", "√x", "\n", "∛x", "e^x", "1/x", "arcsin(√x)", "x -> rank(x)"])
        self.zvar_mode.set_state(self.zvar_state)
        self.zvar_mode.stateChanged.connect(self.update_state_zvar)
        zvar_layout.addWidget(self.zvar_mode)

        # Add zvar frame to grid layout
        self.grid_layout.addWidget(zvar_frame, 0, 7)

        self.dropdown_group.currentIndexChanged.connect(self.update_data_to_show)
        self.dropdown_yvar.currentIndexChanged.connect(self.update_data_to_show)
        self.dropdown_xvar.currentIndexChanged.connect(self.update_data_to_show)
        self.dropdown_zvar.currentIndexChanged.connect(self.update_data_to_show)

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
        # Set stretch factor for the histograms frame to make it expand
        histograms_layout.setStretchFactor(histograms_frame, 1)

        self.plotsurface = PlotSurface()

        self.df = self.df[self.df['Stilling_F'] < 100]

        dep = 'Lang_fravær'
        explan = ['Ansatt_antallAAR', 'Stilling_F']
        """
        Det ser ut til at vi kan dele inn i grupper for utdannelsekode, dette datasettet er for hele kommunen, alle ansatte.
        Ansvar betyr hvilken avdeling de jobber i.
        
        """
        # Create data
        #X, Y, Z = logistic_regression_surface(self.df, 'Lang_fravær', explan)
        X, Y, Z = logistic_regression_surface(self.df, 'Lang_fravær', explan, time_control='t')
        # X, Y, Z = logistic_regression_surface(self.df, 'Lang_fravær', explan, time_control='t', entity_control='LNR', sample_percentage=0.01)

        # Update the plot with the provided data
        self.plotsurface.updateData(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, x_title=explan[0], y_title=explan[1], main_title=f"Sansynlighet for {dep}")

        # Add the histograms to the histograms layout
        histograms_layout.addWidget(self.plotsurface)

        # Add the grid layout to the scroll layout
        self.scroll_layout.addWidget(histograms_frame)


        # Add widgets to the scroll layout
        pass  # Placeholder, replace with actual code

    def update_data_to_show(self):


        # Selecting three headers/columns from the original DataFrame
        selected_columns = [self.dropdown_group.currentText(), self.dropdown_xvar.currentText(), self.dropdown_yvar.currentText(), self.dropdown_zvar.currentText()]

        # Creating a sub DataFrame with only the selected columns
        sub_df = self.df[selected_columns].copy()

        # Check if the name at the 0th position is different from the names at the 1st, 2nd, and 3rd positions
        if not (selected_columns[0] != selected_columns[1] and selected_columns[0] != selected_columns[2] and
                selected_columns[0] != selected_columns[3]):
            return

        sub_df = apply_transformation(sub_df, selected_columns[1], self.xvar_state)
        sub_df = apply_transformation(sub_df, selected_columns[2], self.yvar_state)
        sub_df = apply_transformation(sub_df, selected_columns[3], self.zvar_state)
        sub_df = group_by_method(sub_df, selected_columns[0], self.group_state)

        # Check if sub_df is None
        if sub_df is None:
            # Handle the case where sub_df is None (possibly due to an error in the transformation functions)
            QMessageBox.warning(self, "Error", "Error in the group by function")
            return
        # Check for infinite values
        if sub_df.isin([np.inf, -np.inf]).any().any():
            QMessageBox.warning(self, "Error", "Data contains infinite values.")
            return

        self.threeway.updateData(sub_df, x_ax_name=selected_columns[1], y_ax_name=selected_columns[2], z_ax_name=selected_columns[3])



    def update_state_group(self, state):
        self.group_state = state
        self.update_data_to_show()

    def update_state_xvar(self, state):
        self.xvar_state = state
        self.update_data_to_show()

    def update_state_yvar(self, state):
        self.yvar_state = state
        self.update_data_to_show()

    def update_state_zvar(self, state):
        self.zvar_state = state
        self.update_data_to_show()