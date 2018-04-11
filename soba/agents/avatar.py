import random
import soba.agents.resources.aStar as aStar
import soba.agents.resources.fov as fov
import soba.visualization.ramen.performanceGenerator as ramen
from soba.agents.occupant import Occupant
import time

class Avatar(Occupant):

    def __init__(self, unique_id, model, initial_pos, color = 'red', initial_state='walking'):

        self.model = model
        self.unique_id = unique_id
        self.fov = []
        self.state = initial_state
        self.pos = initial_pos
        self.model.grid.place_agent(self, initial_pos)
        self.color = color
        self.shape = 'circle'
        self.speed = None
        self.movement = {}        
        self.movements = [self.pos]
        self.inbuilding = False

    def getWay(self, pos = None, pos_to_go = None, other = []):
        '''
        Invocation of the AStar resource to calculate the optimal path.
            Args:
                pos: Initial position, by default the current position of the occupant.
                pos_to_go: Final position, by default the value of the 'pos_to_go' attribute of the occupant.
                other: List of auxiliary positions given to be considered impenetrable by the occupants, 
                that is, they will not be used by the AStar.
            Return: List of positions (x, y).
        '''
        posSend = pos
        pos_to_goSend = pos_to_go
        if pos == None:
            posSend = self.pos
        if pos_to_go == None:
            pos_to_goSend = self.pos_to_go
        return aStar.getPathContinuous(self.model, posSend, pos_to_goSend, other)

    def posInMyFOV(self, pos):
        '''
        Check if the position is in my field of vision
            Args: 
                pos: Position to be checked
            Return: Boolean
        '''
        if pos in self.fov:
            return True
        return False

    def makeMovementAvatar(self, pos):
        '''Carry out a movement: displacement between cells or reduction of the movement cost parameter.'''
        self.model.grid.move_agent(self, pos)
        self.reportMovement()
        self.movements = [self.pos]
        self.checkLeaveArrive()
        self.getFOV()

    def reportMovement(self):
        pass

    def checkLeaveArrive(self):
        if not self.inbuilding:
            if self.model.ramenAux:
                ramen.reportCreation(self, 'E')
            self.inbuilding = True
            return
        if (self.pos in self.model.exits) and self.inbuilding:
            self.inbuilding = False
            if self.model.ramenAux:
                ramen.reportExit(self)
            return

    def getFOV(self):
        '''Calculation of the occupant's field of vision, registered in the attribute fov'''
        asciMap = self.model.asciMap
        fovMap, flag = fov.makeFOV(asciMap, self.pos)
        self.fov = []
        for index1, line in enumerate(fovMap):
            for index2, element in enumerate(line):
                if element == flag:
                    self.fov.append((index2, index1))

    def step(self):
        return