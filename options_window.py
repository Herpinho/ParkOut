from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog
from utils.config import global_options

class OptionsWindow(QDialog):
    def __init__(self,parent = None):
        self.bus_input = 6
        self.passenger_input = 15
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.setMinimumSize(400,300)
        self.setStyleSheet("background-color:rgb(55, 62, 74);")
        layout = QVBoxLayout(self)
        title = QLabel("Options")
        title.setStyleSheet(
                            "padding:5px;"
                            "font-size:40px;"
                            )

        bus_option_label = QLabel("Bus count:")
        bus_input = QLineEdit()
        bus_input.setStyleSheet("background-color:rgb(55, 62, 74);")
        bus_input.setPlaceholderText("Bus count")
        bus_input.setFixedWidth(200)
        bus_input.setText(str(self.bus_input))

        passenger_option_label = QLabel("Passenger count:")
        passenger_input = QLineEdit()
        passenger_input.setStyleSheet("background-color:rgb(55, 62, 74);")
        passenger_input.setPlaceholderText("Passenger count")
        passenger_input.setFixedWidth(200)
        passenger_input.setText(str(self.passenger_input))

        apply_button = QPushButton("Apply")
        apply_button.setStyleSheet("background-color:rgb(84, 161, 80);")
        apply_button.clicked.connect(self.apply_settings)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color:rgb(173, 29, 37);")
        close_button.clicked.connect(self.close)

        layout.addWidget(title, alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(bus_option_label, alignment=Qt.AlignCenter | Qt.AlignLeft)
        layout.addWidget(bus_input, alignment=Qt.AlignCenter | Qt.AlignLeft)
        layout.addWidget(passenger_option_label, alignment=Qt.AlignCenter | Qt.AlignLeft)
        layout.addWidget(passenger_input, alignment=Qt.AlignCenter | Qt.AlignLeft)
        layout.addWidget(apply_button, alignment=Qt.AlignRight | Qt.AlignBottom)
        layout.addWidget(close_button, alignment=Qt.AlignLeft | Qt.AlignTop)
        self.bus_input = bus_input
        self.passenger_input = passenger_input
    def apply_settings(self):
        global_options.bus_count = int(self.bus_input.text())
        global_options.passenger_count = int(self.passenger_input.text())