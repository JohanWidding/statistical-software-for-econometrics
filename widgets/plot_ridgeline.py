import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import matplotlib
from matplotlib.backends.backend_template import FigureCanvas
from sklearn.neighbors import KernelDensity

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid_spec
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class PlotRidgeline(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.fig = Figure(constrained_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax = self.fig.add_subplot()

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)



    def updateData(self, data, catagory_var, dep):
        data[catagory_var] = data[catagory_var].astype(str)
        categories = [str(cat) for cat in np.unique(data[catagory_var])]
        # Sort the list of strings numerically and alphabetically
        categories = sorted(categories, key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))

        self.ax.clear()
        gs = grid_spec.GridSpec(len(categories), 1)

        i = 0


        ax_objs = []
        for catagory in categories:
            # Filter the DataFrame based on the specified category
            filtered_data = data[data[catagory_var] == catagory]
            # Access the dependent variable column from the filtered DataFrame
            x = np.array(filtered_data[dep])

            x_d = np.linspace(0, 1, 1000)

            kde = KernelDensity(bandwidth=0.03, kernel='gaussian')
            kde.fit(x[:, None])

            logprob = kde.score_samples(x_d[:, None])

            # creating new axes object
            ax_objs.append(self.fig.add_subplot(gs[i:i + 1, 0:]))

            # plotting the distribution
            ax_objs[-1].plot(x_d, np.exp(logprob), color="#f0f0f0", lw=1)
            ax_objs[-1].fill_between(x_d, np.exp(logprob), alpha=1)

            # setting uniform x and y lims
            ax_objs[-1].set_xlim(0, 1)
            ax_objs[-1].set_ylim(0, 5)

            # make background transparent
            rect = ax_objs[-1].patch
            rect.set_alpha(0)

            # remove borders, axis ticks, and labels
            ax_objs[-1].set_yticklabels([])

            if i == len(categories) - 1:
                ax_objs[-1].set_xlabel("Test Score", fontsize=16, fontweight="bold")
            else:
                ax_objs[-1].set_xticklabels([])

            spines = ["top", "right", "left", "bottom"]
            for s in spines:
                ax_objs[-1].spines[s].set_visible(False)

            adj_country = catagory.replace(" ", "\n")
            ax_objs[-1].text(-0.02, 0, adj_country, fontweight="bold", fontsize=14, ha="right")

            i += 1

        gs.update(hspace=-0.7)

        self.ax.text(0.07, 0.85, "Distribution of Aptitude Test Results from 18 – 24 year-olds", fontsize=20)

        self.canvas.draw()

