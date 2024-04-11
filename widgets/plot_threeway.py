import sys
import numpy as np
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import FuncFormatter


class PlotThreeWay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fig = Figure(constrained_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax = self.fig.add_subplot(111, projection='3d')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def updateData(self, df, title_name='', x_ax_name='', y_ax_name='', z_ax_name='', has_legend=False, change_formatter=None):
        self.ax.clear()
        x_data = df.iloc[:, 0]
        y_data = df.iloc[:, 1]
        z_data = df.iloc[:, 2]

        self.scatter = self.ax.scatter(x_data, y_data, z_data)

        self.ax.grid(True)
        self.ax.set_title(title_name)
        self.ax.set_xlabel(x_ax_name)
        self.ax.set_ylabel(y_ax_name)
        self.ax.set_zlabel(z_ax_name)

        if has_legend:
            self.ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

        if change_formatter:
            self.ax.xaxis.set_major_formatter(FuncFormatter(change_formatter))

        self.canvas.draw()