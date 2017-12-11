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

#Class Model base
class Model:

	def __init__(self, width, height, seed = dt.datetime.now(), timeByStep = 60):

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
		PID = os.system('$!')
		os.system('kill ' + str(PID))

	def run_model(self):
		while self.running:
			self.step()

	def step(self):
		if self.finishSimulation:
			self.finishTheSimulation()
		self.schedule.step()
		self.NStep = self.NStep + 1

# Model for rooms option
class RoomsModel(Model):

	def __init__(self, width, height, jsonRooms, jsonsOccupants, seed = dt.datetime.now(), timeByStep = 60):
		super().__init__(width, height, seed, timeByStep)

		self.rooms = []
		self.createRooms(jsonRooms)
		self.setMap()
		self.createDoors()
		self.createWalls()

		self.createOccupants(jsonsOccupants)
	
	def createOccupants(self, jsonsOccupants):
		for json in jsonsOccupants:
			for n in range(0, json['N']):
				a = RoomsOccupant(n, self, json)
				self.occupants.append(a)

	def isConected(self, pos):
		nextRoom = False
		for room in self.rooms:
			if room.pos == pos:
				nextRoom = room
		if nextRoom == False:
			return False
		for x in range(0, width):
			for y in range(0, height):
				self.pos_out_of_map.append(x, y)
		for room in self.rooms:
			self.pos_out_of_map.remove(room.pos)

	def createRooms(self, jsonRooms):
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

	##
	#Auxiliar methods
	##

	def thereIsClosedDoor(self, beforePos, nextPos):
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

	def ThereIsOtherOccupantInRoom(self, room, agent):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant) and occupant != agent:
					return True
		return False

	def ThereIsSomeOccupantInRoom(self, room):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant):
					return True
		return False

	def thereIsOccupantInRoom(self, room, agent):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant) and occupant == agent:
					return True
		return False

	def getRoom(self, pos):
		for room in self.rooms:
			if room.pos == pos:
				return room
		return False

	def pushAgentRoom(self, agent, pos):
		room = self.getRoom(pos)
		room.agentsInRoom.append(agent)

	def popAgentRoom(self, agent, pos):
		room = self.getRoom(pos)
		room.agentsInRoom.remove(agent)

	def openDoor(self, agent, room1, room2):
		for door in self.doors:
			if ((door.room1 == room1 and door.room2 == room2) or (door.room1 == room2 and door.room2 == room1)):
				door.state = False

	def closeDoor(self, agent, room1, room2):
		numb = random.randint(0, 10)
		for door in self.doors:
			if ((door.room1 == room1 and door.room2 == room2) or (door.room1 == room2 and door.room2 == room1)):
				if  7 >= numb:
					door.state = False
				else:
					door.state = True

	def step(self):
		super().step()

# Model for continuous option
class ContinuousModel(Model):

	def __init__(self, width, height, jsonMap, jsonsOccupants, seed = dt.datetime.now(), scale = 0.5, timeByStep = 60):
		super().__init__(width, height, seed, timeByStep)

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
		for json in jsonsOccupants:
			for n in range(0, json['N']):
				a = ContinuousOccupant(n, self, json)
				self.occupants.append(a)

	def getScaledCoordinate(self, coordenate, scale):
		n = coordenate/scale
		up = True if(float(str(n-int(n))[1:]) > 0.1) else False
		n = int(n)
		if up == True:
			return (n+1)
		return n

	def setMap(self, jsonMap, scale):
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

	##
	#Auxiliar methods
	##

	def thereIsClosedDoor(self, pos):
		possibleDoor = self.grid.get_items_in_pos(pos)
		for item in possibleDoor:
			if isinstance(item, Door):
				return Door.state

	def getDoorInPos(self, pos):
		possibleDoor = self.grid.get_items_in_pos(pos)
		for item in possibleDoor:
			if isinstance(item, Door):
				return item
		return False

	def thereIsAOccupant(self, pos, agent):
		possibleDoor = self.grid.get_items_in_pos(pos)
		for item in possibleDoor:
			if agent == time:
				return True
		return False

	def thereIsSomeOccupant(self, pos):
		possibleDoor = self.grid.get_items_in_pos(pos)
		for item in possibleDoor:
			if agent == time:
				return True
		return False

	def getOccupantsPos(self, pos):
		possibleOccupants = self.grid.get_items_in_pos(pos)
		occupants = []
		for item in possibleOccupants:
			if isinstance(item, Occupant):
				occupants.append(item)
		return occupants

	def thereIsOccupant(self, pos):
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