from soba.agents.continuousOccupant import ContinuousOccupant
import random
import sys
import soba.agents.resources.aStar as aStar

class EmergencyOccupant(ContinuousOccupant):

    def __init__(self, unique_id, model, json):
        super().__init__(unique_id, model, json)

        self.type = json['type']
        self.children = []
        self.parents = []
        self.alive = True
        self.life = 3
        self.foundChildren = []
        strategies = ['safest', 'uncrowded', 'nearest']
        self.exitGateStrategy = json.get('strategy') or 'nearest'
        self.smartModel = False
        self.unavailableDoors = []
        self.stateOne = self.state
        self.out = True
        self.alreadyCreated = False
        self.inbuilding = False
        self.initmove = True
        self.adult = True
        self.alone = True

    def makeMovement(self):
        super().makeMovement()
        if self.model.emergency:
            self.getFOV()

    def makeEmergencyAction(self):
        self.N = 0
        self.markov = False
        self.timeActivity = 0
        if self.children:
            self.pos_to_go = self.pos
            if len(self.foundChildren) == len(self.children):
                self.movements = self.getExitGate()
            else:
                notSelected = True
                child = False
                while notSelected:
                    child = random.choice(self.children)
                    if child not in self.foundChildren:
                        notSelected = False
                self.pos_to_go = child.pos
                self.movements = super().getWay()
        elif not self.adult:
            self.pos_to_go = self.pos
            self.movements = [self.pos_to_go]
        else:
            self.movements = self.getExitGate()

    def getUncrowdedGate(self):
        fewerPeople = 1000000
        doorAux = False
        for door in self.model.outDoors:
            nPeople = 0
            x, y = door.pos
            for xAux in range (-10, 0):
                for yAux in range(-10, 10):
                    if self.model.xyInGrid(x + xAux, y + yAux):
                        items = self.model.grid.get_cell_list_contents((x + xAux, y + yAux))
                        for item in items:
                            if isinstance(item, EmergencyOccupant) and item.inbuilding:
                                nPeople = nPeople + 1
            if fewerPeople > nPeople:
                doorAux = door
                fewerPeople = nPeople
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
        doorAux = False
        for door in self.model.outDoors:
            path = super().getWay(self.pos, door.pos)
            if shortPath > len(path):
                shortPath = len(path)
                pathReturn = path
                doorAux = door
        return doorAux.pos

    def getExitGate(self):
        if True: #self.smartModel:
            if self.exitGateStrategy == 'uncrowded':
                self.pos_to_go = self.getUncrowdedGate()
            elif self.exitGateStrategy == 'safest':
                self.pos_to_go = self.getSafestGate()
            elif self.exitGateStrategy == 'nearest':
                self.pos_to_go = self.getNearestGate()
            elif self.exitGateStrategy == 'lessassigned':
                self.pos_to_go = self.getLessAssignedGate()
            else:
                self.pos_to_go = self.getNearestGate()
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

    def changeSchedule(self):
        if self.model.emergency:
            return False
        super().changeSchedule()

    def step(self):
        print(self.unique_id, self.pos_to_go, self.pos, self.N)
        if self.alive == True:
            if self.model.emergency:
                self.markov = False
                self.timeActivity = 0
                if self.pos != self.pos_to_go:
                    if self.fireInMyFOV():
                        super().getWay(others = self.getPosFireFOV())
                    super().step()
            else:
                super().step()
        else:
            pass