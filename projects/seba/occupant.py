from soba.agents.continuousOccupant import ContinuousOccupant
import random
import sys
import soba.agents.resources.aStar as aStar
import numpy as np

class EmergencyOccupant(ContinuousOccupant):
    """
    
    This class enables to create occupants defined to work in an emergency modeling.
    This class inherits from the ContinuousOccupant class of SOBA.

    Attributes:
        Those Inherited from the ContinuousOccupant class of SOBA.
        children: Children associated with the occupant.
        parents: Parents associated with the occupant.
        alive: Current state of an occupant, live or not.
        life: Number of remaining life points of the occupant.
        foundChildren: Children associated with the occupant found by the occupant during a emergency.
        exitGateStrategy: strategy that is used to leave the building during a emergency.
        adult: Inform if the occupant is an adult.
        alone: Inform if the occupant has occupants who follow him.
        speedEmergency: Movement speed during an emergency.
        parentAsos: Familiar that the child occupant has to follow.
    
    Methods:
        fireInMyFOV: Check if there is fire in the FOV of the occupant.
        makeEmergencyAction: Method that is invoked when initiating an emergency to make the decision of response.
        getExitGate: Obtain the optimal way to evacuate the building according to an evacuation strategy.
        getPosFireFOV: Obtain the positions in the occupant's field of vision where there is fire.
        step: Method invoked by the Model scheduler in each step.
    
    """
    def __init__(self, unique_id, model, json):
        super().__init__(unique_id, model, json)

        self.children = []
        self.parents = []
        self.alive = True
        self.life = 3
        self.foundChildren = []
        strategies = ['safest', 'uncrowded', 'nearest']
        self.exitGateStrategy = json.get('strategy') or 'nearest'
        self.stateOne = self.state
        self.out = True
        self.alreadyCreated = False
        self.inbuilding = False
        self.initmove = True
        self.adult = True
        self.alone = True
        self.speedEmergency = 1.38 if not json.get('speedEmergency') else eval(json.get('speedEmergency'))
        self.parentAsos = False

    def makeEmergencyAction(self):
        """
        Method that is invoked when initiating an emergency to make the decision of response.
        If the occupant is a parent, he will look for his son. If he is a child, 
        he will wait for one of his parents. In any other case, a path is decided to leave the building.
        """
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
        '''
        Obtain the optimal way to evacuate the building according to an evacuation strategy.
            Return: List of positions (x, y)
        '''
        if True:
            if self.exitGateStrategy == 'uncrowded':
                self.pos_to_go = self.model.getNearestGate(self)
                self.model.uncrowdedStr.append(self)
            elif self.exitGateStrategy == 'safest':
                self.pos_to_go = self.model.getSafestGate(self)
            elif self.exitGateStrategy == 'nearest':
                self.pos_to_go = self.model.getNearestGate(self)
            elif self.exitGateStrategy == 'lessassigned':
                self.pos_to_go = self.model.getLessAssignedGate(self)
            else:
                self.pos_to_go = self.model.getNearestGate(self)
        else:
            self.pos_to_go = self.model.getNearestGate(self)
        pathReturn = super().getWay()
        return pathReturn

    def fireInMyFOV(self):
        """
        Check if there is fire in the FOV of the occupant.
            Return: Boolean
        """
        for firePos in self.model.FireControl.fireExpansion:
            if firePos in self.movements and self.posInMyFOV(firePos):
                return True
        return False

    def getPosFireFOV(self):
        """
        Obtain the positions in the occupant's field of vision where there is fire.
            Return: list of positions (x, y)
        """
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
        """Method invoked by the Model scheduler in each step."""
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
                        if self in self.model.occupEmerg:
                            self.model.occupEmerg.remove(self)
            else:
                super().step()
        else:
            pass