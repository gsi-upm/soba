from soba.agents.continuousOccupant import ContinuousOccupant
import random
import sys
import soba.agents.resources.aStar as aStar
import numpy as np
from avatar import EmergencyAvatar
from ast import literal_eval as make_tuple
import ast

class EmergencyOccupant(ContinuousOccupant):
	"""
	
	This class enables to create occupants defined to work in an emergency modeling.
	This class inherits from the ContinuousOccupant class of SOBA.

	Attributes:
		Those Inherited from the ContinuousOccupant class of SOBA.
		children: Children associated with the occupant.
		parents: Parents associated with the occupant.
		alive: Current state of an occupant, live or not.
		life: Number of remaining life points of the occupant.
		foundChildren: Children associated with the occupant found by the occupant during a emergency.
		exitGateStrategy: strategy that is used to leave the building during a emergency.
		adult: Inform if the occupant is an adult.
		alone: Inform if the occupant has occupants who follow him.
		speedEmergency: Movement speed during an emergency.
		parentAsos: Familiar that the child occupant has to follow.
	
	Methods:
		fireInMyFOV: Check if there is fire in the FOV of the occupant.
		makeEmergencyAction: Method that is invoked when initiating an emergency to make the decision of response.
		getExitGate: Obtain the optimal way to evacuate the building according to an evacuation strategy.
		getPosFireFOV: Obtain the positions in the occupant's field of vision where there is fire.
		step: Method invoked by the Model scheduler in each step.
	
	"""
	def __init__(self, unique_id, model, json):
		super().__init__(unique_id, model, json)

		self.familiar = False
		self.children = []
		self.parents = []
		self.child = False
		self.alive = True
		self.life = 3
		self.foundChildren = []
		strategies = ['safest', 'uncrowded', 'nearest']
		self.exitGateStrategy = json.get('strategy') or 'nearest'
		self.stateOne = self.state
		self.out = True
		self.alreadyCreated = False
		self.inbuilding = False
		self.initmove = True
		self.adult = True
		self.alone = True
		self.speedEmergency = 1.38 if not json.get('speedEmergency') else json.get('speedEmergency')
		self.parentAsos = False
		self.shape = "circle"
		self.exclude = []
		self.fovCal = True if not json.get('fov') else json.get('fov')
		self.thereis_exit = True
		self.movements = []
		self.way_saved = []
		self.aStar = False

	def getWay(self, pos1 = False, pos2 = False, other = False):
		pos1 = pos1
		pos2 = pos2
		if not pos1:
			pos1 = self.pos
		if not pos2:
			pos2 = self.pos_to_go
		from_file = True
		if from_file:
			for way in self.way_saved: 
				if pos1 == way[0] and pos2 == way[1]:
					print('way', self.movements)
					if way[2] == None:
						return [self.pos]
					return way[2]
			return [self.pos]
		else:
			print('no way', self.movements)
			return [self.pos]

	def evalCollision(self):
		return True

	def makeEmergencyAction(self, exclude = []):
		"""
		Method that is invoked when initiating an emergency to make the decision of response.
		If the occupant is a parent, he will look for his son. If he is a child, 
		he will wait for one of his parents. In any other case, a path is decided to leave the building.
		"""
		'''
		self.speed = self.speedEmergency
		self.N = 0
		self.markov = False
		self.timeActivity = 0
		if self.children and not self.child:
			child = random.choice(self.children)
			self.pos_to_go = child.pos
			self.movements = self.getWay()
			self.child = child
		elif not self.adult:
			if self.alone:
				self.pos_to_go = self.pos
				self.movements = [self.pos_to_go]
		else:
			self.movements = self.getExitGate(exclude)
			print(1)
			if self.movements[0] == self.pos and len(self.movements)== 1:
				print(2)
				self.thereis_exit = False
		'''
		import random
		self.markov = False
		self.timeActivity = 0
		doors = self.pos_door_poi
		if self.pos_to_go in doors:
			return
		for d in doors:
			print('door', d)
			pos_movements = self.getWay(self.pos, d)
			print('movements', pos_movements)
			if pos_movements != [self.pos] and pos_movements != None:
				self.movements = pos_movements
				self.N = 0
				return        		
		
		print(123123, self.N, self.movements, self.pos_to_go)
		N = self.N
		movements = self.movements[0:N-1]
		print('m', movements)
		self.pos_to_go = self.movements[0]
		print('m', self.pos_to_go)
		self.movements = movements[::-1]
		print('m', self.movements)
		self.N = 0
		print(98765, self.N, self.movements, self.pos_to_go)

	def getExitGate(self, exclude = []):
		'''
		Obtain the optimal way to evacuate the building according to an evacuation strategy.
			Return: List of positions (x, y)
		'''
		if True:
			if self.exitGateStrategy == 'uncrowded':
				self.pos_to_go = self.model.getNearestGate(self, exclude)
				self.model.uncrowdedStr.append(self)
			elif self.exitGateStrategy == 'safest':
				self.pos_to_go = self.model.getSafestGate(self, exclude)
			elif self.exitGateStrategy == 'nearest':
				self.pos_to_go = self.model.getNearestGate(self, exclude)
			else:
				self.pos_to_go = self.model.getNearestGate(self, exclude)
		else:
			self.pos_to_go = self.model.getNearestGate(self)
		pathReturn = self.getWay(other = self.exclude)
		return pathReturn

	def fireInMyFOV(self):
		"""
		Check if there is fire in the FOV of the occupant.
			Return: Boolean
		"""
		if not self.model.FireControl.fireMovements:
			return False
		if not self.movements:
			return False
		for firePos in self.model.FireControl.fireMovements:
			if firePos in self.movements[self.N:] and self.posInMyFOV(firePos):
				return True
		return False

	def getPosFireFOV(self):
		"""
		Obtain the positions in the occupant's field of vision where there is fire.
			Return: list of positions (x, y)
		"""
		others = []
		for pos in self.fov:
			if pos in self.model.FireControl.fireMovements:
				others.append(pos)
		return others

	def changeSchedule(self):
		if self.model.emergency:
			return False
		super().changeSchedule()

	def step(self):
		"""Method invoked by the Model scheduler in each step."""
		

		pos_poi = []
		pos_door_poi = []
		self.pos_door_poi = pos_door_poi
		for poi in self.model.pois:
			if poi.id == 'out':
				pos_door_poi.append(poi.pos)
			else:
				pos_poi.append(poi.pos)

		print(len(pos_poi), pos_poi)
		print(len(pos_door_poi), pos_door_poi)

		if self.aStar:
			import csv
			count = 0
			getAStar = True
			for x1 in range(0, 113):
				for y1 in range(0, 80):
					for x2 in range(0, 113):
						for y2 in range(0, 80):
							start = (x1, y1)
							final = (x2, y2)
							#if (start in pos_door_poi and final in pos_poi) or (start in pos_poi and final in pos_door_poi):
							print(start, final)
							way = super().getWay(start, final)
							row = [str(start), str(final), str(way)]
							with open('waysAStar.csv', 'a') as csvFile:
								writer = csv.writer(csvFile)
								writer.writerow(row)
							csvFile.close()
							count = count+1
							print(count)
			self.running = False

		if self.alive == True:
			if isinstance(self, EmergencyAvatar):
				return
			if self.model.emergency:
				print('emer', self.movements)
				if set(self.model.exits).issubset(self.exclude) or self.pos in self.model.exits:
					if self in self.model.occupEmerg:
						self.model.occupEmerg.remove(self)
						return
				self.markov = False
				self.timeActivity = 0
				if self.parentAsos:
					if not self.model.nearPos(self.parentAsos.pos, self.pos):
						self.pos_to_go = self.parentAsos.pos
						self.movements = self.getWay(other = self.exclude)
						self.N = 0
						if self.pos == self.movements[0]:
							self.parentAsos = False
							self.pos_to_go = self.pos
							self.movements = [self.pos]
							self.N = 0
				elif self.child:
					chi = self.model.getOccupantsPos(self.movements[self.N])
					if chi:
						chi = chi[0]
						if chi.pos not in self.model.exits:
							posChi = chi.pos
							chi.alone = False
							for parent in chi.parents:
								if chi in parent.children:
									parent.foundChildren.append(chi)
									parent.children.remove(chi)
							chi.parentAsos = self
							for parent in chi.parents:
								if parent.pos_to_go == posChi:
									parent.child = False
									parent.makeEmergencyAction()
						else:
							self.child = False
							if chi in self.children:
								self.children.remove(chi)
							self.makeEmergencyAction()
				if self.pos != self.pos_to_go:
					if self.fireInMyFOV():
						print('firefov')
						N = self.N
						movements = self.movements[0:N-1]
						print('m', movements)
						self.pos_to_go = self.movements[0]
						print('m', self.pos_to_go)
						self.movements = movements[::-1]
						print('m', self.movements)
						self.N = 0
						print(98765, self.N, self.movements, self.pos_to_go)

						'''
						self.exclude += self.getPosFireFOV()
						self.movements = self.getWay(other = self.exclude)
						self.N = 0
						if self.pos == self.movements[0]:
							if self.adult:
								if self.child:
									chi = self.model.getOccupantsPos(self.movements[self.N])
									if chi:
										chi = chi[0]
										if chi in self.children:
											self.children.remove(chi)
									self.child = False
								self.exclude.append(self.pos_to_go)
								self.makeEmergencyAction(self.exclude)
								if self.pos == self.movements[0]:
									self.pos_to_go = self.pos
									self.movements = [self.pos]
									self.N = 0
							else:
								self.parentAsos = False
								self.pos_to_go = self.pos
								self.movements = [self.pos]
								self.N = 0
						else:
							self.pos_to_go = self.movements[-1]
							'''
					if (self.movements == None) or (self.N >= len(self.movements))  or (len(self.movements)==1 and self.pos != self.pos_to_go):
						self.movements = [self.pos]
						self.pos_to_go = self.pos
						self.N = 0
						return
					super().step()
				else:
					if self.pos not in self.model.exits:
						if self.thereis_exit:
							return
						else:
							self.makeEmergencyAction()
					else:
						if self in self.model.occupEmerg:
							self.model.occupEmerg.remove(self)
			else:
				print(12, self.movements, self.N)
				if (self.movements == None) or (self.N >= len(self.movements)) or (len(self.movements)==1 and self.pos != self.pos_to_go):
					self.movements = [self.pos]
					self.pos_to_go = self.pos
					self.N = 0
					print(13, self.movements, self.N)
					return
				super().step()
		else:
			if self in self.model.occupEmerg:
				self.model.occupEmerg.remove(self)