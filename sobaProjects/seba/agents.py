from soba.agents.agent import ContinuousOccupant
from soba.agents.agent import Agent
import random
import sys

class EmergencyOccupant(ContinuousOccupant):

    def __init__(self, unique_id, model, json):
        super().__init__(unique_id, model, json)

        self.type = json['type']
        self.family = []
        self.alive = True
        self.life = 3
        self.foundChildren = []
        strategies = ['safest', 'uncrowded', 'nearest', 'lessassigned']
        self.exitGateStrategy = 'safest'
        self.smartModel = False
        self.unavailableDoors = []
        self.stateOne = self.state
        self.out = True
        self.alreadyCreated = False
        self.inbuilding = False
        self.initmove = True

    def makeMovement(self):
        super().makeMovement()
        self.getFOV()

    def makeEmergencyAction(self):
        self.N = 0
        if self.type == 'parent':
            self.pos_to_go = self.pos
            if len(self.foundChildren) == len(self.family):
                self.movements = self.getExitGate()
            else:
                notSelected = True
                child = False
                while notSelected:
                    child = random.choice(self.family)
                    if child not in self.foundChildren:
                        notSelected = False
                self.pos_to_go = child.pos
                self.movements = super().getWay()
        elif self.type == 'child':
            self.pos_to_go = self.pos
            self.movements = [self.pos_to_go]
        else:
            self.movements = self.getExitGate()

    def getUncrowdedGate(self):
        fewerPeople = 1000000
        doorAux = ''
        for door in self.model.outDoors:
            nPeople = 0
            x, y = door.pos
            for xAux in range (-4, 4):
                for yAux in range(-4, 4):
                    items = self.model.grid.get_items_in_pos((x + xAux, y + yAux))
                    for item in items:
                        if isinstance(item, EmergencyOccupant):
                            nPeople = nPeople + 1
            if fewerPeople > nPeople:
                doorAux = door
        return doorAux.pos

    def getSafestGate(self):
        longPath = 0
        doorAux = ''
        for door in self.model.outDoors:
            for fire in self.model.FireControl.limitFire:
                path = super().getWay(door.pos, fire.pos)
                if len(path) > longPath:
                    longPath = len(path)
                    doorAux = door
        return doorAux.pos

    def getNearestGate(self):
        shortPath = 1000000
        doorAux = ''
        for door in self.model.outDoors:
            path = super().getWay(self.pos, door.pos)
            if shortPath > len(path):
                shortPath = len(path)
                pathReturn = path
                doorAux = door
        return doorAux.pos

    def getLessAssignedGate(self):
        pass

    def getExitGate(self):
        if self.smartModel:
            if self.exitGateStrategy == 'uncrowded':
                self.pos_to_go = self.getUncrowdedGate()
            elif self.exitGateStrategy == 'safest':
                self.pos_to_go = self.getSafestGate()
            elif self.exitGateStrategy == 'nearest':
                self.pos_to_go = self.getNearestGate()
            elif self.exitGateStrategy == 'lessassigned':
                self.pos_to_go = self.getLessAssignedGate()
            else:
                self.pos_to_go = self.pos_to_go
        else:
             self.pos_to_go = self.getNearestGate()
        pathReturn = super().getWay()
        return pathReturn

    def fireInMyFOV(self):
        for firePos in self.model.FireControl.fireExpansion:
            if firePos in self.movements and self.posInMyFOV(firePos):
                return True
        return False

    def getPosFireFOV():
        others = []
        for pos in self.fov:
            if pos in self.model.FireControl.fireExpansion:
                others.append(pos)
        return others

    def step(self):
        if self.alive == True:
            if self.pos == self.pos_to_go and self.out == False:
                self.model.reportStop(self)
                self.initmove = True
            if self.model.emergency:
                if self.pos != self.pos_to_go:
                    if self.fireInMyFOV():
                        super().getWay(others = self.getPosFireFOV())
                    self.makeMovement()
                else:
                    if self.pos in self.model.outDoors:
                        pass
                    else:
                        self.makeEmergencyAction()
            else:
                super().step()
        else:
            pass

class Fire():

    def __init__(self, model, pos):
        self.pos = pos
        model.grid.place_item(self, pos)
        self.grade = 1

    def harmOccupant(self, occupant):
        if occupant.life > self.grade:
            occupant.life = occupant.life - self.grade
        else:
            occupant.life = 0
            occupant.alive = False

class FireControl(Agent):

    def __init__(self, unique_id, model, posInit, expansionRate = 1/600, growthRate = 1/600):
        super().__init__(unique_id, model)
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
            doorsPoss = self.model.obtacles['doors']
            for pos in posAdj:
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
        for occupant in self.model.occupants:
            fire = self.getFirePos(occupant.pos)
            if fire != False:
                fire.harmOccupant(occupant)
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