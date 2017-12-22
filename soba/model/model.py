from collections import defaultdict
import random
import os
import os.path
import math
from soba.model.time import Time
from soba.agents.occupant import ContinuousOccupant
from soba.agents.occupant import RoomsOccupant
import soba.agents.modules.aStar as aStar
from soba.space.roomsItems import Room
from soba.space.roomsItems import Door as DoorRooms
from soba.space.roomsItems import Wall as WallRooms
from soba.space.continuousItems import GeneralItem
from soba.space.continuousItems import Door
from soba.space.continuousItems import Wall
from soba.space.continuousItems import Poi
from soba.model.time import BaseScheduler
import datetime as dt
import random
from soba.space.grid import Grid
import soba.visualization.ramen.performanceGenerator as ramen

"""
In the file model.py three classes are defined:

	-Model: Base Class to create simulation models.
	-RoomsModel:
	-ContinuousModel:

"""

class Model:
	"""
	Base Class to create simulation models.
	It creates and manages space and agents.

		Attributes:
			height: Height in number of grid cells.
			width: Width in number of grid cells.
			schedule: BaseScheduler object for agent activation.
			grid: Grid object to implement space.
			running: Parameter to control the model execution.
			NStep: Measure of the number of steps.
			occupants: List of Occupant objects created.
			agents: List of the all Agent objects created.
			asciMap: Representation of the map as ASCI used to get FOV information.
			seed: Seed employ in random generations.
			finishSimulation: Parameter to stop the software simulation.
		Methods:
			finishTheSimulation: Finish with the execution of the simulation software.
			run_model: Model execution.
			step: Execution of the scheduler steps.

	"""

	def __init__(self, width, height, seed = dt.datetime.now(), timeByStep = 60):
		"""
		Create a new Model object.
			Args:
				height: Height in number of grid cells.
				width: Width in number of grid cells.
				schedule: BaseScheduler object for agent activation.
				grid: Grid object to implement space.
				running: Parameter to control the model execution.
				NStep: Measure of the number of steps.
				occupants: List of Occupant objects created.
				agents: List of the all Agent objects created.
				asciMap: Representation of the map as ASCI used to get FOV information.
				seed: Seed employ in random generations.
				finishSimulation: Parameter to stop the software simulation.
			Return: Model object

		"""
		self.width = width
		self.height = height
		self.schedule = BaseScheduler(self)
		self.grid = Grid(width, height, False)
		self.running = True
		self.agents = []
		self.NStep = 0
		self.occupants = []
		self.clock = Time(self, timeByStep = timeByStep)
		self.seed = seed
		random.seed(seed)
		self.asciMap = []
		self.finishSimulation = False

	def finishTheSimulation(self):
		"""Finish with the execution of the simulation software."""
		PID = os.system('$!')
		os.system('kill ' + str(PID))

	def run_model(self):
		"""Model execution."""
		while self.running:
			self.step()

	def step(self):
		"""Main step of the simulation, execution of the scheduler steps."""
		if self.finishSimulation:
			self.finishTheSimulation()
		self.schedule.step()
		self.NStep = self.NStep + 1

class RoomsModel(Model):
	"""
	Base Class to create simulation models on a simplified space based on rooms.

		Attributes:
			Those inherited from the Occupant class.
			rooms: List of Room objects.
			Those inherited from the Occupant class.
			rooms: List of Room objects.
			walls: List of Wall objects.
			pois: List of Pois objects.
			generalItems: List of GeneralItem objects.
			doors: List of Door objects.
		Methods:
			createOccupants: Create occupants of the RoomsOccupant type.
			createRooms: Create the rooms in the grid space.
			setMap: Define the map plane distribution.
			createDoors: Create the doors in the grid space.
			createWalls: Create the walls in the grid space.
			thereIsClosedDoor: Check if one door is closed or open.
			thereIsOtherOccupantInRoom: Evaluate if there is another occupant apart of the past as a parameter in a room.
			thereIsSomeOccupantInRoom: Evaluate if there is any occupant in a room.
			thereIsOccupantInRoom: Evaluate if there is one specific occupant in a room.
			getRoom: Get one Room Object by position.
			pushAgentRoom: Add one agent to a room.
			popAgentRoom: Remove one agent from a room.
			openDoor: Change the status of the door to open.
			closeDoor: Change the status of the door to close.

	"""
	def __init__(self, width, height, jsonRooms, jsonsOccupants, seed = dt.datetime.now(), timeByStep = 60):
		super().__init__(width, height, seed, timeByStep)
		"""
		Create a new RoomsModel object.
			Args:
				height: Height in number of grid cells.
				width: Width in number of grid cells.
				jsonRooms: Json of description of the map plane.
				jsonsOccupants: Json of description of the occupancy.
				seed: Seed employ in random generations.
				timeByStep: Time in seconds associated with each step.
			Return: RoomsModel object
		"""
		self.rooms = []
		self.createRooms(jsonRooms)
		self.setMap()
		self.createDoors()
		self.createWalls()

		self.createOccupants(jsonsOccupants)
	
	def createOccupants(self, jsonsOccupants):
		"""
		Create occupants of the RoomsOccupant type.
				Args:
					jsonOccupants: Json of description of the occupants.
		"""
		for json in jsonsOccupants:
			for n in range(0, json['N']):
				a = RoomsOccupant(n, self, json)
				self.occupants.append(a)

	def createRooms(self, jsonRooms):
		"""
		Create the rooms in the grid space.
			Args:
				jsonRooms: Json of description of the map plane.
		"""
		rooms = jsonRooms
		self.rooms = []
		for k,v in rooms.items():
			newRoom  = 0
			name = k
			conectedTo = v.get('conectedTo')
			entrance = v.get('entrance')
			measures = v['measures']
			dx = measures['dx']
			dy = measures['dy']
			newRoom = Room(name, conectedTo, dx, dy)
			newRoom.entrance = entrance
			self.rooms.append(newRoom)
		for room1 in self.rooms:
			if room1.conectedTo is not None:
				for otherRooms in list(room1.conectedTo.values()):
					for room2 in self.rooms:
						if room2.name == otherRooms:
							room1.roomsConected.append(room2)
							room2.roomsConected.append(room1)
		for room in self.rooms:
			room.roomsConected = list(set(room.roomsConected))
		sameRoom = {}
		for room in self.rooms:
			if sameRoom.get(room.name.split(r".")[0]) is None:
				sameRoom[room.name.split(r".")[0]] = 1
			else:
				sameRoom[room.name.split(r".")[0]] = sameRoom[room.name.split(r".")[0]] + 1

	def setMap(self):
		"""Define the map plane distribution."""
		rooms_noPos = self.rooms
		rooms_using = []
		rooms_used = []
		for room in self.rooms:
			if room.entrance is not None:
				room.pos = (int(1), 1)
				rooms_using.append(room)
				rooms_used.append(room)
				rooms_noPos.remove(room)
				break
		while len(rooms_noPos) > 0:
			for roomC in rooms_using:
				xc, yc = roomC.pos
				rooms_conected = roomC.conectedTo
				rooms_using.remove(roomC)
				if rooms_conected is not None:
					orientations = list(rooms_conected.keys())
					for orientation in orientations:
						if orientation == 'R':
							for room in rooms_noPos:
								if room.name == rooms_conected['R']:
									room.pos = (int(xc + 1), yc)
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'U':
							for room in rooms_noPos:
								if room.name == rooms_conected['U']:
									room.pos = (xc, int(yc + 1))
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'D':
							for room in rooms_noPos:
								if room.name == rooms_conected['D']:
									room.pos = (xc, int(yc - 1))
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'L':
							for room in rooms_noPos:
								if room.name == rooms_conected['L']:
									room.pos = (int(xc -1), yc)
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
				else:
					pass
		self.rooms = rooms_used

	def createDoors(self):
		"""Create the doors in the grid space."""
		self.doors = []
		for roomC in self.rooms:
			roomsConected = roomC.roomsConected
			for room in roomsConected:
				door_created = False
				same_corridor = False
				if room.name != roomC.name:
					for door in self.doors:
						if (door.room1.name == roomC.name and door.room2.name == room.name) or (door.room2.name == roomC.name and door.room1.name == room.name):
							door_created = True
						if room.name.split(r".")[0] == roomC.name.split(r".")[0]:
							same_corridor = True
					if door_created == False and same_corridor == False:
						d = DoorRooms(roomC, room)
						self.doors.append(d)
						room.doors.append(d)
						roomC.doors.append(d)

	def createWalls(self):
		"""Create the walls in the grid space."""
		for room in self.rooms:
			walls = []
			xr, yr = room.pos
			roomA = self.getRoom((xr, yr+1))
			if roomA != False:
				if roomA.name.split(r".")[0] == room.name.split(r".")[0]:
					pass
				else:
					wall = WallRooms(room, roomA)
					walls.append(wall)
			else:
				wall = WallRooms(room)
				walls.append(wall)
			roomB = self.getRoom((xr, yr-1))
			if roomB != False:
				if roomB.name.split(r".")[0] == room.name.split(r".")[0]:
					pass
				else:
					wall = WallRooms(room, roomB)
					walls.append(wall)
			else:
				wall = WallRooms(room)
				walls.append(wall)
			roomC = self.getRoom((xr+1, yr))
			if roomC != False:
				if roomC.name.split(r".")[0] == room.name.split(r".")[0]:
					pass
				else:
					wall = WallRooms(room, roomC)
					walls.append(wall)
			else:
				wall = WallRooms(room)
				walls.append(wall)
			roomD = self.getRoom((xr-1, yr))
			if roomD != False:
				if roomD.name.split(r".")[0] == room.name.split(r".")[0]:
					pass
				else:
					wall = WallRooms(room, roomD)
					walls.append(wall)
			else:
				wall = WallRooms(room)
				walls.append(wall)

			room.walls = walls

	def thereIsClosedDoor(self, beforePos, nextPos):
		"""
		Check if one door is closed or open.
			Args:
				beforePos, nextPos: The two common positions of the door as (x, y).
			Return: True (closed) or False (opened).
		"""
		oldRoom = False
		newRoom = False
		for room in rooms:
			if room.pos == beforePos:
				oldRoom = room
			if room.pos == nextPos:
				newRoom = room
		for door in self.doors:
			if (door.room1.name == oldRoom.name and door.room2.name == newRoom.name) or (door.room2.name == oldRoom.name and door.room1.name == newRoom.name):
				if door.state == False:
					return True
		return False

	def thereIsOtherOccupantInRoom(self, room, agent):
		"""
		Evaluate if there is another occupant apart of the past as a parameter in a room.
			Args:
				room: Room object to be checked.
				agent: Occupant object to be ignored.
			Return: True (yes), False (no)
		"""
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant) and occupant != agent:
					return True
		return False

	def thereIsSomeOccupantInRoom(self, room):
		"""
		Evaluate if there is any occupant in a room.
			Args:
				room: Room object to be checked.
			Return: True (yes), False (no)
		"""
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant):
					return True
		return False

	def thereIsOccupantInRoom(self, room, agent):
		"""
		Evaluate if there is one specific occupant in a room.
			Args:
				room: Room object to be checked.
			Return: True (yes), False (no)
		"""
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant) and occupant == agent:
					return True
		return False

	def getRoom(self, pos):
		""" 
		Get one Room Object by position.
			Args:
				pos: Position of the grid as (x,y).
			Return: Room Object or False
		"""
		for room in self.rooms:
			if room.pos == pos:
				return room
		return False

	def pushAgentRoom(self, agent, pos):
		"""
		Add one agent to a room.
			Args:
				agent: Agent Object
				pos: Position of the grid as (x,y)
		"""
		room = self.getRoom(pos)
		room.agentsInRoom.append(agent)

	def popAgentRoom(self, agent, pos):
		"""
		Remove one agent from a room.
			Args:
				agent: Agent Object
				pos: Position of the grid as (x,y)
		"""
		room = self.getRoom(pos)
		room.agentsInRoom.remove(agent)

	def openDoor(self, agent, room1, room2):
		"""
		Change the status of the door to open (True). 
			Args:
				agent: Agent object which want to open the door.
				room1, room2: The two common rooms of the door as Room object.
				"""
		for door in self.doors:
			if ((door.room1 == room1 and door.room2 == room2) or (door.room1 == room2 and door.room2 == room1)):
				door.state = False

	def closeDoor(self, agent, room1, room2):
		"""
		Change the status of the door to close (False).
			Args:
				agent: Agent object which want to close the door.
				room1, room2: The two common rooms of the door as Room object.
		"""
		numb = random.randint(0, 10)
		for door in self.doors:
			if ((door.room1 == room1 and door.room2 == room2) or (door.room1 == room2 and door.room2 == room1)):
				if  7 >= numb:
					door.state = False
				else:
					door.state = True

	def step(self):
		super().step()

class ContinuousModel(Model):
	"""
	Base Class to create simulation models on a simplified space based on rooms.
		Attributes:
			Those inherited from the Occupant class.
			rooms: List of Room objects.
			walls: List of Wall objects.
			pois: List of Pois objects.
			generalItems: List of GeneralItem objects.
			doors: List of Door objects.
		Methods:
			createOccupants: Create occupants of the ContinuousOccupant type.
			getScaledCoordinate: Gets the value of a coordinate or a cell size scaled.
			setMap: Define the map plane distribution.
			getAsciMap: Get the plane of the grid in an ASCII format, such as a matrix, to apply the fov algorithm.
			thereIsClosedDoor: Check if one door is closed or open.
			getDoorInPos: Get a Door object in a position given.
			getOccupantsPos: Get a Occupant objects in a position given.
			thereIsOccupant: Check if there is any Occupant object in a position given.
"""
	def __init__(self, width, height, jsonMap, jsonsOccupants, seed = dt.datetime.now(), scale = 0.5, timeByStep = 60):
		super().__init__(width, height, seed, timeByStep)
		"""
		Create a new ContinuousModel object.
			Args:
				height: Height in number of grid cells.
				width: Width in number of grid cells.
				jsonMap: Json of description of the map plane.
				jsonsOccupants: Json of description of the occupancy.
				seed: Seed employ in random generations.
				scale: Define the scale of the cells in relation with the measures given in the jsonMap.
				timeByStep: Time in seconds associated with each step.
				asciMap: Plane of the grid in an ASCII format to apply the fov algorithm.
			Return: ContinuousModel object.
		"""
		self.walls = []
		self.lineWalls = []
		self.pois = []
		self.doors = []
		self.generalItems =  []
		self.ramen = False
		self.exits = []

		#Create the map
		self.setMap(jsonMap, scale)
		aStar.getObtacles(self)
		self.createOccupants(jsonsOccupants)

	def createOccupants(self, jsonsOccupants):
		"""
		Create occupants of the ContinuousOccupant type.
				Args:
					jsonOccupants: Json of description of the occupants.
		"""
		for json in jsonsOccupants:
			for n in range(0, json['N']):
				a = ContinuousOccupant(n, self, json)
				self.occupants.append(a)

	def getScaledCoordinate(self, coordenate, scale):
		"""
		Gets the value of a coordinate or a cell size scaled to the size of the grid in relation to a given scale.
			Args:
				coordenate: Coordenate value to be scale
				scale: Value of the scale to be applied.
			Return: value of the coordinate.
		"""
		n = coordenate/scale
		up = True if(float(str(n-int(n))[1:]) > 0.1) else False
		n = int(n)
		if up == True:
			return (n+1)
		return n

	def setMap(self, jsonMap, scale):
		"""
		Define the map plane distribution.
			Args:
				jsonMap: Json of description of the map plane.
				scale: Value of the scale.
		"""
		walls = jsonMap["walls"]
		corners = jsonMap["corners"]
		items = jsonMap["items"]

		for k, v in walls.items():
			pos1 = corners[v["corner1"]]
			pos2 = corners[v["corner2"]]
			x1 = self.getScaledCoordinate(pos1["x"], scale)
			y1 = self.getScaledCoordinate(pos1["y"], scale)
			x2 = self.getScaledCoordinate(pos2["x"], scale)
			y2 = self.getScaledCoordinate(pos2["y"], scale)
			if x1 == x2:
				if y2 > y1:
					for yAux in range(y1+1, y2+1):
						block1 = [(x1, yAux), (x2+1, yAux)]
						block2 = [(x1, yAux), (x1+1, yAux-1), (x1+1, yAux+1)]
						block3 = [(x1+1, yAux), (x1, yAux-1), (x1, yAux+1)]
						w = Wall(block1, block2, block3)
						self.walls.append(w)
				else:
					for yAux in range(y2+1, y1+1):
						block1 = [(x1, yAux), (x2+1, yAux)]
						block2 = [(x1, yAux), (x1+1, yAux-1), (x1+1, yAux+1)]
						block3 = [(x1+1, yAux), (x1, yAux-1), (x1, yAux+1)]
						w = Wall(block1, block2, block3)
						self.walls.append(w)
			else:
				if x2 > x1:
					for xAux in range(x1+1, x2+1):
						block1 = [(xAux, y1), (xAux, y1+1)]
						block2 = [(xAux, y1), (xAux-1, y1+1), (xAux+1, y1+1)]
						block3 = [(xAux, y1+1), (xAux-1, y1), (xAux+1, y1)]
						w = Wall(block1, block2, block3)
						self.walls.append(w)
				else:
					for xAux in range(x2+1, x1+1):
						block1 = [(xAux, y1), (xAux, y1+1)]
						block2 = [(xAux, y1), (xAux-1, y1+1), (xAux+1, y1+1)]
						block3 = [(xAux, y1+1), (xAux-1, y1), (xAux+1, y1)]
						w = Wall(block1, block2, block3)
						self.walls.append(w)

		for k, v in items.items():
			x = self.getScaledCoordinate(v['pos']['x'], scale)
			y = self.getScaledCoordinate(v['pos']['y'], scale)
			centerX = (0.375 > float(str(v['pos']['x']-int(v['pos']['x']))[1:]) > 0.125) or (0.855 > float(str(v['pos']['x']-int(v['pos']['x']))[1:]) > 0.675)
			centerY = (0.375 > float(str(v['pos']['y']-int(v['pos']['y']))[1:]) > 0.125) or (0.855 > float(str(v['pos']['y']-int(v['pos']['y']))[1:]) > 0.675)
			dx = math.floor(self.getScaledCoordinate((v["dx"]), scale))
			dy = math.floor(self.getScaledCoordinate((v["dy"]), scale))
			dxAux2 = dxAux1 = int(dx/2)
			dyAux2 = dyAux1 = int(dy/2)
			if centerY and centerX:
				pass
			elif not centerY and centerX:
				dyAux1 = dyAux1-1
			elif centerY and not centerX:
				dxAux1 = dxAux1-1
			else:
				dxAux1 = dxAux1-1
				dyAux1 = dyAux1-1

			if v['itemType'] == 'door':
				if dx > 1 and dy > 1:
					for xAux in range(x - dxAux1, x + dxAux2+1):
						for yAux in range(y - dyAux1, y + dyAux2+1):
							i = Door(self, (xAux, yAux), (xAux+1, yAux+1), v["rot"])
							self.doors.append(i)
				elif dx > 1:
					for xAux in range(x - dxAux1, x + dxAux2+1):
						yAux = y
						i = Door(self, (xAux, yAux), (xAux, yAux+1), v["rot"])
						self.doors.append(i)
				elif dy > 1:
					for yAux in range(y - dyAux1, y + dyAux2+1):
						xAux = x
						i = Door(self, (xAux, yAux), (xAux+1, yAux), v["rot"])
						self.doors.append(i)
				elif dx == 1 and dy == 1:
					xAux = x
					yAux = y
					rot = v["rot"]
					if rot == 'y':
						i = Door(self, (xAux, yAux), (xAux+1, yAux), v["rot"])
					else:
						i = Door(self, (xAux, yAux), (xAux, yAux+1), v["rot"])
					self.doors.append(i)

			elif v['itemType'] == 'poi':
				if dx > 1 and dy > 1:
					for xAux in range(x - dxAux1, x + dxAux2+1):
						for yAux in range(y - dyAux1, y + dyAux2+1):
							if 'share' in v:
								i = Poi(self, (xAux, yAux), v['id'], v['share'])
							else:
								i = Poi(self, (xAux, yAux), v['id'], color = v.get('Color'))
							self.pois.append(i)
				elif dx > 1:
					for xAux in range(x - dxAux1, x + dxAux2+1):
						yAux = y
						if 'share' in v:
							i = Poi(self, (xAux, yAux), v['id'], v['share'])
						else:
							i = Poi(self, (xAux, yAux), v['id'], color = v.get('Color'))
						self.pois.append(i)
				elif dy > 1:
					for yAux in range(y - dyAux1, y + dyAux2+1):
						xAux = x
						if 'share' in v:
							i = Poi(self, (xAux, yAux), v['id'], v['share'])
						else:
							i = Poi(self, (xAux, yAux), v['id'], color = v.get('Color'))
						self.pois.append(i)
				elif dx == 1 and dy == 1:
					xAux = x
					yAux = y
					if 'share' in v:
						i = Poi(self, (xAux, yAux), v['id'], v['share'])
					else:
						i = Poi(self, (xAux, yAux), v['id'], color = v.get('Color'))
					self.pois.append(i)
				if v['itemType'] == 'poi' and v['itemType'] == 'exit':
					self.exits.append(i.pos)

			else:
				if dx > 1 and dy > 1:
					for xAux in range(x - dxAux1, x + dxAux2+1):
						for yAux in range(y - dyAux1, y + dyAux2+1):
							i = GeneralItem(self, (xAux, yAux), color = v.get('Color'))
							self.generalItems.append(i)
				elif dy > 1:
					for yAux in range(y - dyAux1, y + dyAux2+1):
						xAux = x
						i = GeneralItem(self, (xAux, yAux), color = v.get('Color'))
						self.generalItems.append(i)
				elif dx > 1:
					for xAux in range(x - dxAux1, x + dxAux2+1):
						yAux = y
						i = GeneralItem(self, (xAux, yAux), color = v.get('Color'))
						self.generalItems.append(i)
				if dx == 1 and dy == 1:
					i = GeneralItem(self, (x, y), color = v.get('Color'))
					self.generalItems.append(i)

		self.getAsciMap()

	def getAsciMap(self):
		"""Get the plane of the grid in an ASCII format, such as a matrix, to apply the fov algorithm."""
		asciMapAux = []
		asciMap2 = []
		for i in range(self.height):
			asciMapAux.append([0] * self.width)
		for i in range(self.height):
			for j in range(self.width):
				asciMapAux[i][j] = '.'
		for wall in self.walls:
			x, y = wall.block1[0]
			asciMapAux[y][x] = '#'
		for door in self.doors:
			x, y = door.pos1
			x2, y2 = door.pos2
			asciMapAux[y][x] = '.'
			asciMapAux[y2][x2] = '.'
		string = ''
		for line in asciMapAux:
			for element in line:
				string = string + element
			asciMap2.append(string)
			string = ''
		self.asciMap = asciMap2

	def thereIsClosedDoor(self, pos):
		"""
		Check if one door is closed or open.
			Args:
				pos: Position of the door as (x, y).
			Return: State of the door as boolean.
		"""
		possibleDoor = self.grid.get_items_in_pos(pos)
		for item in possibleDoor:
			if isinstance(item, Door):
				return Door.state

	def getDoorInPos(self, pos):
		"""
		Get a Door object in a position given.
			Args:
				pos: Position of the door as (x, y).
			Return: Door object or false.
		"""
		possibleDoor = self.grid.get_items_in_pos(pos)
		for item in possibleDoor:
			if isinstance(item, Door):
				return item
		return False

	def getOccupantsPos(self, pos):
		"""
		Get a Occupant objects in a position given.
			Args:
				pos: Position as (x, y).
			Return: List of Cccupant objects.
		"""
		possibleOccupants = self.grid.get_items_in_pos(pos)
		occupants = []
		for item in possibleOccupants:
			if isinstance(item, Occupant):
				occupants.append(item)
		return occupants

	def thereIsOccupant(self, pos):
		"""
		Check if there is any Occupant object in a position given.
			Args:
				pos: Position as (x, y).
			Return: True (yes), False (no).
		"""
		possible_occupant = self.grid.get_cell_list_contents([pos])
		if (len(possible_occupant) > 0):
			for occupant in possible_occupant:
				if isinstance(occupant,Occupant):
					return True
		return False

	def step(self):
		if self.finishSimulation and self.ramen:
			ramen.generateJSON()
		super().step()