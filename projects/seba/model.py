from occupant import EmergencyOccupant
from fire import FireControl
import random
import datetime as dt
from soba.models.continuousModel import ContinuousModel
from time import time

class SEBAModel(ContinuousModel):

    def __init__(self, width, height, jsonMap, jsonsOccupants, sebaConfiguration, seed = int(time())):
        super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed, timeByStep = 60)

        self.adults = []
        self.children = []
        self.emergency = False
        self.FireControl = False
        today = dt.date.today()
        self.fireTime = dt.datetime(today.year, today.month, 1, 9, 0, 0, 0)
        self.outDoors = []
        self.getOutDoors()
        self.make = False
        self.families = []
        self.familiesJson = sebaConfiguration.get('families')
        self.createOccupants(jsonsOccupants)

    def getOutDoors(self):
        for poi in self.pois:
            if poi.id == 'out':
                self.outDoors.append(poi)

    def createOccupants(self, jsonsOccupants):
        for json in jsonsOccupants:
            for n in range(0, json['N']):
                a = EmergencyOccupant(n, self, json)
                self.occupants.append(a)
                self.adults.append(a)
        if self.familiesJson:
            for f in self.familiesJson:
                nA = 0
                nC = 0
                n = 0
                if f.get('N') and f.get('adult'):
                    n = f.get('N')
                    nA = f.get('adult')
                    nC = n - nA
                if f.get('adult') and f.get('child'):
                    nA = f.get('adult')
                    nC = f.get('child')
                if f.get('N') and f.get('child'):
                    nC = f.get('child')
                    n = f.get('N')
                    nA = n - nC
                children = []
                for j in range(0, nC):
                    ch = random.choice(self.adults)
                    children.append(ch)
                    ch.adult = False
                    self.adults.remove(ch)
                    self.children.append(ch)
                for j in range(0, nA):
                    ad = random.choice(self.adults)
                    while ad.children:
                        ad = random.choice(self.adults)
                    ad.children = children

    def isThereFire(self, pos):
        for fire in self.FireControl:
            if fire.pos == pos:
                return True
        return False

    def informEmergency(self):
        for occupant in self.occupants:
            occupant.makeEmergencyAction()

    def harmOccupant(self, occupant, fire):
        if occupant.life > fire.grade:
            occupant.life = occupant.life - fire.grade
        else:
            occupant.life = 0
            occupant.alive = False

    def step(self):
        if self.clock.clock.hour > 13:
            self.finishSimulation = True
        if (self.clock.clock >= self.fireTime) and not self.emergency:
            self.FireControl = FireControl(100000, self, random.choice(self.pois).pos)
            self.informEmergency()
            self.emergency = True
        super().step()
        if self.emergency:
            for occupant in self.occupants:
                fire = self.FireControl.getFirePos(occupant.pos)
                if fire != False:
                    self.harmOccupant(occupant, fire)