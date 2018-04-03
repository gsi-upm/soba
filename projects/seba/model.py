from occupant import EmergencyOccupant
from fire import FireControl
import random
import datetime as dt
from soba.models.continuousModel import ContinuousModel
from time import time
from ast import literal_eval as make_tuple
import listener as lstn

class SEBAModel(ContinuousModel):

	def __init__(self, width, height, jsonMap, jsonsOccupants, sebaConfiguration, seed = int(time())):
		lstn.setModel(self)
		super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed, timeByStep = 60)
		self.adults = []
		self.children = []
		self.emergency = False
		self.FireControl = False
		today = dt.date.today()
		self.fireTime = dt.datetime(today.year, today.month, 1, 8, 10, 0, 0)
		self.outDoors = []
		self.getOutDoors()
		self.make = False
		self.families = []
		self.familiesJson = sebaConfiguration.get('families')
		self.createOccupants(jsonsOccupants)
		self.uncrowdedStr = []

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
				elif f.get('adult') and f.get('child'):
					nA = f.get('adult')
					nC = f.get('child')
				elif f.get('N') and f.get('child'):
					nC = f.get('child')
					n = f.get('N')
					nA = n - nC
				children = []
				for j in range(0, nC):
					ch = random.choice(self.adults)
					while ch.children:
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
					for c in children:
						c.parents.append(ad)

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

	def getSafestGate(self, occupant):
		longPath = 0
		doorAux = ''
		for door in self.outDoors:
			for fire in self.FireControl.limitFire:
				path = occupant.getWay(door.pos, fire.pos)
				if len(path) > longPath:
					longPath = len(path)
					doorAux = door
		return doorAux.pos

	def getNearestGate(self, occupant):
		shortPath = 1000000
		doorAux = False
		for door in self.outDoors:
			path = occupant.getWay(occupant.pos, door.pos)
			if shortPath > len(path):
				shortPath = len(path)
				pathReturn = path
				doorAux = door
		return doorAux.pos

	def getUncrowdedGate(self):
		doorsN = {}
		for d in self.outDoors:
			doorsN[str(d.pos)] = 0
		for o in self.occupants:
			pos = o.pos_to_go
			doorsN[str(pos)] = doorsN[str(pos)] + 1
		for o in self.uncrowdedStr:
			pos = o.pos_to_go
			n = doorsN[str(pos)]
			naux = 100000
			doorPos = False
			for k, v in doorsN.items():
				if naux > v+1:
					doorPos = make_tuple(k)
					naux = v
			if doorPos:
				doorsN[str(doorPos)] = doorsN[str(doorPos)] + 1
				doorsN[str(o.pos_to_go)] = doorsN[str(o.pos_to_go)] - 1
				o.pos_to_go = doorPos
				o.movements = o.getWay()
				o.N = 0
			self.uncrowdedStr.remove(o)

	#API methods
	def getPositionsFire(self):
		data = []
		if not self.FireControl:
			return data
		for fire in self.FireControl.fireExpansion:
			data.append(fire.pos)
		return data

	def getExitWayAvatar(self, avatar_id, strategy = 'nearest'):
		a = self.getOccupantId(int(avatar_id))
		a.exitGateStrategy = strategy
		data = a.getExitGate()
		return data

	def step(self):
		if self.clock.clock.hour > 13:
			self.finishSimulation = True
		if (self.clock.clock >= self.fireTime) and not self.emergency:
			self.FireControl = FireControl(100000, self, random.choice(self.pois).pos)
			self.informEmergency()
			self.emergency = True
		if self.emergency and self.uncrowdedStr:
			self.getUncrowdedGate()
		super().step()
		if self.emergency:
			for occupant in self.occupants:
				fire = self.FireControl.getFirePos(occupant.pos)
				if fire != False:
					self.harmOccupant(occupant, fire)