#!/usr/bin/python
import sys
import os
import soba.launchers.visual
import soba.launchers.batch

def process(aux):
	if aux == True:
		print('SOBA is running')
	else:
		print('\n   Wrong params :(\n')
		print('   Options:\n\t-v,\t\tVisual option on browser\n\t-b,\t\tBackground option')
		print(' ')

def run(model, *args, iterations = 1):
	if len(sys.argv) > 1:
		if sys.argv[1] == '-v':
			process(True)
			soba.launchers.visual.run(model, *args)
		elif sys.argv[1] == '-b':
			process(True)
			soba.launchers.batch.run(model, *args, iterations)
		else:
			process(False)
	else:
		process(False)