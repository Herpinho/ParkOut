import random

from PySide6.QtCore import QObject
from openpyxl.utils import rows_from_range
from rich import columns
from tensorflow.python.ops.metrics_impl import false_negatives

from models.bus import Bus

class Board(QObject):
   ## board_updated = Signal()
    def __init__(self, rows = 16, cols = 16, num_platforms = 4):
        super().__init__()
        self.rows = rows
        self.cols= cols
        self.num_platforms = num_platforms

        self.grid = [[None for _ in range (cols)] for _ in range(rows)]

        self.platforms = [None for _ in range(num_platforms)]
        self.bus_count= 6
        self.buses = []

        self.initialize_board()
        for bus in self.buses:
            print(vars(bus))
        print("Board grid:")
        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell is None:
                    row_str.append("Empty")
                else:
                    # Show bus color or some short identifier
                    row_str.append(cell.color[0].upper())  # first letter of color, uppercase
            print(" | ".join(row_str))
    def initialize_board(self):
        colors = ["red","white","yellow","green"]
        capacities = [4,6,8,12]

        for i in range(self.bus_count):
            color = random.choice(colors)
            capacity = random.choice(capacities)
            direction = random.choice(["up","down","left","right"])
            bus = Bus(color=color, capacity=capacity,direction=direction)

            placed = False
            attempts = 0
            while not placed and attempts < 100:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                if self.place_bus(bus,row, col):
                    placed = True
                attempts += 1

    def move_bus_to_platform(self,bus,platform_index):

        if platform_index < 0 or platform_index >= self.num_platforms:
            return False
        if self.platforms[platform_index] is not None:
            return False
        if not bus.can_board_passengers():
            return False

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] ==bus:
                    self.grid[r][c] = None

        self.platforms[platform_index] = bus
        bus.board_passengers()
        self.board_updated.emit()
        return True

    def remove_bus_from_platform(self, platform_index):
        if 0 <= platform_index < self.num_platforms:
            self.platforms[platform_index] = None
            self.board_updated.emit()

    def is_solved(self):
        return all(bus.boarded for bus in self.buses)


    def can_place_bus(self, row, col, length, direction):
        if direction == "up":
            if row - length + 1 < 0:
                return False
            for i in range(length):
                if self.grid[row - i][col] is not None:
                    return False
        elif direction == "down":
            if row + length > self.rows:
                return False
            for i in range(length):
                if self.grid[row + i][col] is not None:
                    return False
        elif direction == "left":
            if col - length + 1 < 0:
                return False
            for i in range(length):
                if self.grid[row][col - i] is not None:
                    return False
        elif direction == "right":
            if col + length > self.cols:
                return False
            for i in range(length):
                if self.grid[row][col + i] is not None:
                    return False
        else:
            return False
        return True


    def place_bus(self, bus, row, col):
            bus.length = int(bus.capacity / 2)  # assuming 4 passengers per tile

            if self.can_place_bus(row, col, bus.length, bus.direction):
                bus.col = col
                bus.row = row
                if bus.direction == "up":
                    for i in range(bus.length):
                        self.grid[row - i][col] = bus# move up vertically
                elif bus.direction == "down":
                    for i in range(bus.length):
                        self.grid[row + i][col] = bus  # move down vertically
                elif bus.direction == "left":
                    for i in range(bus.length):
                        self.grid[row][col - i] = bus  # move left horizontally
                elif bus.direction == "right":
                    for i in range(bus.length):
                        self.grid[row][col + i] = bus  # move right horizontally
                self.buses.append(bus)
                return True
            return False





