class Bus:
    def __init__(self,color:str, capacity: int, direction: str):
        self.color = color
        self.capacity = capacity
        self._direction = direction ## up down left right
        self.passengers = []
        self.boarded = False
        self.row = None
        self.col = None
        self.length = None

    @property
    def direction(self):
        return self._direction
    def add_passenger(self,passenger):
        if passenger.color != self.color:
            return False
        if len(self.passengers) >=self.capacity:
            return False
        self.passengers.append(passenger)
        return True

    def can_board_passengers(self):
        return len(self.passengers)<self.capacity

    def board_passengers(self):
        if self.can_board_passengers():
            self.boarded = True
    def get_direction(self):
        return self.direction
    def remove_bus(self,bus):
        #TEMPORARY TESTING TOOL
        del bus