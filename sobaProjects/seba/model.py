from soba.model.model import ContinuousModel
from agents import EmergencyOccupant
from agents import FireControl
import random
import datetime as dt
import ramenScript as ramen

class SEBAModel(ContinuousModel):

    def __init__(self, width, height, jsonMap, jsonsOccupants, seed, scale = 0.5):
        self.parents = []
        self.children = []

        super().__init__(width, height, jsonMap, jsonsOccupants, seed, scale)

        self.emergency = False
        self.FireControl = False
        self.fireTime = dt.datetime(2017, 10, 1, 1, 0, 0, 0)
        self.outDoors = []
        self.getOutDoors()
        self.make = False

    def getOutDoors(self):
        for poi in self.pois:
            if poi.id == 'out':
                self.outDoors.append(poi)

    def createOccupants(self, jsonsOccupants):
        for json in jsonsOccupants:
            for n in range(0, json['N']):
                a = EmergencyOccupant(n, self, json)
                self.occupants.append(a)
                if json['type'] == 'child':
                    self.children.append(a)
                else:
                    self.parents.append(a)
                a.color = random.choice(['blue', 'red', 'yellow', 'brown'])
        for a in self.parents:
            if len(self.children)>0:
                ch = random.choice(self.children)
                self.children.remove(ch)
                a.family.append(ch)

    def isThereFire(self, pos):
        for fire in self.FireControl:
            if fire.pos == pos:
                return True
        return False

    def informEmergency(self):
        for occupant in self.occupants:
            occupant.makeEmergencyAction()

    def step(self):
        if self.clock.clock > dt.datetime(2017, 10, 1, 0, 0, 30, 0):
            self.make = True
            ramen.generateJSON()
        if self.clock.clock >= self.fireTime and not self.emergency:
            self.FireControl = FireControl(100000, self, random.choice(self.pois).pos)
            self.informEmergency()
            self.emergency = True
        super().step()

    def reportCreation(self, agent, rotation):
        ramen.createAgent(agent, self.NStep, agent.pos, rotation, sentiment = "happiness")

    def reportExit(self, agent):
        ramen.removeAgent(agent, self.NStep)

    def reportMovement(self, agent, direction):
        ramen.addAgentMovement(agent, self.NStep, direction, agent.speed)

    def reportStop(self, agent):
        ramen.stopAgent(agent, self.NStep)
