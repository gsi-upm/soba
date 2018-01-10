import sys
import soba.launchers.visual as visual
from mesa.batchrunner import BatchRunner as batch
"""
In the file run.py is implemented the method
	Methods: 
		-run: This method is implemented to start the execution of the simulation.

"""

def process(aux):
	if aux == True:
		print('SOBA is running')
	else:
		print('\n Wrong params :(\n')
		print('   Options:\n\t-v,\t\tVisual option on browser\n\t-b,\t\tBackground option\n\t-r,\t\tRamen option')
		print(' ')

def run(model, *args, iterations = 1):
	"""
	Execution of the simulation according to the parameters given in the console.
		Args:
			model: Model that is simulated.
			args: List of parameters to configure the models simulation.
			iterations: Number of simulations that will be executed in batch mode.
	"""
	if len(sys.argv) > 1:
		if sys.argv[1] == '-v':
			process(True)
			visual.run(model, *args)
		elif sys.argv[1] == '-b':
			process(True)
			batch.run(model, *args, iterations = iterations, ramen=False)
		elif sys.argv[1] == '-r':
			process(True)
			batch.run(model, *args, iterations = iterations, ramen=True)
		else:
			process(False)
	else:
		process(False)