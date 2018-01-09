from soba.visualization.drawModelBack import BackEndVisualization
from soba.visualization.server import ModularServer
import random

"""
In the file visual.py is implemented the execution with visual representation:
	Methods: 
		-run: Execute the simulation with visual representation.

"""

def run(model, visualJS = [], *params):
	"""
	Execute the simulation with visual representation.
		Args:
			model: Model that is simulated.
			visualJS: JS files with the visualization elements that are included in the JavaScript browser visualization template.
			params: Parameters loaded in the models about the agents and anything else.
	"""
	backEndVisualization = BackEndVisualization(params[0], params[1], 500, 500)
	if visualJS:
		listAux = [backEndVisualization] + visualJS
	else:
		listAux = [backEndVisualization]
	method = 'ModularServer(models, listAux, "Simulation"'
	n=0
	for e in params:
		method = method+',params['+str(n)+']'
		n = n +1
	method = method + ')'
	server = eval(method)
	server.port = 7777
	server.launch()