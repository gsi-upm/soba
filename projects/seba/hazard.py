import random
import sys
from mesa.agent import Agent
import soba.agents.resources.aStar as aStar


class Hazard():
    """
    This class enables to create fire object on a position. 
    The objects of this class are controlled by one FireControl object.

    Attributes:
        grade: Intensity level of the fire.
        pos: Fire position.
    """

    def __init__(self, model, pos):
        self.pos = pos
        model.grid.place_agent(self, pos)
        self.grade = 1

class HazardControl(Agent):
    """
    This class enables to create agents that control the hazard expansión, representing the emergency threat.

    Attributes:
        hazardExpansion: Set of hazard objects belonging to this hazardControl.
        limitiHazard: hazard objects that are in the limit to make the expansion.
        expansionRate: Rate of expansion of the threat.
        growthRate: Value of growth in intensity of the hazard.

    Methods:
        createHazardPos: Create a hazard object in a given position.
        gethazardPos: Get a hazard object in a position given.
        expansionhazard:  Make the expansion of hazard limits.
        growthhazard: Make the growth in intensity of the hazard.
        step: Method invoked by the Model scheduler in each step.
    """
    def __init__(self, unique_id, model, posInit, expansionRate = 1, growthRate = 1):
        super().__init__(unique_id, model)
        self.model.schedule.add(self)
        self.expansion = []
        self.limit = []
        self.expansionRate = expansionRate #m/s
        self.growthRate = growthRate
        self.N = 0
        self.movements = []
        self.costMovement = 0.5*(1/self.expansionRate)*(1/self.model.clock.timeByStep)
        self.costGrowth = 0.5*(1/self.growthRate)*(1/self.model.clock.timeByStep)
        self.createHazardPos(posInit)

    def createHazardPos(self, pos):
        """
        Create a hazard object in a given position.
            Args:
                pos: Position to put the hazard object as (x, y)
        """
        f = hazard(self.model, pos)
        self.hazard.append(f)
        self.expansion.append(f)
        self.movements.append(pos)

    def getHazardPos(self, pos):
        """
        Get a hazard object in a position given.
            Args: 
                pos: Position to be checked.
            Return: hazard object or False
        """
        for hazard in self.hazardExpansion:
            if hazard.pos == pos:
                return hazard
        return False

    def expansionHazard(self):
        """
        Make the expansion of hazard limits.
        """
        hazardExpansionAux = self.limitiHazard[:]
        n = 0
        for hazard in hazardExpansionAux:
            n = n +1
            self.limitiHazard.remove(hazard)
            x, y = hazard.pos
            posAdj = [(x + 1, y + 1), (x + 1, y), (x - 1, y), (x - 1, y - 1), (x, y + 1), (x, y - 1), (x - 1, y + 1), (x + 1, y - 1)]
            doorsPoss = aStar.doorsPoss
            for pos in posAdj:
                xaux, yaux = pos
                if self.model.xyInGrid((xaux, yaux)):
                    cellPos = hazard.pos
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
                            self.createHazardPos(pos)

    def growthHazard(self):
        """
        Make the growth in intensity of the hazard.
        """
        for hazard in self.hazardExpansion:
            hazard.grade = hazard.grade + 1

    def step(self):
        """
        Method invoked by the Model scheduler in each step.
        """
        if self.costGrowth > 0:
            self.costGrowth = self.costGrowth - 1
        else:
            self.growthHazard()
            self.costGrowth = 0.5*(1/self.growthRate)*(1/self.model.clock.timeByStep)
        if self.costMovement > 0:
            self.costMovement = self.costMovement - 1
        else:
            self.expansionHazard()
            self.costMovement = 0.5*(1/self.expansionRate)*(1/self.model.clock.timeByStep)