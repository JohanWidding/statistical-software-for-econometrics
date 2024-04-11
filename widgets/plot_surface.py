import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class PlotSurface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fig = Figure(constrained_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax = self.fig.add_subplot(111, projection='3d')

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def updateData(self, X, Y, Z, x_title='', y_title='', main_title='', **kwargs):
        # Clear previous plot
        self.ax.clear()

        # Plot the surface
        surf = self.ax.plot_surface(X, Y, Z, **kwargs)

        # Customize the z axis
        self.ax.set_zlim(np.min(Z), np.max(Z))

        # Set x-axis and y-axis titles
        self.ax.set_xlabel(x_title)
        self.ax.set_ylabel(y_title)

        # Set main title
        self.ax.set_title(main_title)

        # Add a color bar
        self.fig.colorbar(surf, shrink=0.5, aspect=5)

        # Redraw canvas
        self.canvas.draw()