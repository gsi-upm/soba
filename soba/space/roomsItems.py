class Room():

    def __init__(self, name, conectedTo, dx, dy, pos = (0,0)):
        self.name = name
        self.conectedTo = conectedTo
        self.dx = dx
        self.dy = dy
        self.pos = pos
        self.roomsConected = []
        self.agentsInRoom = []
        self.walls = []
        self.entrance = None
        self.doors = []

class Door():

    def __init__(self, room1 = False, room2= False):
        self.state = False
        self.room1 = room1
        self.room2 = room2

    def open(self):
        self.state = True

    def close(self):
        self.state = False

class Wall():

    def __init__(self, room1 = False, room2 = False):
        self.room1 = room1
        self.room2 = room2