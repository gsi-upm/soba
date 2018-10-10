from soba.agents.continuousOccupant import ContinuousOccupant
import random
import sys
import soba.agents.resources.aStar as aStar
import numpy as np
from avatar import EmergencyAvatar

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

        self.familiar = False
        self.children = []
        self.parents = []
        self.child = False
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
        self.speedEmergency = 1.38 if not json.get('speedEmergency') else json.get('speedEmergency')
        self.parentAsos = False
        self.shape = "circle"
        self.exclude = []
        self.fovCal = True if not json.get('fov') else json.get('fov')

    def makeEmergencyAction(self, exclude = []):
        """
        Method that is invoked when initiating an emergency to make the decision of response.
        If the occupant is a parent, he will look for his son. If he is a child, 
        he will wait for one of his parents. In any other case, a path is decided to leave the building.
        """
        self.speed = self.speedEmergency
        self.N = 0
        self.markov = False
        self.timeActivity = 0
        if self.children and not self.child:
            print("Tengo hijos asi que escojo uno")
            child = random.choice(self.children)
            print(child)
            self.pos_to_go = child.pos
            print(4, self.movements)
            self.movements = super().getWay()
            print(5, self.movements)
            self.child = child
            print("mis movimientos son estos porque voy a por mi hijo: ", self.movements)
        elif not self.adult:
            print("soy un niño")
            if self.alone:
                print("estoy solo asi que me quedo quieto, en la posición: ", self.pos)
                self.pos_to_go = self.pos
                self.movements = [self.pos_to_go]
        else:
            self.movements = self.getExitGate(exclude)

    def getExitGate(self, exclude = []):
        '''
        Obtain the optimal way to evacuate the building according to an evacuation strategy.
            Return: List of positions (x, y)
        '''
        if True:
            if self.exitGateStrategy == 'uncrowded':
                self.pos_to_go = self.model.getNearestGate(self, exclude)
                self.model.uncrowdedStr.append(self)
            elif self.exitGateStrategy == 'safest':
                self.pos_to_go = self.model.getSafestGate(self, exclude)
            elif self.exitGateStrategy == 'nearest':
                self.pos_to_go = self.model.getNearestGate(self, exclude)
            else:
                self.pos_to_go = self.model.getNearestGate(self, exclude)
        else:
            self.pos_to_go = self.model.getNearestGate(self)
        pathReturn = super().getWay(other = self.exclude)
        return pathReturn

    def fireInMyFOV(self):
        """
        Check if there is fire in the FOV of the occupant.
            Return: Boolean
        """
        for firePos in self.model.FireControl.fireMovements:
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
            if pos in self.model.FireControl.fireMovements:
                others.append(pos)
        return others

    def changeSchedule(self):
        if self.model.emergency:
            return False
        super().changeSchedule()

    def step(self):
        print(self.inbuilding)
        """Method invoked by the Model scheduler in each step."""
        if self.alive == True:
            if isinstance(self, EmergencyAvatar):
                return
            if self.model.emergency:
                if set(self.model.exits).issubset(self.exclude) or self.pos in self.model.exits:
                    if self in self.model.occupEmerg:
                        self.model.occupEmerg.remove(self)
                        return
                self.markov = False
                self.timeActivity = 0
                if self.parentAsos:
                    print("tengo padres asociados, que ya me han encontrado")
                    if not self.model.nearPos(self.parentAsos.pos, self.pos):
                        print("mi padre no está en una posición justo al lado a si que me muevo")
                        self.pos_to_go = self.parentAsos.pos
                        self.movements = super().getWay(other = self.exclude)
                        self.N = 0
                        print("")
                        if self.pos == self.movements[0]:
                            self.parentAsos = False
                            self.pos_to_go = self.pos
                            self.movements = [self.pos]
                            self.N = 0
                elif self.child:
                    print("tengo niño al que buscar")
                    print("Mis movimientos son estos: ", self.movements)
                    chi = self.model.getOccupantsPos(self.movements[self.N])
                    if chi:
                        print(1, self.movements)
                        chi = chi[0]
                        if chi.pos not in self.model.exits:
                            posChi = chi.pos
                            print("en la pos,", posChi)
                            chi.alone = False
                            for parent in chi.parents:
                                if chi in parent.children:
                                    parent.foundChildren.append(chi)
                                    parent.children.remove(chi)
                            chi.parentAsos = self
                            for parent in chi.parents:
                                if parent.pos_to_go == posChi:
                                    parent.child = False
                                    print(2, self.movements)
                                    parent.makeEmergencyAction()
                        else:
                            self.child = False
                            if chi in self.children:
                                self.children.remove(chi)
                            self.makeEmergencyAction()
                if self.pos != self.pos_to_go:
                    if self.fireInMyFOV():
                        self.exclude += self.getPosFireFOV()
                        self.movements = super().getWay(other = self.exclude)
                        self.N = 0
                        print("Calculo nueva ruta: ", self.movements)
                        if self.pos == self.movements[0]:
                            if self.adult:
                                if self.child:
                                    chi = self.model.getOccupantsPos(self.movements[self.N])
                                    if chi:
                                        chi = chi[0]
                                        if chi in self.children:
                                            self.children.remove(chi)
                                    self.child = False
                                self.exclude.append(self.pos_to_go)
                                self.makeEmergencyAction(self.exclude)
                                if self.pos == self.movements[0]:
                                    self.pos_to_go = self.pos
                                    self.movements = [self.pos]
                                    self.N = 0
                            else:
                                self.parentAsos = False
                                self.pos_to_go = self.pos
                                self.movements = [self.pos]
                                self.N = 0
                        else:
                            self.pos_to_go = self.movements[-1]
                    print("Estos son mis movimiento sahora: ", self.movements, 'y m pos a ir:', self.pos_to_go)
                    super().step()
                else:
                    if self.pos not in self.model.exits:
                        self.makeEmergencyAction()
                    else:
                        print(232312312323123123)
                        if self in self.model.occupEmerg:
                            self.model.occupEmerg.remove(self)
            else:
                super().step()
        else:
            if self in self.model.occupEmerg:
                self.model.occupEmerg.remove(self)