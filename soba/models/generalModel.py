from collections import defaultdict
import random
import os
import os.path
import math
from soba.models.timeControl import Time
from soba.agents.occupant import ContinuousOccupant
from soba.agents.occupant import RoomsOccupant
import soba.agents.modules.aStar as aStar
from soba.space.roomsItems import Room
from soba.space.roomsItems import Door as DoorRooms
from soba.space.roomsItems import Wall as WallRooms
from soba.space.continuousItems import GeneralItem
from soba.space.continuousItems import Door
from soba.space.continuousItems import Wall
from soba.space.continuousItems import Poi
from soba.models.timeControl import BaseScheduler
import datetime as dt
import random
from mesa.space import Grid
import soba.visualization.ramen.performanceGenerator as ramen
from mesa import Model
from mesa.time import SimultaneousActivation

class GeneralModel(Model):
	"""
	Base Class to create simulation models.
	It creates and manages space and agents.

		Attributes:
			height: Height in number of grid cells.
			width: Width in number of grid cells.
			schedule: BaseScheduler object for agent activation.
			grid: Grid object to implement space.
			running: Parameter to control the models execution.
			NStep: Measure of the number of steps.
			occupants: List of Occupant objects created.
			agents: List of the all Agent objects created.
			asciMap: Representation of the map as ASCI used to get FOV information.
			seed: Seed employ in random generations.
			finishSimulation: Parameter to stop the software simulation.
		Methods:
			finishTheSimulation: Finish with the execution of the simulation software.
			run_model: Model execution.
			step: Execution of the scheduler steps.

	"""

	def __init__(self, width, height, seed = dt.datetime.now(), timeByStep = 60):
		super().__init__(seed)
		"""
		Create a new Model object.
			Args:
				height: Height in number of grid cells.
				width: Width in number of grid cells.
				schedule: BaseScheduler object for agent activation.
				grid: Grid object to implement space.
				running: Parameter to control the models execution.
				NStep: Measure of the number of steps.
				occupants: List of Occupant objects created.
				agents: List of the all Agent objects created.
				asciMap: Representation of the map as ASCI used to get FOV information.
				seed: Seed employ in random generations.
				finishSimulation: Parameter to stop the software simulation.
			Return: Model object
		"""

		self.width = width
		self.height = height
		self.schedule = SimultaneousActivation(self)
		self.grid = Grid(width, height)
		self.agents = []
		self.NStep = 0
		self.occupants = []
		self.clock = Time(self, timeByStep = timeByStep)
		self.asciMap = []
		self.finishSimulation = False

	def finishTheSimulation(self):
		"""Finish with the execution of the simulation software."""
		PID = os.system('$!')
		os.system('kill ' + str(PID))

	def step(self):
		"""Main step of the simulation, execution of the scheduler steps."""
		if self.finishSimulation:
			self.finishTheSimulation()
		self.schedule.step()
		self.NStep = self.NStep + 1