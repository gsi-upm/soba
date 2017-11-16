from collections import defaultdict
import numpy as np
from soba.agents.agent import Occupant
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

class MapVisualization(VisualizationElement):
	path = os.path.abspath(soba.__file__)
	path = path.rsplit('/', 1)[0]
	path = path + "/visualization/drawModelFront.js"
	path2 = os.path.abspath(soba.__file__)
	path2 = path2.rsplit('/', 1)[0]
	path2 = path2 + "/visualization/drawModelFront.js"
	package_includes = [path, path2, "Chart.min.js"]
	portrayal_method = None
	canvas_width = 500
	canvas_height = 500

	def __init__(self, portrayal_method,  cellW, cellH, canvas_width=500, canvas_height=500):
		self.portrayal_method = portrayal_method
		self.grid_width = cellW
		self.grid_height = cellH
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height

		new_element = ("new CanvasModule({}, {}, {}, {})"
			.format(self.canvas_width, self.canvas_height,
				self.grid_width, self.grid_height ))

		self.js_code = "elements.push(" + new_element + ");"

	def render(self, model):
		grid_state = defaultdict(list)
		for x in range(model.grid.width):
			for y in range(model.grid.height):
				cell_objects = model.grid.get_items_in_pos((x, y))
				for obj in cell_objects:
					if isinstance(obj, Occupant):
						portrayal = self.portrayal_method(obj)
						if portrayal:
							portrayal["x"] = x
							portrayal["y"] = y
							grid_state[portrayal["Layer"]].append(portrayal)
					if isinstance(model, ContinuousModel):
						grid_state[100] = ''
						if isinstance(obj, Door):
							offSet = 20
							x, y = obj.pos
							JSON_door = {"x":x,
										"y": y,
										"state": obj.state,
										"rot": obj.rot
							}
							grid_state[offSet].append(JSON_door)

						if isinstance(obj, Poi):
							offSet = 30
							x, y = obj.pos
							JSON_poi = {"x": x,
										"y": y,
							}
							grid_state[offSet].append(JSON_poi)

						if isinstance(obj, GeneralItem):
							offSet = 40
							x, y = obj.pos
							JSON_generalItem = {"x":x,
										"y": y
							}
							grid_state[offSet].append(JSON_generalItem)
					else:
						grid_state[100] = 'rooms'
						offSet_Rooms = 10
						roomsSends = []
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
								JSON_room = {"x":x,
											 "y": y,
											 "nAgents": nAgents,
											 "name": room.name.split(r".")[0],
											 "text": room.name.split(r".")[0]
								}
								grid_state[offSet_Rooms].append(JSON_room)
								roomsSends.append(room)
							else:
								x, y = room.pos
								JSON_room = {"x":x,
											 "y": y,
											 "nAgents":'',
											 "name": room.name.split(r".")[0],
											 "text": ''
								}
								grid_state[offSet_Rooms].append(JSON_room)

						offSet_Doors = offSet_Rooms + 10
						for door in model.doors:
							x1, y1 = door.room1.pos
							x2, y2 = door.room2.pos
							JSON_Door = {"x1": x1,
										 "y1": y1,
										 "x2": x2,
										 "y2": y2,
										 "state": door.state
							}
							grid_state[offSet_Doors].append(JSON_Door)
		if isinstance(model, ContinuousModel):
			for wall in model.walls:
				offSet = 10
				x1, y1 = wall.block1[0]
				x2, y2 = wall.block1[1]
				JSON_walls = {"x1":x1,
							"y1": y1,
							"x2": x2,
							"y2": y2
							}
				grid_state[offSet].append(JSON_walls)            
		return grid_state