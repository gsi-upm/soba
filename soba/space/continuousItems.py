class GeneralItem():

    def __init__(self, model, pos):
        self.pos = pos
        model.grid.place_item(self, pos)

class Door():

    def __init__(self, model, pos, rot, state = True):
        self.state = state
        self.pos = pos
        self.rot = rot
        model.grid.place_item(self, pos)

    def open(self):
        self.state = True

    def close(self):
        self.state = False

class Wall():

    def __init__(self, block1, block2, block3):
        self.block1 = block1
        self.block2 = block2
        self.block3 = block3

class Poi():

    def __init__(self, model, pos, ide, share = True):
        self.pos = pos
        self.id = ide
        model.grid.place_item(self, pos)
        self.used = False
        self.share = share