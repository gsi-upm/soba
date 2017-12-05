class GeneralItem():

    def __init__(self, model, pos, color = None):
        self.pos = pos
        model.grid.place_item(self, pos)
        self.color = 'grey' if color == None else color

class Door():

    def __init__(self, model, pos1, pos2, rot, state = True):
        self.state = state
        self.pos1 = pos1
        self.pos2 = pos2
        self.rot = rot

    def open(self):
        self.state = True

    def close(self):
        self.state = False

class Wall():

    def __init__(self, block1, block2, block3, color = None):
        self.block1 = block1
        self.block2 = block2
        self.block3 = block3
        self.color = 'brown' if color == None else color

class Poi():

    def __init__(self, model, pos, ide, share = True, color = None):
        self.pos = pos
        self.id = ide
        model.grid.place_item(self, pos)
        self.used = False
        self.share = share
        self.color = 'green' if color == None else color