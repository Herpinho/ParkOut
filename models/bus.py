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
    def remove_bus(self,bus):
        #TEMPORARY TESTING TOOL
        del bus