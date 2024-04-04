from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import importlib

class ShowSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.current_widget = None

    def update_data(self, module_name, class_name="Page"):
        # Remove the current widget if it exists
        if self.current_widget:
            self.layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()

        # Dynamically import the module
        module = importlib.import_module(f"pages.{module_name}.page")

        # Access the Page class from the imported module
        Page = getattr(module, class_name)

        # Create and add the new widget
        page = Page()
        self.layout.addWidget(page)
        self.current_widget = page