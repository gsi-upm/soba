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
		self.createOccupants(jsonsOccupants)

	def step(self):
		if self.clock.clock.hour > 17:
			self.finishSimulation = True
		super().step()

jsonsOccupants = []

#Number of occupants
N = 3

#Definition of the states
states = OrderedDict([('Leaving','out'), ('Resting', 'sofa'), ('Working in my laboratory', 'wp')])

#Definition of the schedule
schedule = {'t1': "08:00:00", 't2': "09:00:00", 't3': "14:10:00"}

#Possible Variation on the schedule
variation = {'t1': "00:01:00", 't2': "00:01:00", 't3': "00:20:00"}

#Probability of state change associated with the Markovian chain as a function of the temporal period
markovActivity = {
	'-t1': [[100, 0, 0], [0, 0, 0], [0, 0, 0]],
	't1-t2': [[0, 0, 100], [0, 50, 50], [0, 50, 50]],
	't2-t3': [[100, 0, 0], [0, 50, 50], [0, 50, 50]],
	't3-': [[0, 0, 100], [0, 100, 0], [0, 100, 0]]
}

#Time associated to each state (minutes)
timeActivity = {
	'-t1': [1, 0, 0], 't1-t2': [10, 10, 10], 't2-t3': [10, 10, 10], 't3-': [1, 1, 1]
}

timeActivityVariation = {
	'-t1': [0, 0, 0], 't1-t2': [0, 0, 0], 't2-t3': [0, 0, 0], 't3-': [0, 0, 0]
}

#Store the information
jsonOccupant = {'type': 'example' , 'N': N, 'states': states , 'schedule': schedule, 'variation': variation, 
	'markovActivity': markovActivity, 'timeActivity': timeActivity, "timeActivityVariation": timeActivityVariation}

jsonsOccupants.append(jsonOccupant)

with open('labgsi.blueprint3d') as data_file:
	jsonMap = ramen.returnMap(data_file)

cellW = 40
cellH = 40

if len(sys.argv) > 1 and sys.argv[1] == '-v':
	parameters = {'width': cellW, 'height': cellH, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants}
	soba.run.run(ModelExample, parameters, visualJS="example.js")
else:
	#Fixed parameters during iterations
	fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
	#Variable parameters to each iteration
	variable_params = {"seed": range(10, 500, 10)}
	soba.run.run(ModelExample, fixed_params, variable_params)