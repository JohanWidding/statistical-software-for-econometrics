from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView
import pandas as pd

class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0:  # Display index numbers in the first column
                return str(index.row() + 1)
            else:
                return str(self._data[index.row()][index.column() - 1])  # Adjust column index to account for index column
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:  # Display 'Index' as header for the first column
                return "Index"
            else:
                return str(self._headers[section - 1])  # Adjust column index to account for index column
        return None

class Page(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Create a table view
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        # Load the DataFrame from CSV file
        self.dataframe = pd.read_csv('data/dataset.csv')

        # Get headers
        headers = self.dataframe.columns.tolist()

        # Set up the data model
        self.model = CustomTableModel(self.dataframe.values.tolist(), headers)
        self.table_view.setModel(self.model)