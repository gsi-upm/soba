import random
import datetime
from soba.agents.agent import Agent

"""
In the file timeControl.py three classes are defined:

	-Time: Class that inherits of the Agent class to manage the time in sexagesimal units. 
	-BaseScheduler: Class to store and manage the activation of agents added to the models's schedule.
	-RandomActivation: Class that inherits from the BaseScheduler class. Add random activation.

"""

class Time(Agent):
	"""
	Class that inherits of the Agent class to manage the time in sexagesimal units.

		Attributes:
			clock: Clock for time monitoring during simulation.
			timeByStep: Time in seconds associated with each step.
			startDay: Time of the beginning of a day in the simulation.
			endDay: Time of the end of a day in the simulation.
		Methods:
			step: Advance of the clock in a step.
			increaseTime: Increase the value of the clock a given time.
			decreaseTime: Decrease the value of the clock a given time.
	"""

	def __init__(self, model, timeByStep = 1, day = 1, hour = 7, minute = 0, seg = 0, microsecond = 0):
		super().__init__(100000, model)
		"""
		Create a new Time object.
			Args: 
				models: Associated Model object.
				timeByStep: Time in seconds associated with each step.
				day, hour, minute, seg, microsecond: Initial time value of the clock.
			Return: Time object.
		"""
		self.timeByStep = timeByStep
		today = datetime.date.today()
		self.startDay = datetime.datetime(today.year, today.month, day, hour, minute, seg, microsecond)
		self.endDay = datetime.datetime(today.year, today.month, 1, 20, 0, 0, 0)
		self.clock = self.startDay

	def increaseTime(self, seconds=0, days=0, hours=0, minutes=0, microseconds=0):
		"""
		Increase the value of the clock a given time.
			Args:
				seconds, days, hours, minutes, microseconds: Time value to be increase.
			Return: The new Clock object.
		"""
		clockOld = self.clock
		dayOld = clockOld.day
		clockNew = clockOld + datetime.timedelta(days=days, minutes=minutes, seconds=seconds, microseconds=microseconds)
		if clockNew.hour >= self.endDay.hour and clockNew.minute > self.endDay.minute:
			clockNew = datetime.datetime(2107, 1, dayOld+1, self.startDay.hour, self.startDay.minute, 0, 0)
			+ (clockNew - self.endDay)
		return clockNew

	def decreaseTime(self, days=0, hours=0, minutes=0, seconds=0, microseconds=0):
		"""
		Decrease the value of the clock a given time.
			Args:
				seconds, days, hours, minutes, microseconds: Time value to be decrease.
			Return: The new Clock object.
		"""
		clockOld = self.clock
		clockNew = clockOld - datetime.timedelta(days=days, minutes=minutes, seconds=seconds, microseconds=microseconds)
		return clockNew

	def step(self):
		"""Advance of the clock in a step."""
		self.clock = self.increaseTime(self.timeByStep)
		print(self.clock.strftime("%d:%H:%M:%S"))

class BaseScheduler():
	"""
	Class to store and manage the activation of agents added to the models's schedule.
	The agents are activated in the order in which they were added.
	
		Attributes:
			steps: Measurement of the progress of the simulation. In each step the agents perform actions in the models.
			agents: List of agents that are included in the scheduler and are activated in each step.
			
		Methods:
			add: Add an agent to the scheduler.
			remove: Remove an agent from the scheduler.
			step: Advances in the simulation, activating the action of the agents.
			getAgentCount: Get number of agents that are included in the scheduler.
	"""
	def __init__(self, model):
		"""
		Create a new BaseScheduler object.
			Args: 
				model: Associated Model object.
			Return: BaseScheduler object
		"""
		self.model = model
		self.steps = 0
		self.agents = []

	def add(self, agent):
		"""
		Add an agent to the scheduler.
			Args:
				agent: Agent to be added.
		"""
		self.agents.append(agent)

	def remove(self, agent):
		"""
		Remove an agent from the scheduler.
			Args:
				agent: Agent to be removed.
		"""
		while agent in self.agents:
			self.agents.remove(agent)

	def step(self):
		""" Advances in the simulation, activating the action of the agents, following the orded in which they were added."""
		for agent in self.agents:
			agent.step()
		self.steps += 1

	def getAgentCount(self):
		"""
		Get number of agents that are included in the scheduler.
			Return: Number of agents.
		"""
		return len(self.agents)

class RandomActivation(BaseScheduler):
	"""
	Class that inherits from the BaseScheduler class. Manage the activation of agents added 
	to the models's schedule following a random order.
	
		Attributes:
			Those inherited from the BaseScheduler class.
		Methods:
			step: Advances in the simulation, activating the action of the agents.
	"""
	def step(self):
		""" Advances in the simulation, activating the action of the agents, following a random order."""
		random.shuffle(self.agents)
		for agent in self.agents:
			agent.step()
		self.steps += 1
		self.time += 1