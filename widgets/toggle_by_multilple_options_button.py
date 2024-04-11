from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QVBoxLayout


class ToggleByMultipleOptionsButton(QWidget):
    stateChanged = pyqtSignal(str)
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = []
        self.current_option = None

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.setSpacing(0)

        for option in options:
            if option == "\n":
                main_layout.addLayout(layout)
                layout = QHBoxLayout()  # Start a new horizontal layout
                layout.setSpacing(0)
            else:
                button = QPushButton(option)
                button.setCheckable(True)
                button.clicked.connect(self.on_button_clicked)
                layout.addWidget(button)
                self.buttons.append(button)
        main_layout.addLayout(layout)

    def on_button_clicked(self):
        sender = self.sender()
        if sender.isChecked():
            for button in self.buttons:
                if button is not sender:
                    button.setChecked(False)
            self.current_option = sender.text()
            self.stateChanged.emit(self.current_option)
        else:
            self.current_option = None

    def get_current_option(self):
        return self.current_option

    def set_state(self, option):
        """
        Set the state of the button group to the specified option.
        """
        for button in self.buttons:
            if button.text() == option:
                button.setChecked(True)
                self.current_option = option
                self.stateChanged.emit(option)
                break