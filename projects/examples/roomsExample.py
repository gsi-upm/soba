from soba.models.roomsModel import RoomsModel
import soba.run
from collections import OrderedDict
from time import time
import sys

class ModelExample(RoomsModel):

	def __init__(self, width, height, jsonMap, jsonsOccupants, seed = int(time())):
		super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed)

	def step(self):
		if self.clock.clock.day > 3:
			self.finishSimulation = True
		super().step()

jsonMap = {

  'Pos1': {'entrance':'', 'conectedTo': {'U':'Pos2'}, 'measures': {'dx':2, 'dy':2}},
  'Pos2': {'measures': {'dx':3, 'dy':3.5}, 'conectedTo': {'R':'Pos3'}},
  'Pos3': {'measures': {'dx':3, 'dy':3.5}}

	}

jsonsOccupants = []

N = 3

states = OrderedDict([('out','Pos1'), ('Working in my laboratory', {'Pos2': 1, 'Pos3': 2})])

schedule = {'t1': "09:00:00", 't2': "13:00:00", 't3': "14:10:00"}

variation = {'t1': "00:10:00", 't2': "01:20:00", 't3': "00:20:00"}

markovActivity = {
	'-t1': [[100, 0], [0, 0]],
	't1-t2': [[50, 50], [0, 0]],
	't2-t3': [[0, 0], [50, 0]],
	't3-': [[0, 50], [10, 90]]
}

timeActivity = {
	'-t1': [60, 0],
	't1-t2': [2, 60],
	't2-t3': [60, 10],
	't3-': [60, 20]
}


jsonOccupant = {'type': 'example' , 'N': N, 'states': states , 'schedule': schedule, 'variation': variation, 
	'markovActivity': markovActivity, 'timeActivity': timeActivity}

jsonsOccupants.append(jsonOccupant)

cellW = 4
cellH = 4

if len(sys.argv) > 1 and sys.argv[1] == '-v':
	parameters = {'width': cellW, 'height': cellH, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants}
	soba.run.run(ModelExample, parameters, visualJS="example.js")
else:
	fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
	variable_params = {"seed": range(10, 500, 10)}
	soba.run.run(ModelExample, fixed_params, variable_params)



#Visual run
"""


#Batch run

fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
variable_params = {"seed": range(10, 500, 10)}

soba.run.run(ModelExample, fixed_params, variable_params)
"""