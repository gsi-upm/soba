from soba.agents.agent import Occupant
from soba.model.model import RoomsModel
import soba.run
from collections import OrderedDict
import datetime as dt

class ModelExample(RoomsModel):

	def __init__(self, width, height, jsonRooms, jsonsOccupants, seed):
		super().__init__(width, height, jsonRooms, jsonsOccupants, seed)

	def step(self):
		super().step()
		if (int(self.clock.day) == 5):
			PID = os.system('$!')
			os.system('kill ' + str(PID))

jsonRooms = {

  'Pos1': {'entrance':'', 'conectedTo': {'U':'Pos2'}, 'measures': {'dx':2, 'dy':2}},
  'Pos2': {'measures': {'dx':3, 'dy':3.5}, 'conectedTo': {'R':'Pos3'}},
  'Pos3': {'measures': {'dx':3, 'dy':3.5}}

	}

jsonsOccupants = []

N = 2
states = OrderedDict([('out','Pos1'), ('Working in my laboratory', {'Pos2': 1, 'Pos3': 2})])

schedule = {'s': "00:00:00", 't1': "08:50:00", 't2': "13:00:00", 't3': "14:10:00", 'e': "23:59:59"}

markovActivity = {
	's-t1': [[100, 0], [0, 0]],
	't1-t2': [[50, 50], [0, 0]],
	't2-t3': [[0, 0], [50, 0]],
	't3-e': [[0, 50], [10, 90]]
}

timeActivity = {
	's-t1': [60, 0],
	't1-t2': [2, 60],
	't2-t3': [60, 10],
	't3-e': [60, 20]
}


jsonOccupant = {'type':'example' , 'N':N, 'states': states , 'schedule': schedule, 'markovActivity': markovActivity, 'timeActivity': timeActivity}

jsonsOccupants.append(jsonOccupant)

#Visual run

soba.run.run(ModelExample, 3, 3, jsonRooms, jsonsOccupants, dt.datetime.now())

#Batch run

'''
fixed_params = {"width": 3,
                "height": 3,
                "jsonRooms": jsonRooms,
                "jsonsOccupants": jsonsOccupants}
variable_params = {"N": range(10, 500, 10)}

soba.run.run(ModelExample, fixed_params, variable_params, iterations = 1)
'''