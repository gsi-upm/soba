from collections import defaultdict
import numpy as np
from soba.agents.agent import Agent
from soba.space.roomsItems import Room
from soba.space.roomsItems import Wall
from soba.space.roomsItems import Door
from soba.space.continuousItems import Wall
from soba.space.continuousItems import Door
from soba.space.continuousItems import Poi
from soba.space.continuousItems import GeneralItem
from soba.visualization.server import VisualizationElement
import soba
import os
import re
from soba.model.model import ContinuousModel

class BackEndVisualization(VisualizationElement):
	path = os.path.abspath(soba.__file__)
	path = path.rsplit('/', 1)[0]
	path = path + "/visualization/drawModelFront.js"
	package_includes = [path]

	def __init__(self, cellW=500, cellH=500, canvas_width=500, canvas_height=500):
		self.grid_width = cellW
		self.grid_height = cellH
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height

		visualizationObject = ("new VisualClass({}, {}, {}, {})".format(self.canvas_width, self.canvas_height, self.grid_width, self.grid_height))

		self.js_code = "elements.push(" + visualizationObject + ");"

	def render(self, model):
		grid_state = defaultdict(list)

		if isinstance(model, ContinuousModel):
			grid_state[0] = 'continuous'
		elif isinstance(model, RoomsModel):
			grid_state[0] = 'rooms'
		else:
			grid_state[0] = 'other'

		for x in range(model.grid.width):
			for y in range(model.grid.height):
				cell_objects = model.grid.get_items_in_pos((x, y))
				for obj in cell_objects:
					if isinstance(obj, Agent):
						offset = 1
						x, y = obj.pos
						color = obj.color
						shape = obj.shape
						JSON_Agent = {"x": x, "y": y, "color": color, "shape": shape}
						grid_state[offset].append(JSON_Agent)

		if grid_state[0] == 'continuous':
			for x in range(model.grid.width):
				for y in range(model.grid.height):
					cell_objects = model.grid.get_items_in_pos((x, y))
					for obj in cell_objects:
						if isinstance(obj, Poi):
							offSet = 2
							x, y = obj.pos
							JSON_poi = {"x": x, "y": y}
							grid_state[offSet].append(JSON_poi)

						if isinstance(obj, GeneralItem):
							offSet = 3
							x, y = obj.pos
							JSON_generalItem = {"x": x, "y": y}
							grid_state[offSet].append(JSON_generalItem)

			for wall in model.walls:
				offSet = 4
				x1, y1 = wall.block1[0]
				x2, y2 = wall.block1[1]
				JSON_walls = {"x1":x1, "y1": y1, "x2": x2, "y2": y2}
				grid_state[offSet].append(JSON_walls)

			for door in model.doors:
				offSet = 5
				x, y = door.pos1
				JSON_door = {"x":x, "y": y, "state": door.state, "rot": door.rot}
				grid_state[offSet].append(JSON_door)


		elif grid_state[0] == 'rooms':
			offSet_Rooms = 2
			roomsSends = []
			JSONs_rooms = []
			for room in model.rooms:
				send = False
				for roomAux in roomsSends:
					if (roomAux.name.split(r".")[0] == room.name.split(r".")[0]):
						send = True
					if send == False:
						nAgents = 0
						for room2 in model.rooms:
							if (room2.name.split(r".")[0] == room.name.split(r".")[0]):
								nAgents = nAgents + len(room2.agentsInRoom)
						x, y = room.pos
						JSON_room = {"x":x, "y": y, "nAgents": nAgents, "name": room.name.split(r".")[0], "text": room.name.split(r".")[0]}
						JSONs_rooms.append(JSON_room)
						roomsSends.append(room)
					else:
						x, y = room.pos
						JSON_room = {"x":x, "y": y, "nAgents":'', "name": room.name.split(r".")[0], "text": ''}
						JSONs_rooms.append(JSON_room)
			grid_state[offSet_Doors].append(JSON_rooms)

			offSet_Doors = 3
			JSONs_Doors = []
			for door in model.doors:
				x1, y1 = door.room1.pos
				x2, y2 = door.room2.pos
				JSON_Door = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "state": door.state}
				JSONs_Doors.append(JSON_room)
			grid_state[offSet_Doors].append(JSONs_Doors)
   
		return grid_state