from occupant import EmergencyOccupant
from fire import FireControl
import random
import datetime as dt
from soba.models.continuousModel import ContinuousModel
from time import time
import time as sp
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
		self.fireTime = dt.datetime(today.year, today.month, 1, 13, 30, 0, 0)
		if (sebaConfiguration.get('hazard')):
			h = sebaConfiguration.get('hazard')
			self.fireTime = dt.datetime(today.year, today.month, 1, int(h[0]+h[1]), int(h[3]+h[4]), int(h[6]+h[7]))
		self.outDoors = []
		self.getOutDoors()
		self.familiesJson = sebaConfiguration.get('families')
		self.createOccupants(jsonsOccupants)
		self.uncrowdedStr = []
		self.occupEmerg = []

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
			self.occupEmerg.append(occupant)
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
			if occupant in self.occupEmerg:
				self.occupEmerg.remove(occupant)

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

	def getSafestGate(self, occupant, exclude = []):
		"""
		Get the path to the safest exit door.
		"""
		longPath = 0
		doorAux = occupant
		for door in self.outDoors:
			if not door.pos in exclude:
				for fire in self.FireControl.limitFire:
					path = occupant.getWay(door.pos, fire.pos)
					if len(path) > longPath:
						longPath = len(path)
						doorAux = door
		return doorAux.pos

	def getNearestGate(self, occupant, exclude = []):
		"""
		Get the path to the safest nearest exit door.
		"""
		shortPath = 1000000
		doorAux = occupant
		for door in self.outDoors:
			if not door.pos in exclude:
				print("no está door.pos: ", door.pos, 'en exclude: ', exclude)
				path = occupant.getWay(occupant.pos, door.pos, other = exclude)
				if shortPath > len(path):
					shortPath = len(path)
					pathReturn = path
					doorAux = door
		return doorAux.pos

	def getUncrowdedGate(self, exclude = []):
		"""
		Get the path to the uncrowded exit door.
		"""
		doorsN = {}
		for d in self.outDoors:
			if d.pos not in exclude:
				doorsN[str(d.pos)] = 0
		for o in self.occupants:
			pos = o.pos_to_go
			if doorsN.get(str(pos)):
				doorsN[str(pos)] = doorsN.get(str(pos)) + 1
		for o in self.uncrowdedStr:
			pos = o.pos_to_go
			if pos in self.exits:
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
	def positions_fire(self):
		fire = []
		if not self.FireControl:
			return fire
		for f in self.FireControl.fireExpansion:
			x, y = f.pos
			fire.append({"x": x, "y": y})
		data = {"positions": fire}
		return data

	def exit_way_avatar(self, avatar_id, strategy = 0):
		a = self.getOccupantId(int(avatar_id))
		strategies = ['nearest', 'safest', 'uncrowded', 'lessassigned']
		a.exitGateStrategy = strategy
		pos = a.getExitGate()
		positions = []
		for p in pos:
			x, y = p
			positions.append({"x": x, "y": y})
		data = {"positions": positions}
		return data

	def fire_in_pov(self, avatar_id):
		a = self.getOccupantId(int(avatar_id))
		print(a)
		pos = a.getPosFireFOV()
		print(pos)
		positions = []
		for p in pos:
			x, y = p
			positions.append({"x": x, "y": y})
		data = {"positions": positions}
		return data

	def create_avatar(self, idAvatar, pos, color = 'red', initial_state = 'walking'):
		a = self.createEmergencyAvatar(idAvatar, pos, color, initial_state)
		self.occupants.append(a)
		return a

	def step(self):
		"""
		Execution of the scheduler steps.
		"""
		for i in self.exits:
			print(i)
		a = 0
		d = 0
		t = "Normal" 
		if self.emergency:
			t = "Emergency"
		for o in self.occupants:
			if o.alive:
				a = a + 1
			else:
				d = d + 1
		print("Situation: ", t, ", Occupants dead: ", d, ", Occupants alive: ", a)
		if self.emergency and not self.occupEmerg:
			print("Simulation terminated.")
			self.finishSimulation = True
			sp.sleep(1)
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