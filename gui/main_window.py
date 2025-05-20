from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ParkOut")
        self.resize(800, 600)
        self.setStyleSheet("background-color:rgb(55, 62, 74);")
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        title = QLabel("ParkOut")
        title.setStyleSheet("color:rgb(255,255,255);"
                            "padding-left:10px;"
                            "padding-right:10px;"
                            "font-size:100px;")
        title.setBaseSize(QSize(50, 50))
        title.setAlignment(Qt.AlignCenter)

        start_game_button = QPushButton("Start")
        start_game_button.setStyleSheet("background-color:rgb(84, 161, 80);"
                                        " border-radius:62px; "
                                        "padding:5px;"
                                        "font-size:60px;"
                                        "")
        start_game_button.setFixedSize(350, 125)
        start_game_button.clicked.connect(self.start_game)
        exit_game_button = QPushButton("Exit")
        exit_game_button.setFixedSize(150, 60)
        exit_game_button.setStyleSheet("background-color:rgb(173, 29, 37);"
                                        
                                        "padding:5px;"
                                        "font-size:40px;"
                                        "transparent:true;"
                                       "border-radius: 30px;"
                                       )
        exit_game_button.clicked.connect(self.exit_game)
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(start_game_button,alignment=Qt.AlignCenter)
        layout.addWidget(exit_game_button,alignment=Qt.AlignCenter)
        self.setCentralWidget(central_widget)
        self.game_window = None
    def exit_game(self):
        self.close()
    def start_game(self):
        from gui.game_window import GameWindow
        self.hide()
        self.game_window = GameWindow(self)
        self.game_window.show()

