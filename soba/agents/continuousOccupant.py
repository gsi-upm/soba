import random
import soba.agents.resources.aStar as aStar
import soba.agents.resources.fov as fov
import soba.visualization.ramen.performanceGenerator as ramen
from soba.agents.occupant import Occupant
import time

class ContinuousOccupant(Occupant):
	"""
	This class enables to create occupants that are modelled with a continuous space models.
	based on considering a scaled grid (x, y). Cell size of 0.5m ^ 2 by default.
	The occupants are agents with their activity defined by markov states.

	Attributes:
		Those Inherited from the Occupant class.
		fov: List of positions (x, y) that the occupant can see.
	
	Methods:
		getPosState: Auxiliary method to distribute the occupants between the points of interests with same id for more than one occupant.
		getWay: Invocation of the AStar resource to calculate the optimal path.
		getPlaceToGo: Obtaining the position associated with the current state.
		posInMyFOV: Check if a position is in my field of vision.
		evalAvoid: Check the future movement to be made by another agent to assess a possible collision.
		evalCollision: Evaluate a possible collision with an agent and solve it if necessary by calculating another path.
		makeMovement: Carry out a movement: displacement between cells or reduction of the movement cost parameter.
		getFOV: Calculation of the occupant's field of vision, registered in the attribute fov.
		step: Method invoked by the Model scheduler in each step.
	
	"""
	global ramenAux
	ramenAux = False
	def activeRamen():
		global ramenAux
		ramenAux = True

	def __init__(self, unique_id, model, json, speed = 0.7):
		super().__init__(unique_id, model, json, speed)
		"""
		Create a new ContinuousOccupant object.
			Args: 
				unique_id: Unique identifier corresponding to the Occupant.
				models: Associated Model object, by default ContinuousModel.
				json: Json of definition of parameters of behavior
				speed: Movement speed in m/s
			Return: ContinuousOccupant object
		"""

		self.pov = []

		#Control params.
		self.costMovement = round(0.25/(self.speed*self.model.clock.timeByStep))
		self.out = True
		self.initmove = True
		self.posEntering = False

		#State machine
		for k, v in json['states'].items():
			pos = self.getPosState(v)
			self.positionByState[k] = pos
		pos = self.positionByState[list(json['states'].items())[0][0]]
		self.model.grid.place_agent(self, pos)

	def getPosState(self, name):
		'''
		Auxiliary method to distribute the occupants between the points of interests with same id for more than one occupant.
			Args:
				name: Poi id/name.
			Return: Position associated with this occupant.
		'''
		options = []
		for poi in self.model.pois:
			if poi.id == name and (poi.share or not poi.used):
				if not poi.share:
					poi.used = True
					time.sleep(50)
					return poi.pos
				options.append(poi.pos)
		return random.choice(options)

	def startActivity(self):
		super.startActivity()

	def getWay(self, pos = None, pos_to_go = None, other = []):
		'''
		Invocation of the AStar resource to calculate the optimal path.
			Args:
				pos: Initial position, by default the current position of the occupant.
				pos_to_go: Final position, by default the value of the 'pos_to_go' attribute of the occupant.
				other: List of auxiliary positions given to be considered impenetrable by the occupants, 
				that is, they will not be used by the AStar.
			Return: List of positions (x, y).
		'''
		posSend = pos
		pos_to_goSend = pos_to_go
		if pos == None:
			posSend = self.pos
		if pos_to_go == None:
			pos_to_goSend = self.pos_to_go
		return aStar.getPathContinuous(self.model, posSend, pos_to_goSend, other)

	def getPlaceToGo(self):
		'''
		Obtaining the position associated with the current state. It is invoked when you enter a new state.
			Return: Position as coordinate (x, y).
		'''
		pos_to_go = self.positionByState[self.state]
		return pos_to_go

	def posInMyFOV(self, pos):
		'''
		Check if the position is in my field of vision
			Args: 
				pos: Position to be checked
			Return: Boolean
		'''
		if pos in self.pov:
			return True
		return False

	def evalAvoid(self, otherAgent):
		'''
		Check the future movement to be made by another agent to assess a possible collision.
			Args: 
				otherAgent: The other agent to be avoid.
			Return: Boolean
		'''
		if otherAgent.pos == otherAgent.pos_to_go:
			return False
		collision = [()]
		before1 = self.pos
		before2 = otherAgent.pos
		after1 = self.movements[self.N]
		after2 = otherAgent.movements[otherAgent.N]
		if before1 == after2 and before2 == after1:
			return False
		return True

	def evalCollision(self):
		"""
		Evaluate a possible collision with an agent, invoking the evalAvoid method, and solve it if necessary by calculating another path.
			Return: True if the collision exists and is avoided, False otherwise.
		"""
		possibleOccupant = self.model.grid.get_cell_list_contents(self.movements[self.N])
		for i in possibleOccupant:
			if isinstance(i, Occupant):
				if len(self.movements) - 1 == self.N:
					return False
				if self.evalAvoid(i):
					return False
				x1, y1 = self.pos
				x2, y2 = self.movements[self.N]
				possiblePosition1 = [(x1, y1 + 1), (x1 + 1, y1), (x1 - 1, y1), (x1, y1 - 1)]
				possiblePosition2 = [(x1 + 1, y1 + 1), (x1 + 1, y1 - 1), (x1 - 1, y1 - 1), (x1 - 1, y1 + 1)]
				possiblePosition = possiblePosition2 + possiblePosition1

				d = 100000000;
				pos = (0, 0)
				path = []
				for nextPos in possiblePosition:
					if aStar.canMovePos(self.model, self.pos, nextPos):
						pathAux = self.getWay(nextPos, other = [x2, y2])
						dAux = len(pathAux)
						if dAux < d:
							d = dAux
							pos = nextPos
							path = pathAux
				if d != 100000000:
					self.model.grid.move_agent(self, pos)
					self.movements = path
					self.N = 0
					return True
				else:
					while True:
						posRandom = random.choice(possiblePosition)
						if aStar.canMovePos(self.model, self.pos, posRandom):
							self.model.grid.move_agent(self, posRandom)
							self.movements = self.getWay()
							self.N = 0
							return True
		return False

	def makeMovement(self):
		'''Carry out a movement: displacement between cells or reduction of the movement cost parameter.'''
		if self.costMovement > 1:
			self.costMovement = self.costMovement - 1
			
			if ramenAux:
				self.reportMovement()
		else:
			if self.initmove:
				if self.pos != self.pos_to_go:
					x1, y1 = self.pos
					x2, y2 = self.movements[self.N]
					rect = True
					if x1!=x2 and y1!=y2:
						rect = False
					if rect == True:
						self.costMovement = round(0.5/(self.speed*self.model.clock.timeByStep))
					else:
						self.costMovement = round(0.707106781/(self.speed*self.model.clock.timeByStep))
					self.initmove = False
					self.step()
					return
			if not self.evalCollision():
				if ramenAux:
					self.reportMovement()
				self.model.grid.move_agent(self, self.movements[self.N])
				if self.pos != self.pos_to_go:
					self.N = self.N+1
					x1, y1 = self.pos
					x2, y2 = self.movements[self.N]
					rect = True
					if x1!=x2 and y1!=y2:
						rect = False
					if rect == True:
						self.costMovement = round(0.5/(self.speed*self.model.clock.timeByStep))
					else:
						self.costMovement = round(0.707106781/(self.speed*self.model.clock.timeByStep))
				else:
					self.costMovement = round(0.5/(self.speed*self.model.clock.timeByStep))

	def reportMovement(self):
		x1, y1 = self.pos
		x2, y2 = self.movements[self.N]
		pos = ''
		if x2 > x1 and y2 > y1:
			pos = 'NE'
		elif x2 > x1 and y2 == y1:
			pos = 'E'
		elif x1 > x2 and y2 == y1:
			pos = 'W'
		elif x1 > x2 and y1 > y2:
			pos = 'SW'
		elif y2 > y1 and x2 == x1:
			pos = 'N'
		elif x1 == x2 and y1 > y2:
			pos = 'S'
		elif x1 > x2 and y2 > y1:
			pos = 'NW'
		elif x2 > x1 and y1 > y2:
			pos = 'SE'
		else:
			ramen.reportStop(self)
			return
		ramen.reportMovement(self, pos)

	def checkLeaveArrive(self):
		print(self.pos_to_go)
		if (self.pos_to_go not in self.model.exits) and not self.inbuilding:
			self.alreadyCreated = False
			ramen.reportCreation(self, 'E')
			self.inbuilding = True
		elif self.pos in self.model.exits and self.inbuilding:
			self.inbuilding = False
			ramen.reportExit(self)

	def getFOV(self):
		'''Calculation of the occupant's field of vision, registered in the attribute fov'''
		asciMap = self.model.asciMap
		fovMap, flag = fov.makeFOV(asciMap, self.pos)
		self.fov = []
		for index1, line in enumerate(fovMap):
			for index2, element in enumerate(line):
				if element == flag:
					self.fov.append((index2, index1))

	def step(self):
		"""
		Method invoked by the Model scheduler in each step. Evaluate if appropriate and, if so, perform: 
		A change of state, a movement or advance in the cost of a movement, or an advance in the performance of an activity.
		"""
		if self.markov == True or self.changeSchedule():
			self.markov_machine.runStep(self.markovActivity[self.getPeriod()])
		elif self.pos != self.pos_to_go:
			self.makeMovement()
		elif self.time_activity > 0:
			self.time_activity = self.time_activity - 1
		else:
			self.markov = True
			self.step()
		if ramenAux:
			self.checkLeaveArrive()
