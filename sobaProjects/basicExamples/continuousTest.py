from soba.agents.agent import Occupant
from soba.model.model import ContinuousModel
import soba.run
from collections import OrderedDict
import json
import datetime as dt

class ModelExample(ContinuousModel):

	def __init__(self, width, height, jsonMap, jsonsOccupants, seed, scale):
		super().__init__(width, height, jsonMap, jsonsOccupants, seed, scale)

	def step(self):
		super().step()
		if (int(self.clock.day) == 5):
			PID = os.system('$!')
			os.system('kill ' + str(PID))

jsonsOccupants = []

N = 2
states = OrderedDict([('Leaving','out'), ('Resting', 'sofa'), ('Working in my laboratory', 'wp')])

schedule = {'s': "00:00:00", 't1': "00:50:00", 't2': "13:00:00", 't3': "14:10:00", 'e': "23:59:59"}

markovActivity = {
	's-t1': [[100, 0, 0], [0, 0, 0], [0, 0, 0]],
	't1-t2': [[30, 40, 30], [0, 50, 50], [0, 50, 50]],
	't2-t3': [[0, 0, 0], [50, 50, 0], [0, 0, 0]],
	't3-e': [[0, 50, 50], [10, 90, 0], [0, 0, 0]]
}

timeActivity = {
	's-t1': [60, 0, 0],
	't1-t2': [2, 60, 15],
	't2-t3': [60, 10, 15],
	't3-e': [60, 20, 15]
}


jsonOccupant = {'type':'example' , 'N':N, 'states': states , 'schedule': schedule, 'markovActivity': markovActivity, 'timeActivity': timeActivity}

jsonsOccupants.append(jsonOccupant)

with open('LabGSI.blueprint3d') as data_file:
	NITEMS = 0
	data = json.load(data_file)
	corners = {}
	walls = {}
	items = {}
	offset = 40
	flor = data["floorplan"]
	for k, v in flor["corners"].items():
		corners[k] = {"x":  v["x"]/25 + offset,"y":-v["y"]/25 + offset}

	n = 0
	for k in flor["walls"]:
		walls["idWall" + str(n)] = {"corner1": k["corner1"], "corner2": k["corner2"]}
		n = n + 1

	n = 0
	for k in data["items"]:
		if str(k['item_type']) == '2' or str(k['item_type']) == '9' or str(k['item_type']) == '3':
			pass
		else:
			myList = [0, 3.14/2]
			rot = min(myList, key=lambda x:abs(x-abs(k["rotation"])))
			print(k["rotation"])
			print('rot', rot)
			if rot == 0:
				dx = k["width"]
				dy = k["depth"]
				rot = 'x'
			else:
				dy = k["width"]
				dx = k["depth"]
				rot = 'y'
			items["idItem" + str(n)] = {"itemType": k["item_type"], "pos": { "x": k["xpos"]/25 + offset, "y":  -k["zpos"]/25 + offset}, "dx" :dx/25, "dy" :dy/25}
			if k["item_name"] == 'Chair':
				items["idItem" + str(n)]["itemType"] = "poi"
				items["idItem" + str(n)]["id"] = "wp"
				items["idItem" + str(n)]["share"] = "False"
			if k["item_name"] == 'Red Chair':
				items["idItem" + str(n)]["itemType"] = "poi"
				items["idItem" + str(n)]["id"] = "sofa"
			if k["item_name"] == 'Open Door':
				items["idItem" + str(n)]['rot'] = rot
				items["idItem" + str(n)]["itemType"] = "door"
			if k["item_name"] == 'Out Door':
				items["idItem" + str(n)]["itemType"] = "poi"
				items["idItem" + str(n)]["id"] = "out"
				items["idItem" + str(n+1000)] = {"itemType": k["item_type"], "pos": { "x": k["xpos"]/25 + offset, "y":  -k["zpos"]/25 + offset}, "dx" :dx/25, "dy" :dy/25, 'rot': rot}
				items["idItem" + str(n+1000)]["itemType"] = "door"
			n = n + 1
	print('NUMERO DE ITEMS', NITEMS)
	jsonResponse = {"corners": corners, "walls": walls, "items": items}

#Visual run

soba.run.run(ModelExample, None, 70, 70, jsonResponse, jsonsOccupants, dt.datetime.now(), 2)

#Batch run
'''
fixed_params = {"width": 70,
				"height": 70,
				"jsonMap": jsonResponse,
				"jsonsOccupants": jsonsOccupants,
				"scale": 2
				}
variable_params = {"seed": range(10, 500, 10)}

soba.run.run(ModelExample, fixed_params, variable_params, iterations = 1)
'''