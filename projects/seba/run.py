from soba.models.continuousModel import ContinuousModel
import soba.visualization.ramen.mapGenerator as ramen
import soba.run
from collections import OrderedDict
import json
from time import time
import sys
from model import SEBAModel
from visualization.back import Visualization
import datetime as dt

strategies = ['nearest', 'safest', 'uncrowded']

# Simulation configuration
today = dt.date.today()

timeHazard = "10:00:00"


 #Only two are neccesary 

families = []

sebaConfiguration = {'families': families, 'hazard': timeHazard}

# Occupancy atributtes

jsonsOccupants = []

strategy = strategies[0]

N = 8
NDis = 2

speed = 1.38
speedDis = 0.7



states = OrderedDict([('Free time','out'), ('Rest', 'sofa'), ('Lunch','out'), ('Work', 'wp')])

schedule = {'t1': "09:30:00", 't2': "13:20:00", 't3': "15:00:00", 't4': "18:00:00"}

variation = {'t1': "00:30:00", 't2': "00:30:00", 't3': "00:30:00", 't4': "00:59:00"}

markovActivity = {

    '-t1': [[100, 0, 0, 0], [100, 0, 0, 0], [100, 0, 0, 0], [100, 0, 0, 0]],
    't1-t2': [[0, 30, 0, 70], [0, 10, 0, 90], [0, 20, 0, 80], [0, 40, 0, 60]],
    't2-t3': [[100, 0, 0, 0], [0, 10, 20, 60], [20, 10, 50, 40], [0, 10, 70, 30]],
    't3-t4': [[100, 0, 0, 0], [0, 10, 20, 60], [20, 10, 0, 70], [30, 10, 0, 60]],
    't4-': [[100, 0, 0, 0], [70, 0, 0, 30], [70, 0, 0, 30], [70, 0, 0, 30]]

}

timeActivity = {
    '-t1': [3, 0, 0, 0], 't1-t2': [0, 10, 0, 45], 't2-t3': [0, 10, 50, 45], 't3-t4': [0, 10, 20, 45], 't4-': [3, 10, 10, 20]
}


timeActivityVariation = {
    '-t1': [0, 0, 0, 0], 't1-t2': [0, 5, 0, 10], 't2-t3': [0, 5, 10, 10], 't3-t4': [0, 10, 5, 10], 't4-': [0, 5, 5, 10]
}

jsonOccupant = {'type': 'regular' , 'N': N, 'states': states , 'schedule': schedule, 'variation': variation,
'markovActivity': markovActivity, 'timeActivity': timeActivity, 'timeActivityVariation': timeActivityVariation,
'strategy': strategy, 'speedEmergency': speed}

jsonsOccupants.append(jsonOccupant)

jsonOccupantDis = {'type': 'dis' , 'N': NDis, 'states': states , 'schedule': schedule, 'variation': variation,
'markovActivity': markovActivity, 'timeActivity': timeActivity, 'timeActivityVariation': timeActivityVariation,
'strategy': strategy, 'speedEmergency': speedDis}

jsonsOccupants.append(jsonOccupantDis)

with open('auxiliarFiles/labgsi.blueprint3d') as data_file:
	jsonMap = ramen.returnMap(data_file, offsety = 9, offsetx = 0)

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