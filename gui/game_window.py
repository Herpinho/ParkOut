from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
from gui.bus_segment_item import BusSegmentItem
from gui.main_window import MainWindow
from utils.config import global_options
from core.board import Board
class GameWindow(QMainWindow):
    CELL_SIZE = 60
    #
    def __init__(self, main_window):
        super().__init__()
        self.passenger_option = global_options.passenger_count
        self.main_window = main_window
        self.setWindowTitle("ParkOut - in Game")
        self.showMaximized()
        self.setStyleSheet("background-color:rgb(55, 62, 74);")
        self.board = Board(rows = 10, cols = 10)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.displayed_passengers = []
        self.update_displayed_passengers()
        self.draw_board()
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.view)
        main_menu_button = QPushButton("Back to Menu", self)
        main_menu_button.setStyleSheet(
            "background-color: rgb(173, 29, 37);"
            "border-radius: 5px;"
            "border-style: solid;"
            "border-width: 2px;"
            "border-color: rgb(59, 5, 8);"
            "color: black;"
            "font-size: 15px;"
            "padding: 10px;"
        )
        main_menu_button.clicked.connect(self.main_menu)

        layout.addWidget(main_menu_button, alignment=Qt.AlignBottom)

        self.setCentralWidget(central_widget)
    def draw_board(self):
        self.scene.clear()
        terminal_width = self.CELL_SIZE * 2
        board_offset_x = terminal_width
        terminal_rect = QRectF(0, 0, terminal_width, self.board.rows * self.CELL_SIZE)
        terminal_item = self.scene.addRect(terminal_rect)
        terminal_item.setBrush(QBrush(QColor("#cccccc")))  # Light gray
        terminal_item.setPen(QPen(Qt.black, 2))
        terminal_item.setZValue(-1)

        passenger_diameter = 30
        margin = 10
        spacing = 10
        for i, passenger in enumerate(self.displayed_passengers):
            y = margin + i * (passenger_diameter + spacing)
            ellipse = self.scene.addEllipse(10, y, passenger_diameter, passenger_diameter)
            ellipse.setBrush(QBrush(passenger.color))
            ellipse.setPen(QPen(Qt.black))
            ellipse.setZValue(1)
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                x = board_offset_x + col * self.CELL_SIZE

                rect = QRectF(x, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                rect_item = self.scene.addRect(rect)
                rect_item.setPen(Qt.NoPen)
        grid_width = self.board.cols * self.CELL_SIZE
        grid_height = self.board.rows * self.CELL_SIZE
        outer_rect = QRectF(board_offset_x, 0, grid_width, grid_height)
        border_item = self.scene.addRect(outer_rect)
        border_pen = QPen(Qt.blue)
        border_pen.setWidth(3)
        border_item.setPen(border_pen)
        border_item.setBrush(Qt.NoBrush)
        scene_width = board_offset_x + self.board.cols * self.CELL_SIZE
        scene_height = self.board.rows * self.CELL_SIZE
        self.scene.setSceneRect(0, 0, scene_width, scene_height)
        self.view.setSceneRect(self.scene.sceneRect())
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                bus = self.board.grid[row][col]
                if bus:
                    x = board_offset_x + col * self.CELL_SIZE
                    y = row * self.CELL_SIZE
                    height = self.CELL_SIZE
                    width = self.CELL_SIZE

                    # Desenha o autocarro (retângulo)
                    rect_item = BusSegmentItem(row, col, bus, self, x, y, width, height)
                    rect_item.setBrush(QBrush(QColor(bus.color)))
                    rect_item.setZValue(1)
                    self.scene.addItem(rect_item)

                    # Desenha a seta (triângulo)
                    arrow = QPolygonF()

                    center_x = x + width / 2
                    center_y = y + height / 2
                    arrow_size = 20

                    if bus.direction == "up":
                        arrow.append(QPointF(center_x, center_y - arrow_size))
                        arrow.append(QPointF(center_x - arrow_size / 2, center_y))
                        arrow.append(QPointF(center_x + arrow_size / 2, center_y))
                    elif bus.direction == "down":
                        arrow.append(QPointF(center_x, center_y + arrow_size))
                        arrow.append(QPointF(center_x - arrow_size / 2, center_y))
                        arrow.append(QPointF(center_x + arrow_size / 2, center_y))
                    elif bus.direction == "left":
                        arrow.append(QPointF(center_x - arrow_size, center_y))
                        arrow.append(QPointF(center_x, center_y - arrow_size / 2))
                        arrow.append(QPointF(center_x, center_y + arrow_size / 2))
                    elif bus.direction == "right":
                        arrow.append(QPointF(center_x + arrow_size, center_y))
                        arrow.append(QPointF(center_x, center_y - arrow_size / 2))
                        arrow.append(QPointF(center_x, center_y + arrow_size / 2))

                    arrow_item = QGraphicsPolygonItem(arrow)
                    arrow_item.setBrush(QBrush(Qt.black))
                    arrow_item.setZValue(2)
                    self.scene.addItem(arrow_item)

    def update_displayed_passengers(self):
        self.displayed_passengers = self.board.passenger_list[:self.passenger_option]
    def main_menu(self):
        self.hide()
        self.main_window.show()

    def can_move_until_exit(self,bus):
        row, col = bus.row, bus.col

        if bus.direction == 'right':
            if col+1>=self.board.cols:
                self.board.grid[row][col] = None
                bus.remove_bus(bus)
                self.board.remove_passengers(bus,self.displayed_passengers)
                self.update_displayed_passengers()
                self.board.bus_count -=1
            elif col + bus.length >= self.board.cols:
                self.board.grid[row][col]=None
                bus.col = col + 1

            elif self.board.grid[row][col + bus.length] is None:
                self.board.grid[row][col]=None
                self.board.grid[row][col+bus.length]=bus
                bus.col = col+1


        elif bus.direction == 'left':
            print(col)

            if col<=0:
                bus.remove_bus(bus)
                self.board.grid[row][col] = None
                self.board.remove_passengers(bus,self.displayed_passengers)
                self.update_displayed_passengers()
                self.board.bus_count -=1
            elif col - bus.length < 0:
                self.board.grid[row][col]=None
                bus.col = col - 1

            elif self.board.grid[row][col-bus.length] is None:
                self.board.grid[row][col]=None
                self.board.grid[row][col-bus.length]=bus
                bus.col = col-1

        elif bus.direction == 'down':
            if row+1>=self.board.rows:
                bus.remove_bus(bus)
                self.board.grid[row][col] = None
                self.board.remove_passengers(bus,self.displayed_passengers)
                self.update_displayed_passengers()
                self.board.bus_count -= 1
            elif row + bus.length >= self.board.rows:
                self.board.grid[row][col]=None
                bus.row = row +1

            elif self.board.grid[row+ bus.length][col] is None:
                self.board.grid[row][col]=None
                self.board.grid[row+bus.length][col]=bus
                bus.row = row + 1

        elif bus.direction == 'up':
            if row<=0:
                bus.remove_bus(bus)
                self.board.grid[row][col] = None
                self.board.remove_passengers(bus,self.displayed_passengers)
                self.update_displayed_passengers()
                self.board.bus_count -=1
            elif row - bus.length < 0:
                self.board.grid[row][col]=None
                bus.row = row -1

            elif self.board.grid[row - bus.length][col] is None:
                self.board.grid[row][col] = None
                self.board.grid[row - bus.length][col] = bus
                bus.row = row - 1


        self.draw_board()
        if self.board.bus_count == 0:
            self.game_end()
    def game_end(self):
        score = QMessageBox()
        score.setWindowTitle("Game Over")
        score.setText(f"Final Score: {self.board.point_count} out of {self.board.max_points}")
        score.setStandardButtons(QMessageBox.Ok)
        score.resize(QSize(200, 100))
        score.exec()

        self.main_menu()

