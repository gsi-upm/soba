from soba.visualization.drawModelBack import MapVisualization
from soba.visualization.server import ModularServer
import random

def occupancyVisualization(agent):
    json = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": agent.color,
                 "r": 0.5}
    return json

def run(model, visual = None, *params):
	mapVisualization = MapVisualization(occupancyVisualization, params[0], params[1], 500, 500)
	if visual != None:
		listAux = [mapVisualization] + visual
	else:
		listAux = [mapVisualization]
	method = 'ModularServer(model, listAux, "Simulation"'
	n=0
	for e in params:
		method = method+',params['+str(n)+']'
		n = n +1
	method = method + ')'
	server = eval(method)
	server.port = 8882
	server.launch()