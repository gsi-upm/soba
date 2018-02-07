from soba.models.continuousModel import ContinuousModel
import soba.visualization.ramen.mapGenerator as ramen
import soba.run
from collections import OrderedDict
import json
from time import time
import sys

class ModelExample(ContinuousModel):

	def __init__(self, width, height, jsonMap, jsonsOccupants, seed = int(time())):
		super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed, timeByStep = 0.1)

	def step(self):
		if self.clock.clock.hour > 9:
			self.finishSimulation = True
		super().step()

jsonsOccupants = []

N = 1

states = OrderedDict([('Leaving','out'), ('Resting', 'sofa'), ('Working in my laboratory', 'wp')])

schedule = {'t1': "08:01:00", 't2': "13:00:00", 't3': "14:10:00"}

variation = {'t1': "00:00:00", 't2': "01:20:00", 't3': "00:20:00"}

markovActivity = {
	'-t1': [[100, 0, 0], [0, 0, 0], [0, 0, 0]],
	't1-t2': [[30, 40, 30], [0, 50, 50], [0, 50, 50]],
	't2-t3': [[0, 0, 0], [50, 50, 0], [0, 0, 0]],
	't3-': [[0, 50, 50], [10, 90, 0], [0, 0, 0]]
}

timeActivity = {
	'-t1': [3, 0, 0], 't1-t2': [2, 60, 15], 't2-t3': [60, 10, 15], 't3-': [60, 20, 15]
}

jsonOccupant = {'type': 'example' , 'N': N, 'states': states , 'schedule': schedule, 'variation': variation, 
	'markovActivity': markovActivity, 'timeActivity': timeActivity}

jsonsOccupants.append(jsonOccupant)

with open('labgsi.blueprint3d') as data_file:
	jsonMap = ramen.returnMap(data_file)

cellW = 40
cellH = 40

if len(sys.argv) > 1 and sys.argv[1] == '-v':
	parameters = {'width': cellW, 'height': cellH, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants}
	soba.run.run(ModelExample, parameters, visualJS="example.js")
else:
	fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
	variable_params = {"seed": range(10, 500, 10)}
	soba.run.run(ModelExample, fixed_params, variable_params)

#Visual run
'''
parameters = {'width': cellW, 'height': cellH, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants}
soba.run.run(ModelExample, parameters, visualJS="example.js")
'''

#Batch run
'''
fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
variable_params = {"seed": range(10, 500, 10)}

soba.run.run(ModelExample, fixed_params, variable_params)
'''