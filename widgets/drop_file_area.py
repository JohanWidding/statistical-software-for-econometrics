import os

import pandas as pd
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DropArea(QWidget):
    def __init__(self):
        super().__init__()

        # Create layout for the drop area
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create QLabel for drop area
        self.drop_label = QLabel("Drop files here")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setAcceptDrops(True)

        # Set frame style
        self.drop_label.setStyleSheet("QLabel { border: 2px dashed #aaa; border-radius: 8px; color: darkgray;}")



        # Add drop label and plus symbol to layout
        self.layout.addWidget(self.drop_label)

        # Connect drag and drop events
        self.drop_label.dragEnterEvent = self.dragEnterEvent
        self.drop_label.dropEvent = self.dropEvent

        # Create a label to display the file name
        self.file_label = QLabel("")
        self.file_label.setAlignment(Qt.AlignCenter)

        # Add the label to the layout
        self.layout.addWidget(self.file_label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            print("Dropped file:", file_path)

            # Check file extension
            file_extension = file_path.split(".")[-1].lower()

            # Process different file types
            try:
                if file_extension == "dta":
                    df = pd.read_stata(file_path)
                elif file_extension == "csv":
                    df = pd.read_csv(file_path)
                elif file_extension in ["xls", "xlsx"]:
                    df = pd.read_excel(file_path)
                else:
                    # Unsupported file type
                    QMessageBox.warning(self, "Unsupported File", "This file format is not supported.")
                    return
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while reading the file: {str(e)}")
                return

            # Create a label to display the file name
            self.file_label.setText(file_path.split("/")[-1])

            # Save DataFrame as CSV file
            script_dir = os.path.dirname(os.path.dirname(__file__))
            output_file_path = os.path.join(script_dir, "data/dataset.csv")
            df.to_csv(output_file_path, index=False)
            print("DataFrame saved as CSV:", output_file_path)