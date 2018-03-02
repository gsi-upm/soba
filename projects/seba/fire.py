import random
import sys
from mesa.agent import Agent
import soba.agents.resources.aStar as aStar

class Fire():

    def __init__(self, model, pos):
        self.pos = pos
        model.grid.place_agent(self, pos)
        self.grade = 1

class FireControl(Agent):

    def __init__(self, unique_id, model, posInit, expansionRate = 1/600, growthRate = 1/600):
        super().__init__(unique_id, model)
        self.model.schedule.add(self)
        self.fireExpansion = []
        self.limitFire = []
        self.expansionRate = expansionRate #m/s
        self.growthRate = growthRate
        self.N = 0
        self.movements = []
        self.costMovement = 0.5*(1/self.expansionRate)*(1/self.model.clock.timeByStep)
        self.costGrowth = 0.5*(1/self.growthRate)*(1/self.model.clock.timeByStep)
        self.createFirePos(posInit)

    def createFirePos(self, pos):
        f = Fire(self.model, pos)
        self.limitFire.append(f)
        self.fireExpansion.append(f)
        self.movements.append(pos)

    def getFirePos(self, pos):
        for fire in self.fireExpansion:
            if fire.pos == pos:
                return fire
        return False

    def expansionFire(self):
        fireExpansionAux = self.limitFire[:]
        n = 0
        for fire in fireExpansionAux:
            n = n +1
            self.limitFire.remove(fire)
            x, y = fire.pos
            posAdj = [(x + 1, y + 1), (x + 1, y), (x - 1, y), (x - 1, y - 1), (x, y + 1), (x, y - 1), (x - 1, y + 1), (x + 1, y - 1)]
            doorsPoss = aStar.doorsPoss
            for pos in posAdj:
                xaux, yaux = pos
                if self.model.xyInGrid(xaux, yaux):
                    cellPos = fire.pos
                    posAux = pos
                    move = True
                    for wall in self.model.walls:
                        if (cellPos in wall.block1 and posAux in wall.block1) or (cellPos in wall.block2 and posAux in wall.block2) or (cellPos in wall.block3 and posAux in wall.block3):
                            move = False
                    if not move:
                        for doorsPos in doorsPoss:
                            if ((cellPos in doorsPos) and (posAux in doorsPos)):
                                move = True
                    if move:
                        if not (pos in self.movements):
                            self.createFirePos(pos)

    def growthFire(self):
        for fire in self.fireExpansion:
            fire.grade = fire.grade + 1

    def step(self):
        if self.costGrowth > 0:
            self.costGrowth = self.costGrowth - 1
        else:
            self.growthFire()
            self.costGrowth = 0.5*(1/self.growthRate)*(1/self.model.clock.timeByStep)
        if self.costMovement > 0:
            self.costMovement = self.costMovement - 1
        else:
            self.expansionFire()
            self.costMovement = 0.5*(1/self.expansionRate)*(1/self.model.clock.timeByStep)