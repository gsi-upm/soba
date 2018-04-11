from soba.agents.continuousOccupant import ContinuousOccupant
import random
import sys
import soba.agents.resources.aStar as aStar
import numpy as np

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
        self.speedEmergency = 1.38 if not json.get('speedEmergency') else eval(json.get('speedEmergency'))
        self.parentAsos = False

    def makeMovement(self):
        super().makeMovement()
        if self.model.emergency:
            self.getFOV()

    def makeEmergencyAction(self):
        self.speed = self.speedEmergency
        self.N = 0
        self.markov = False
        self.timeActivity = 0
        if self.children:
            child = random.choice(self.children)
            self.pos_to_go = child.pos
            self.movements = super().getWay()
        elif not self.adult:
            if self.alone:
                self.pos_to_go = self.pos
                self.movements = [self.pos_to_go]
        else:
            self.movements = self.getExitGate()

    def getExitGate(self):
        if True: #self.smartModel:
            if self.exitGateStrategy == 'uncrowded':
                self.pos_to_go = self.model.getNearestGate(self)
                self.model.uncrowdedStr.append(self)
            elif self.exitGateStrategy == 'safest':
                self.pos_to_go = self.model.getSafestGate(self)
            elif self.exitGateStrategy == 'nearest':
                self.pos_to_go = self.model.getNearestGate(self)
            elif self.exitGateStrategy == 'lessassigned':
                self.pos_to_go = self.model.getLessAssignedGate()
            else:
                self.pos_to_go = self.model.getNearestGate()
        else:
            self.pos_to_go = self.model.getNearestGate(self)
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
        if self.alive == True:
            if self.model.emergency:
                self.markov = False
                self.timeActivity = 0
                if self.parentAsos:
                    if not self.model.nearPos(self.parentAsos.pos, self.pos):
                        self.pos_to_go = self.parentAsos.pos
                        super().getWay()
                        self.N = 0
                elif self.children:
                    posC = self.model.getOccupantsPos(self.movements[self.N])
                    if posC and posC not in self.model.exits:
                        posC = posC[0]
                        if posC in self.children:
                            posC.alone = False
                            for parent in posC.parents:
                                if posC in parent.children:
                                    parent.foundChildren.append(posC)
                                    parent.children.remove(posC)
                            posC.parentAsos = self
                            for parent in posC.parents:
                                if parent.pos_to_go == posC.pos:
                                    parent.makeEmergencyAction()
                if self.pos != self.pos_to_go:
                    if self.fireInMyFOV():
                        super().getWay(others = self.getPosFireFOV())
                    super().step()
                else:
                    if self.pos not in self.model.exits:
                        self.makeEmergencyAction()
            else:
                super().step()
        else:
            pass