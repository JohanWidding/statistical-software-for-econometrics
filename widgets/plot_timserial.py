import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.ticker import FuncFormatter

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class PlotTimeserialDf(QWidget):

    def __init__(self, ylabel="", xlabel="", title="", formatter="", color=None, legend=True):
        self.y_ax_name = ylabel
        self.x_ax_name = xlabel
        self.title_name = title
        self.colors = color
        self.formatter = formatter
        self.has_legend = legend

        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Add a grid
        self.sc.axes.grid(True)



        # Add a title
        self.sc.axes.set_title(self.title_name)

        # Add a label for the y-axis
        self.sc.axes.set_ylabel(self.y_ax_name)
        self.sc.axes.set_xlabel(self.x_ax_name)

        layout.addWidget(self.sc)

        self.setLayout(layout)

        # Set the background color using CSS
        self.setStyleSheet("background-color: none;")

    def change_formatter(self, x, pos):
        return self.formatter + f'{x:.2f}'

    def updateData(self, df):
        self.sc.axes.clear()  # Clear the previous plot
        if self.colors == None:
            df.plot(ax=self.sc.axes, legend=False)
        else:
            df.plot(ax=self.sc.axes, legend=False, color=self.colors)  # Disable automatic legend

        self.sc.axes.grid(True)

        # Add a title
        self.sc.axes.set_title(self.title_name)

        # Add a label for the y-axis
        self.sc.axes.set_ylabel(self.y_ax_name)
        self.sc.axes.set_xlabel(self.x_ax_name)


        # Display the legend outside the plot to the right
        if self.has_legend: self.sc.axes.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

        self.sc.axes.yaxis.set_major_formatter(FuncFormatter(self.change_formatter))

        self.sc.draw()

