from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtCore import Signal, QObject, Qt
from models.bus import *
from gui import game_window


class BusSegmentItem(QGraphicsRectItem):
    def __init__(self, row, col, bus, game_window, x, y, width, height):
        # Initialize QGraphicsRectItem with rectangle
        super().__init__(x, y, width, height)

        self.row = row
        self.col = col
        self.bus = bus
        self.game_window = game_window

        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        print(f"test at ({self.row},{self.col}) - BUS ID: {id(self.bus)} - BUS DIRECTION: {Bus.get_direction(self.bus)}")
        from gui.main_window import MainWindow
        if self.game_window:
            cells = self.game_window.can_move_until_exit(self.bus)

