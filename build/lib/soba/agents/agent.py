class Agent():
	"""
	Base class to create Agent objects.
	The agents are controlled by the scheduler of the Model associated.

	Attributes:
		model: Model associated to the agent.
		unique_id: Unique id of the agent.
		color: Color with which the agent will be represented in the visualization.
	Methods:
		step: Method invoked by the Model scheduler in each step. Step common to all Agents.
	"""

	def __init__(self, unique_id, model):
		"""
		Create a new Agent object.
			Args: 
				unique_id: Unique identifier corresponding to the agent.
				model: Associated Model object.
			Return: Agent object
		"""
		self.unique_id = unique_id
		self.model = model
		self.model.schedule.add(self)
		self.color = 'orange'
		self.shape = 'circle'

	def step(self):
		"""Method invoked by the Model scheduler in each step. Step common to all Agents."""
		pass