from soba.models.continuousModel import ContinuousModel
import soba.visualization.ramen.mapGenerator as ramen
import soba.run
from collections import OrderedDict
import json
from time import time
import sys
from model import SEBAModel
from visualization.back import Visualization

strategies = ['nearest', 'safest', 'uncrowded']

# Simulation configuration

families = []

family1 = {'N': 3, 'child': 1, 'adult': 2} #Only two are neccesary 
family2 = {'N': 3, 'child': 2, 'adult': 1}
families.append(family1)
families.append(family2)

sebaConfiguration = {'families': []}

# Occupancy atributtes

jsonsOccupants = []

N = 4

states = OrderedDict([('Leaving','out'), ('Resting', 'sofa'), ('Working in my laboratory', 'wp')])

schedule = {'t1': "08:01:00", 't2': "13:20:00", 't3': "14:10:00"}

variation = {'t1': "00:01:00", 't2': "00:01:00", 't3': "00:20:00"}

markovActivity = {
	'-t1': [[100, 0, 0], [0, 0, 0], [0, 0, 0]],
	't1-t2': [[0, 100, 0], [0, 0, 100], [0, 0, 100]],
	't2-t3': [[100, 0, 0], [60, 40, 0], [60, 0, 40]],
	't3-': [[0, 0, 100], [0, 100, 0], [0, 100, 0]]
}

timeActivity = {
	'-t1': [3, 0, 1], 't1-t2': [1, 0, 4], 't2-t3': [60, 10, 15], 't3-': [5, 100, 15]
}

timeActivityVariation = {
	'-t1': [0, 0, 0], 't1-t2': [0, 5, 2], 't2-t3': [5, 2, 3], 't3-': [0, 13, 3]
}

jsonOccupant = {'type': 'sebaOccupant' , 'N': N, 'states': states , 'schedule': schedule, 'variation': variation, 
	'markovActivity': markovActivity, 'timeActivity': timeActivity, "timeActivityVariation": timeActivityVariation, 
	'strategy': strategies[0], 'speedEmergency': 'np.random.normal(1.15, 0.15)'}


jsonsOccupants.append(jsonOccupant)

with open('auxiliarFiles/labgsi.blueprint3d') as data_file:
	jsonMap = ramen.returnMap(data_file)

cellW = 20
cellH = 20

if len(sys.argv) > 1 and sys.argv[1] == '-v':
	back = Visualization(cellW, cellH)
	parameters = {'width': cellW, 'height': cellH, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants, 'sebaConfiguration': sebaConfiguration}
	soba.run.run(SEBAModel, parameters, visualJS="visualization/front.js", back=back)
else:
	fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants, 'sebaConfiguration': sebaConfiguration}
	variable_params = {"seed": range(10, 500, 10)}
	soba.run.run(SEBAModel, fixed_params, variable_params)