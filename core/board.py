import random

from PySide6.QtCore import QObject
from openpyxl.utils import rows_from_range
from rich import columns
from tensorflow.python.ops.metrics_impl import false_negatives
from models.passenger import Passenger
from models.bus import Bus
from utils.config import global_options
class Board(QObject):
   ## board_updated = Signal()
    def __init__(self, rows = 10, cols = 10, num_platforms = 10):
        super().__init__()
        self.rows = rows
        self.max_points = 0
        self.cols= cols
        self.num_platforms = num_platforms
        self.point_count = 0
        self.grid = [[None for _ in range (cols)] for _ in range(rows)]

        self.platforms = [None for _ in range(num_platforms)]
        self.bus_count = global_options.bus_count
        self.buses = []
        self.passenger_list = []
        self.initialize_board()
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
        random.shuffle(self.passenger_list)
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
                self.passenger_list.extend(self.generate_passengers(bus))
                return True
            return False

    def generate_passengers(self,bus):
        passengers = []

        for _ in range(bus.capacity):
            passenger = Passenger (
                color = bus.color
            )
            print(f"{passenger.color} created")
            passengers.append(passenger)
            self.max_points += 1

        return passengers

    def remove_passengers(self,bus,passengers):
        count = bus.capacity
        color = bus.color
        removed = 0
        print(count)
        for passenger in passengers[:]:
            print(passenger)
            if passenger.color == color and removed < count:
                removed += 1
                print(removed,passenger.color)
                passengers.remove(passenger)
                self.passenger_list.remove(passenger)
                self.point_count +=1


