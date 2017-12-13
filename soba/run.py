import sys
import soba.launchers.visual as visual
import soba.launchers.batch as batch

def process(aux):
	if aux == True:
		print('SOBA is running')
	else:
		print('\n Wrong params :(\n')
		print('   Options:\n\t-v,\t\tVisual option on browser\n\t-b,\t\tBackground option\n\t-r,\t\tRamen option')
		print(' ')

def run(model, *args, iterations = 1):
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