import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class PlotHistogram(QWidget):

    def __init__(self, data=None, column_name="", title="", xlabel="", ylabel="Frequency", color=None):
        self.data = data
        self.column_name = column_name
        self.title_name = title
        self.xlabel_name = xlabel
        self.ylabel_name = ylabel
        self.color = color

        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create the matplotlib FigureCanvas object
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Add a title
        self.canvas.axes.set_title(self.title_name)

        # Add labels for the axes
        self.canvas.axes.set_xlabel(self.xlabel_name)
        self.canvas.axes.set_ylabel(self.ylabel_name)

        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # Set the background color using CSS
        self.setStyleSheet("background-color: none;")

    def updateData(self, data, column_name, title="", xlabel="", ylabel=""):


        self.canvas.axes.clear()  # Clear the previous plot

        # Plot histogram
        self.canvas.axes.hist(data[column_name])

        # Set the title, labels, and redraw the canvas
        self.canvas.axes.set_title(title)
        self.canvas.axes.set_xlabel(xlabel)
        self.canvas.axes.set_ylabel(ylabel)
        self.canvas.draw()
