from occupant import EmergencyOccupant
from fire import FireControl
import random
import datetime as dt
from soba.models.continuousModel import ContinuousModel
from time import time
from ast import literal_eval as make_tuple
import listener as lstn
from avatar import EmergencyAvatar

class SEBAModel(ContinuousModel):
	"""
	Base Class to create simulation models  on emergency situations in buildings.
		Attributes:
			Those inherited from the ContinuousModel class.
			adults: List of all adult EmergencyOccupant objects created.
			children: List of all children EmergencyOccupant objects created.
			emergency: Control of the start of the emergency. 
			FireControl: FireControl Object.
			fireTime: Date and time of the start of the emergency
			outDoors: Listing of exit doors of the building
		Methods:
			createOccupants: Create one occupant object of the EmergencyOccupant type.
			createEmergencyAvatar: Create one avatar object of the EmergencyAvatar type.
			isThereFire: Evaluate if there is fire in a position.
			informEmergency: Launches the state of emergency.
			harmOccupant: Damages an occupant with the fire that is in its same position.
			getUncrowdedGate: Get the path to the uncrowded exit door.
			getSafestGate: Get the path to the safest exit door.
			getNearestGate: Get the path to the nearest exit door.
			step: Execution of the scheduler steps.

	"""

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
		self.familiesJson = sebaConfiguration.get('families')
		self.createOccupants(jsonsOccupants)
		self.uncrowdedStr = []

	def getOutDoors(self):
		for poi in self.pois:
			if poi.id == 'out':
				self.outDoors.append(poi)

	def createOccupants(self, jsonsOccupants):
		"""
		Create one occupant object of the EmergencyOccupant type.
				Args:
					jsonOccupants: Json of description of the occupants.
		"""
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

	def createEmergencyAvatar(self, idAvatar, pos, color = 'red', initial_state = 'walking'):
		"""
		Create one avatar object of the EmergencyAvatar type.
			Args:
				idAvatar: Unique ID given to the avatar agent as int.
				pos: Initial position of the avatar as (x, y)
				color: Color assigned to the avatar as String
				initial_state: State of the avatar as String
			Return: EmergencyAvatar object
		"""
		unique_id = 100000 + int(idAvatar)
		a = EmergencyAvatar(unique_id, self, pos, color, initial_state)
		self.occupants.append(a)
		return a

	def isThereFire(self, pos):
		"""
		Evaluate if there is fire in a position.
			Args:
				pos: Position given as (x, y)
			Return: Boolean
		"""
		for fire in self.FireControl:
			if fire.pos == pos:
				return True
		return False

	def informEmergency(self):
		"""
		Launches the state of emergency.
		"""
		for occupant in self.occupants:
			occupant.makeEmergencyAction()

	def harmOccupant(self, occupant, fire):
		"""
		Damages an occupant with the fire that is in its same position.
			Args:
				occupant: EmergencyOccupant object
				fire: 
			Return: Boolean
		"""
		if occupant.life > fire.grade:
			occupant.life = occupant.life - fire.grade
		else:
			occupant.life = 0
			occupant.alive = False
	"""
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
	"""
	def getSafestGate(self, occupant):
		"""
		Get the path to the safest exit door.
		"""
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
		"""
		Get the path to the safest nearest exit door.
		"""
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
		"""
		Get the path to the uncrowded exit door.
		"""
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

	def getExitWayAvatar(self, avatar_id, strategy = 0):
		a = self.getOccupantId(int(avatar_id))
		strategies = ['nearest', 'safest', 'uncrowded', 'lessassigned']
		a.exitGateStrategy = strategy
		data = a.getExitGate()
		return data

	def getFireInFOVAvatar(self, avatar_id):
		a = self.getOccupantId(int(avatar_id))
		data = a.getPosFireFOV()
		return data

	def putCreateEmergencyAvatar(self, idAvatar, pos, color = 'red', initial_state = 'walking'):
		a = self.createEmergencyAvatar(idAvatar, pos, color, initial_state)
		return a

	def step(self):
		"""
		Execution of the scheduler steps.
		"""
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