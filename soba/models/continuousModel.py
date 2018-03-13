from collections import defaultdict
import random
import os
import os.path
import math
from soba.models.timeControl import Time
from soba.models.generalModel import GeneralModel
from soba.agents.continuousOccupant import ContinuousOccupant
from soba.agents.roomsOccupant import RoomsOccupant
import soba.agents.resources.aStar as aStar
from soba.space.continuousElements import GeneralItem
from soba.space.continuousElements import Door
from soba.space.continuousElements import Wall
from soba.space.continuousElements import Poi
import datetime as dt
import random
from mesa.space import Grid
import soba.visualization.ramen.performanceGenerator as ramen
from mesa import Model
from mesa.time import SimultaneousActivation
from soba.agents.occupant import Occupant

class ContinuousModel(GeneralModel):
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
	global ramenAux
	global ramenRT
	ramenAux = False
	ramenRT = False
	def activeRamen(rt):
		global ramenAux
		global ramenRT
		ramenAux = True
		ramenRT = rt
		ContinuousOccupant.activeRamen()

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
		self.exits = []

		#Create the map
		self.setMap(jsonMap, scale)
		aStar.getObtacles(self)

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
				i = False
				if dx > 1 and dy > 1:
					for xAux in range(x - dxAux1, x + dxAux2+1):
						for yAux in range(y - dyAux1, y + dyAux2+1):
							if 'share' in v:
								i = Poi(self, (xAux, yAux), v['id'], v['share'])
							else:
								i = Poi(self, (xAux, yAux), v['id'], color = v.get('Color'))
							self.pois.append(i)
							if v['itemName'] == 'exit':
								self.exits.append(i.pos)
				elif dx > 1:
					for xAux in range(x - dxAux1, x + dxAux2+1):
						yAux = y
						if 'share' in v:
							i = Poi(self, (xAux, yAux), v['id'], v['share'])
						else:
							i = Poi(self, (xAux, yAux), v['id'], color = v.get('Color'))
						self.pois.append(i)
						if v['itemName'] == 'exit':
							self.exits.append(i.pos)
				elif dy > 1:
					for yAux in range(y - dyAux1, y + dyAux2+1):
						xAux = x
						if 'share' in v:
							i = Poi(self, (xAux, yAux), v['id'], v['share'])
						else:
							i = Poi(self, (xAux, yAux), v['id'], color = v.get('Color'))
						self.pois.append(i)
						if v['itemName'] == 'exit':
							self.exits.append(i.pos)
				elif dx == 1 and dy == 1:
					xAux = x
					yAux = y
					if 'share' in v:
						i = Poi(self, (xAux, yAux), v['id'], v['share'])
					else:
						i = Poi(self, (xAux, yAux), v['id'], color = v.get('Color'))
					self.pois.append(i)
					if v['itemName'] == 'exit':
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
		possibleDoor = self.grid.get_cell_list_contents([pos])
		for item in possibleDoor:
			if isinstance(item, Door):
				return Door.state

	def nearPos(self, pos1, pos2):
		x, y = pos2
		posis = [(x, y), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
		if pos1 in posis:
			return True
		return False

	def getDoorInPos(self, pos):
		"""
		Get a Door object in a position given.
			Args:
				pos: Position of the door as (x, y).
			Return: Door object or false.
		"""
		possibleDoor = self.grid.get_cell_list_contents([pos])
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
		possibleOccupants = self.grid.get_cell_list_contents([pos])
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

	def getPOIsId(self, poiId):
		pois = []
		for i in self.pois:
			if i.id == poiId:
				pois.append(i)
		if pois:
			return pois
		return False

	def getPOIsPos(self, poiPos):
		pois = []
		conts = self.grid.get_cell_list_contents(poiPos)
		for c in conts:
			if isinstance(c, Poi):
				pois.append(c)
		if pois:
			return pois
		return False

	def checkFreePOI(self, p):
		conts = self.grid.get_cell_list_contents(p.pos)
		for c in conts:
			if isinstance(c, Occupant):
				return False
		return True

	def xyInGrid(self, x, y):
		if x >= 0 and not x >= self.width:
			if y >= 0 and not y >= self.height:
				return True
		return False

	def step(self):
		if self.finishSimulation and ramenAux:
			ramen.generateJSON()
		for a in self.occupants:
			a.alreadyMovement = False
		super().step()
		if ramenRT:
			ramen.generateRTJSON(self.NStep-1)