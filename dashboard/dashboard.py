import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QPushButton, QGridLayout, QLineEdit, QScrollArea
from PyQt5.QtCore import Qt

from dashboard.show_selection_widget import ShowSelectionWidget


class Dashboard(QWidget):
    data_signal = pyqtSignal(dict)  # Define a signal to send data to the parent

    def __init__(self, data):
        super().__init__()
        self.data = data
        layout = QGridLayout()

        label = QLabel('Analytical tools')
        label.setFont(QFont("Arial", 14))
        self.search_input = QLineEdit()
        search_button = QPushButton("Search")
        self.search_input.returnPressed.connect(self.handle_search)
        search_button.clicked.connect(self.handle_search)

        self.search_input.setFixedWidth(300)
        self.search_input.setFixedHeight(50)
        self.search_input.setFont(QFont("Arial", 20))
        search_button.setFixedWidth(300)

        self.result_label = QLabel('Results:')
        self.result_display = QWidget()  # Container for scrollable results
        self.result_layout = QVBoxLayout()
        self.result_layout.setAlignment(Qt.AlignTop)
        self.result_display.setLayout(self.result_layout)


        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.result_display)
        scroll_area.setFixedWidth(300)
        self.updateScrollArea(".\\pages", "")


        # Create a new widget for the additional box
        self.additional_box = ShowSelectionWidget()


        layout.addWidget(label, 0, 0)
        layout.addWidget(self.search_input, 1, 0)
        layout.addWidget(search_button, 2, 0)
        layout.addWidget(self.result_label, 3, 0)
        layout.addWidget(scroll_area, 4, 0)
        layout.addWidget(self.additional_box, 0, 1, 5, 2)

        self.setLayout(layout)

    def handle_search(self):
        # This function will be called when the "Search" button is clicked.
        search_term = self.search_input.text()

        self.updateScrollArea(".\\pages", search_term)

    import os

    # ...

    def updateScrollArea(self, relative_folder_path, search_term):
        search_term = search_term.replace(" ", "_").lower()
        # Construct the absolute path to the folder
        folder_path = os.path.join(os.getcwd(), relative_folder_path)

        # Clear any previous buttons
        for i in reversed(range(self.result_layout.count())):
            widget = self.result_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Get the list of sub-folders in the specified folder that begin with the search term
        subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir() and f.name.startswith(search_term)]

        self.result_label.setText('Sub-folders: ' + '(' + str(len(subfolders)) + ')')

        # Create buttons based on sub-folders
        for subfolder in subfolders:
            button = QPushButton(subfolder.replace("_", " ").capitalize())
            button.setStyleSheet("text-align: left;")
            button.clicked.connect(lambda checked, folder=subfolder: self.details_button_click(folder))
            self.result_layout.addWidget(button)

    def details_button_click(self, info):
        self.additional_box.update_data(info)

