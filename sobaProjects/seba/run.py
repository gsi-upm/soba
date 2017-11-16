import soba.run as run
from collections import OrderedDict
import json
import datetime as dt
from model import SEBAModel
from back import Visualization
import math

## Definición de ocupantes

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


jsonOccupant = {'type':'parent' , 'N':N, 'states': states , 'schedule': schedule, 'markovActivity': markovActivity, 'timeActivity': timeActivity}

jsonsOccupants.append(jsonOccupant)


##Generación de mapa (ignorar)

with open('labgsi.blueprint3d') as data_file:
	NITEMS = 0
	data = json.load(data_file)
	corners = {}
	walls = {}
	items = {}
	offsety = 10
	offsetx = 1 
	flor = data["floorplan"]
	for k, v in flor["corners"].items():
		corners[k] = {"x":  v["x"]/100 + offsetx,"y": -v["y"]/100 + offsety}

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
			#rot = min(myList, key=lambda x:abs(x-abs(k["rotation"])))
			rotAux =  k["rotation"]
			rot = 'x' if ((rotAux == 0) or (rotAux == math.pi)) else 'y'
			if rot == 'x':
				dx = k["width"]
				dy = k["depth"]
			else:
				dy = k["width"]
				dx = k["depth"]
			items["idItem" + str(n)] = {"itemType": k["item_type"], "pos": { "x": k["xpos"]/100 + offsetx, "y":  -k["zpos"]/100 + offsety}, "dx" :dx/100, "dy" :dy/100}
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
				items["idItem" + str(n+1000)] = {"itemType": k["item_type"], "pos": { "x": k["xpos"]/100 + offsetx, "y": -k["zpos"]/100 + offsety}, "dx" :dx/100, "dy" :dy/100, 'rot': rot}
				items["idItem" + str(n+1000)]["itemType"] = "door"
			n = n + 1
	jsonResponse = {"corners": corners, "walls": walls, "items": items}

cellW = 40
cellH = 40


# Seleccionar ejecución: Visual (-v) o Batch (-v)
# Descomentar la que proceda y comentar la otra

visual = Visualization(cellW, cellH, canvas_width=500, canvas_height=500)

#Visual run

run.run(SEBAModel, [visual], cellW, cellH, jsonResponse, jsonsOccupants, dt.datetime.now(), 0.5)

#Batch run
'''
fixed_params = {"width": 120,
				"height": 120,
				"jsonMap": jsonResponse,
				"jsonsOccupants": jsonsOccupants,
				"scale": 2
				}

variable_params = {"seed": range(10, 500, 10)}

run.run(SEBAModel, fixed_params, variable_params, iterations = 1)
'''