from soba.visualization.drawModelBack import BackEndVisualization
from soba.visualization.server import ModularServer
import random

def run(model, visualJS = [], *params):
	print(*params)
	backEndVisualization = BackEndVisualization(params[0], params[1], 500, 500)
	if visualJS:
		listAux = [backEndVisualization] + visualJS
	else:
		listAux = [backEndVisualization]
	method = 'ModularServer(model, listAux, "Simulation"'
	n=0
	for e in params:
		method = method+',params['+str(n)+']'
		n = n +1
	method = method + ')'
	server = eval(method)
	server.port = 7777
	server.launch()