from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib
from matplotlib.ticker import FuncFormatter

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class PlotTwoWay(QWidget):
    def __init__(self, ylabel="", xlabel="", title="", formatter="", color=None, legend=False):
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
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.grid(True)
        self.sc.axes.set_title(self.title_name)
        self.sc.axes.set_ylabel(self.y_ax_name)
        self.sc.axes.set_xlabel(self.x_ax_name)
        layout.addWidget(self.sc)
        self.setLayout(layout)
        self.setStyleSheet("background-color: none;")

    def change_formatter(self, x, pos):
        return self.formatter + f'{x:.2f}'

    def updateData(self, df):
        self.sc.axes.clear()
        x_data = df.iloc[:, 0]
        y_data = df.iloc[:, 1]

        self.sc.axes.scatter(y_data, x_data)

        self.sc.axes.grid(True)
        self.sc.axes.set_title(self.title_name)
        self.sc.axes.set_ylabel(self.y_ax_name)
        self.sc.axes.set_xlabel(self.x_ax_name)

        if self.has_legend:
            self.sc.axes.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

        self.sc.axes.yaxis.set_major_formatter(FuncFormatter(self.change_formatter))
        self.sc.draw()
