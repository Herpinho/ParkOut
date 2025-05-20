from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
from gui.bus_segment_item import BusSegmentItem
from gui.main_window import MainWindow
from core.board import Board
class GameWindow(QMainWindow):
        CELL_SIZE = 80
        def __init__(self, main_window):
            super().__init__()
            self.main_window = main_window
            self.setWindowTitle("ParkOut - Jogo")
            self.resize(800, 600)
            self.setStyleSheet("background-color:rgb(55, 62, 74);")

            self.board = Board(rows = 10, cols = 10)

            self.scene = QGraphicsScene()
            self.view = QGraphicsView(self.scene)
            self.setCentralWidget(self.view)

            self.draw_board()

        def draw_board(self):
            self.scene.clear()

            for row in range(self.board.rows):
                for col in range(self.board.cols):
                    rect = QRectF(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                    self.scene.addRect(rect)

            for row in range(self.board.rows):
                for col in range(self.board.cols):
                    bus = self.board.grid[row][col]
                    if bus:
                        x = col * self.CELL_SIZE
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

        def main_menu(self):
            self.hide()
            self.main_window.show()

        def can_move_until_exit(self,bus):
            row, col = bus.row, bus.col

            if bus.direction == 'right':
                if col+1>=self.board.cols:
                    self.board.grid[row][col] = None
                    bus.remove_bus(bus)

                    #bus delivered
                    #get passengers
                    #increase some kind of score counter
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
                    #bus delivered
                    #get passengers
                    #remove bus
                    #increase some kind of score counter
                elif col - bus.length < 0:
                    self.board.grid[row][col]=None
                    bus.col = col - 1

                elif self.board.grid[row][col-bus.length] is None:
                    self.board.grid[row][col]=None
                    self.board.grid[row][col-bus.length]=bus
                    bus.col = col-1

            elif bus.direction == 'down':
                if row+1>=self.board.cols:
                    bus.remove_bus(bus)
                    self.board.grid[row][col] = None
                    #bus delivered
                    #get passengers
                    #remove bus
                    #increase some kind of score counter
                elif row + bus.length >= self.board.rows:
                    self.board.grid[row][col]=None
                    bus.row = row +1

                elif self.board.grid[row+ bus.length][col] is None:
                    self.board.grid[row][col]=None
                    self.board.grid[row+bus.length][col]=bus
                    bus.row = row + 1

            elif bus.direction == 'up':
                print(col)
                if col-1<=0:
                    bus.remove_bus(bus)
                    self.board.grid[row][col] = None
                    #bus delivered
                    #get passengers
                    #remove bus
                    #increase some kind of score counter
                elif row - bus.length < 0:
                    self.board.grid[row][col]=None
                    bus.row = row -1

                elif self.board.grid[row - bus.length][col] is None:
                    self.board.grid[row][col] = None
                    self.board.grid[row - bus.length][col] = bus
                    bus.row = row - 1


            self.draw_board()