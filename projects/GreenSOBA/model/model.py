from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from mesa.space import ContinuousSpace

from collections import defaultdict
import random
import os
import os.path

import configuration.settings
import configuration.defineOccupancy
import configuration.defineMap

from log.log import Log

from model.energy import Energy
from model.time import Time

from agents.occupant import Occupant
from agents.pc import PC
from agents.light import Light
from agents.hvac import HVAC


from space.door import Door
from space.room import Room
from space.window import Window
from space.wall import Wall
from space.thermalZone import ThermalZone
from time import time

class SOBAModel(Model):

	def __init__(self, width, height, modelWay = None, seed = int(time()), nothing = 1):
		super().__init__(seed)
		#Init configurations and defines
		configuration.settings.init()
		configuration.defineOccupancy.init()
		configuration.defineMap.init()

		#Way of working
		if modelWay is None:
			self.modelWay = configuration.settings.model
		else:
			self.modelWay = modelWay

		#Mesa
		self.schedule = BaseScheduler(self)
		self.grid = MultiGrid(width, height, False)
		self.running = True

		#Control of time and energy
		self.energy = Energy()
		self.clock = Time()

		#Log
		self.log = Log()
		self.roomsSchedule = []
		self.agentSatisfationByStep = []
		self.fangerSatisfationByStep = []
		self.agentsActivityByTime = []
		self.occupantsValues = False
		if self.modelWay != 0 and os.path.isfile('../log/tmp/occupants.txt'):
			self.occupantsValues = self.log.getOccupantsValues()

		#Vars of control
		self.complete = False
		self.num_occupants = 0
		self.day = self.clock.day
		self.NStep = 0
		self.timeToSampling = 'init' # Temperature ThermalLoads
		self.placeByStateByTypeAgent = {}
		self.lightsOn = []

		#Create the map
		self.createRooms()
		self.createThermalzones()
		self.setMap(width, height)
		self.createDoors()
		self.createWindows()
		self.createWalls()

		#Create agents
		self.setAgents()

	def consumeEnergy(self, appliance):
		if isinstance(appliance, PC):
			if appliance.state == 'on':
				self.energy.consumeEnergyAppliance('PC',appliance.consumeOn)
			elif appliance.state == 'standby':
				self.energy.consumeEnergyAppliance('PC',appliance.consumeStandby)
			else:
				self.energy.consumeEnergyAppliance('PC',0)

		elif isinstance(appliance, Light):
			if appliance.state == 'on':
				self.energy.consumeEnergyAppliance('Light',appliance.consume)
			else:
				self.energy.consumeEnergyAppliance('Light',0)

		elif isinstance(appliance, HVAC):
			if appliance.state == 'on':
				self.energy.consumeEnergyAppliance('HVAC',appliance.consumeOn)
			else:
				self.energy.consumeEnergyAppliance('HVAC',0)
		else:
			pass

	def isConected(self, pos):
		nextRoom = False
		for room in self.rooms:
			if room.pos == pos:
				nextRoom = room
		if nextRoom == False:
			return False
		for x in range(0, width):
			for y in range(0, height):
				self.pos_out_of_map.append(x, y)
		for room in self.rooms:
			self.pos_out_of_map.remove(room.pos)

	def createRooms(self):
		rooms = configuration.defineMap.rooms_json
		self.rooms = []
		#occupantsByTypeRoom = configuration.defineMap.NumberOccupancyByTypeRoom
		for room in rooms:
			newRoom  = 0
			name = room['name']
			typeRoom = room['type']
			if typeRoom != 'out':
				conectedTo = room.get('conectedTo')
				nameThermalZone = room.get('thermalZone')
				entrance = room.get('entrance')
				measures = room['measures']
				dx = measures['dx']
				dy = measures['dy']
				dh = measures['dh']
				jsonWindows = room.get('windows')
				newRoom = Room(name, typeRoom, conectedTo, nameThermalZone, dx, dy, dh, jsonWindows)
				newRoom.entrance = entrance
			else:
				newRoom = Room(name, typeRoom, None, False, 0, 0, 0, {})
				self.outBuilding = newRoom
			self.rooms.append(newRoom)
		for room1 in self.rooms:
			if room1.conectedTo is not None:
				for otherRooms in list(room1.conectedTo.values()):
					for room2 in self.rooms:
						if room2.name == otherRooms:
							room1.roomsConected.append(room2)
							room2.roomsConected.append(room1)
		for room in self.rooms:
			room.roomsConected = list(set(room.roomsConected))
		sameRoom = {}
		for room in self.rooms:
			if sameRoom.get(room.name.split(r".")[0]) is None:
				sameRoom[room.name.split(r".")[0]] = 1
			else:
				sameRoom[room.name.split(r".")[0]] = sameRoom[room.name.split(r".")[0]] + 1

	def createThermalzones(self):
		self.thermalZones = []
		namesThermalZonesCreated = []
		for room1 in self.rooms:
			posibleThermalZone = room1.nameThermalZone
			if posibleThermalZone not in namesThermalZonesCreated and posibleThermalZone != False and posibleThermalZone is not None:
				namesThermalZonesCreated.append(posibleThermalZone)
				rooms = []
				for room2 in self.rooms:
					if room2.nameThermalZone == posibleThermalZone:
						rooms.append(room2)
				TZ = ThermalZone(self, posibleThermalZone, rooms)
				for room3 in TZ.rooms:
					room3.thermalZone = TZ
				self.thermalZones.append(TZ)

		if self.modelWay == 2:
			hoursRoomsOnOffByDay = {}
			hoursRoomsOnStrings = self.log.getScheduleRooms()
			hoursRoomsOn = []
			for row in hoursRoomsOnStrings:
				hoursRoomsOn.append([row[0], float(row[1]), float(row[2])])
			for room in self.rooms:
				count = 0
				if room.typeRoom != 'out' and room.typeRoom != 'restroom':
					hoursOneRoomOn = []
					for row in hoursRoomsOn:
						if row[0] == room.name:
							hoursOneRoomOn.append([row[1], row[2]])
					hoursOneRoomOnByDay = []
					for i in range(0, 5):
						hoursOneDay = []
						for hour in hoursOneRoomOn:
							if int(hour[0]) == i:
								hoursOneDay.append(hour[1])
						hoursOneRoomOnByDay.append(hoursOneDay)
					hoursOnOffOneRoomByDay = []
					for i in range(0 ,5):
						hoursOnOffOneRoomOneDay = []
						hourOn = hoursOneRoomOnByDay[i]
						if len(hourOn) > 0:
							auxHour = hourOn[0]
							hourOnAux = hourOn[0]
							for hour in hourOn:
								if (auxHour != hour):
									if(hour > (auxHour + configuration.settings.setOffWorthIt)):
										hourOff = auxHour-0.01
										pairOnOff = [int(hourOnAux*100)/100, int(hourOff*100)/100]
										hoursOnOffOneRoomOneDay.append(pairOnOff)
										auxHour = hour + 0.01
										hourOnAux = hour
									else:
										auxHour = hour + 0.01
								else:
									auxHour = auxHour + 0.01
							pairOnOffObligatory = [hourOnAux, hourOn.pop()]
							hoursOnOffOneRoomOneDay.append(pairOnOffObligatory)
							hoursOnOffOneRoomByDay.append(hoursOnOffOneRoomOneDay)
						else:
							hoursOnOffOneRoomByDay.append(False)
					hoursRoomsOnOffByDay[room.name] = hoursOnOffOneRoomByDay
					count = count + 1

			for tz in self.thermalZones:
				schedule = []
				for i in range(0, 5):
					scheduleByDay = []
					for room in tz.rooms:
						hoursByDay = hoursRoomsOnOffByDay.get(room.name)
						if hoursByDay is not None and hoursByDay != False:
							hoursOneDay = hoursByDay[i]
							if hoursOneDay is not None and hoursOneDay != False:
								for hours in hoursOneDay:
									hourOn = hours[0]
									hourOff = hours[1]
									for pairHours in scheduleByDay:
										if hourOn > pairHours[0] and pairHours[1] > hourOn:
											scheduleByDay.remove([pairHours[0], pairHours[1]])
											hourOn = pairHours[0]
											if(hourOff < pairHours[1]):
												hourOff = pairHours[1]
											else:
												pass
										elif hourOff > pairHours[0] and pairHours[1] > hourOff:
											scheduleByDay.remove([pairHours[0], pairHours[1]])
											hourOff = pairHours[1]
											if(hourOn > pairHours[0]):
												hourOn = pairHours[0]
											else:
												pass
										elif hourOff > pairHours[1] and pairHours[0] > hourOn:
											scheduleByDay.remove([pairHours[0], pairHours[1]])
									scheduleByDay.append([hourOn, hourOff])
					if len(scheduleByDay) == 0:
						scheduleByDay.append([False])
					schedule.append(scheduleByDay)
				scheduleJoined = []
				for day in schedule:
					if day != False:
						scheduleJoined.append(sorted(day))

				for day in scheduleJoined:
					i = 0
					if day != False:
						while (len(day)>(i+1)):
							if (day[i][1] + configuration.settings.setOffWorthIt) > day[i+1][0]:
								day[i][1] = day[i+1][1]
								day.pop(i+1)
							else:
								i = i+1
				tz.schedule = scheduleJoined

	def setMap(self, width, height):
		rooms_noPos = self.rooms
		rooms_using = []
		rooms_used = []
		for room in self.rooms:
			if room.entrance is not None:
				room.pos = (int(1), 2)
				rooms_using.append(room)
				rooms_used.append(room)
				rooms_noPos.remove(room)
				break
		while len(rooms_noPos) > 0:
			for roomC in rooms_using:
				xc, yc = roomC.pos
				rooms_conected = roomC.conectedTo
				rooms_using.remove(roomC)
				if rooms_conected is not None:
					orientations = list(rooms_conected.keys())
					for orientation in orientations:
						if orientation == 'R':
							for room in rooms_noPos:
								if room.name == rooms_conected['R']:
									room.pos = (int(xc + 1), yc)
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'U':
							for room in rooms_noPos:
								if room.name == rooms_conected['U']:
									room.pos = (xc, int(yc + 1))
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'D':
							for room in rooms_noPos:
								if room.name == rooms_conected['D']:
									room.pos = (xc, int(yc - 1))
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'L':
							for room in rooms_noPos:
								if room.name == rooms_conected['L']:
									room.pos = (int(xc -1), yc)
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
				else:
					pass
		self.rooms = rooms_used

	def createDoors(self):
		self.doors = []
		for roomC in self.rooms:
			roomsConected = roomC.roomsConected
			for room in roomsConected:
				door_created = False
				same_corridor = False
				if room.name != roomC.name:
					for door in self.doors:
						if (door.room1.name == roomC.name and door.room2.name == room.name) or (door.room2.name == roomC.name and door.room1.name == room.name):
							door_created = True
						if room.name.split(r".")[0] == roomC.name.split(r".")[0]:
							same_corridor = True
					if door_created == False and same_corridor == False:
						d = Door(roomC, room)
						self.doors.append(d)
						room.doors.append(d)
						roomC.doors.append(d)

	def createWindows(self):
		for room in self.rooms:
			windows = []
			json = room.jsonWindows
			if json is None:
				pass
			else:
				for k in json:
					window = Window(k, json[k]['l1'], json[k]['l2'])
					windows.append(window)
			room.windows = windows

	def createWalls(self):
		for room in self.rooms:
			if room.typeRoom != 'out':
				walls = []
				innerWalls = []
				adjRooms = []
				xr, yr = room.pos
				roomA = self.getRoom((xr, yr+1))
				if roomA != False:
					if roomA.typeRoom != 'out':
						if roomA.name.split(r".")[0] == room.name.split(r".")[0]:
							pass
						else:
							wall = Wall(room.dx, room.dh, room, roomA)
							innerWalls.append(wall)
							adjRooms.append(roomA)
					else:
						wall = Wall(room.dx, room.dh, orientation = 'N')
						walls.append(wall)
				else:
					wall = Wall(room.dx, room.dh, orientation = 'N')
					walls.append(wall)
				roomB = self.getRoom((xr, yr-1))
				if roomB != False:
					if roomB.typeRoom != 'out':
						if roomB.name.split(r".")[0] == room.name.split(r".")[0]:
							pass
						else:
							wall = Wall(room.dx, room.dh, room, roomB)
							innerWalls.append(wall)
							adjRooms.append(roomB)
					else:
						wall = Wall(room.dx, room.dh, orientation = 'S')
						walls.append(wall)
				else:
					wall = Wall(room.dx, room.dh, orientation = 'S')
					walls.append(wall)
				roomC = self.getRoom((xr+1, yr))
				if roomC != False:
					if roomC.typeRoom != 'out':
						if roomC.name.split(r".")[0] == room.name.split(r".")[0]:
							pass
						else:
							wall = Wall(room.dy, room.dh, room, roomC)
							innerWalls.append(wall)
							adjRooms.append(roomC)
					else:
						wall = Wall(room.dy, room.dh, orientation = 'E')
						walls.append(wall)
				else:
					wall = Wall(room.dy, room.dh, orientation = 'E')
					walls.append(wall)
				roomD = self.getRoom((xr-1, yr))
				if roomD != False:
					if roomD.typeRoom != 'out':
						if roomD.name.split(r".")[0] == room.name.split(r".")[0]:
							pass
						else:
							wall = Wall(room.dy, room.dh, room, roomD)
							innerWalls.append(wall)
							adjRooms.append(roomD)
					else:
						wall = Wall(room.dy, room.dh, orientation = 'W')
						walls.append(wall)
				else:
					wall = Wall(room.dy, room.dh, orientation = 'W')
					walls.append(wall)
				room.walls = walls
				room.innerWalls = innerWalls
				room.roomsAdj = adjRooms

	def setAgents(self):
		# Identifications
		id_offset = 1000

		# Height and Width
		height = self.grid.height
		width = self.grid.width

		# CREATE AGENTS

		#Create Lightlights
		self.lights = []
		id_light = 0
		for room in self.rooms:
			if room.typeRoom != 'out' and room.light == False:
				light = Light(id_light, self, room)
				self.lights.append(light)
				id_light = id_light + 1
				room.light = light
				for room2 in self.rooms:
					if room.name.split(r".")[0] == room2.name.split(r".")[0]:
						room2.light = light
				
		id_hvac = id_light + id_offset
		#Create HVAC
		self.HVACs = []
		for thermalZone in self.thermalZones:
			restroom = False
			for room in thermalZone.rooms:
				if room.typeRoom == 'restroom':
					restroom = True
			if restroom == False:
				hvac = HVAC(id_hvac, self, thermalZone)
				thermalZone.hvac = hvac
				self.HVACs.append(hvac)
				id_hvac = id_hvac + 1
			else:
				thermalZone.hvac = False

		#Create PC
		'''
		self.workplaces = []
		id_aux = 0
		for room in self.rooms:
			#for i in range(0, room.PCs):
			pc = PC(id_pc + id_aux, self, room)
			room.PCs.append(pc)
			self.workplaces.append(pc)
			id_aux = id_aux + 1
		'''
		id_occupant = id_hvac + id_offset
		id_pc = id_occupant + id_offset
		self.workplaces = []
		self.agents = []
		# Create occupants
		if self.modelWay == 0:
			countPC = 0
			print('Número de ocupantes: ', configuration.defineOccupancy.occupancy_json[0]['N'])
			for n_type_occupants in configuration.defineOccupancy.occupancy_json:
				self.placeByStateByTypeAgent[n_type_occupants['type']] = n_type_occupants['states']
				n_agents_perfect = int((n_type_occupants['N'] * n_type_occupants['environment'][0]) / 100)
				for i in range(0, n_agents_perfect):
					rooms_with_already_pc = []
					a = Occupant(id_occupant, self, n_type_occupants, 1)
					self.agents.append(a)
					id_occupant = 1 + id_occupant
					for state_use_PCs in n_type_occupants['PCs']:
						roomPC = False
						name_room_with_pc = a.positionByState[state_use_PCs]
						for room in self.rooms:
							if room.name.split(r".")[0]  == name_room_with_pc:
								roomPC = room
						if roomPC != False and roomPC.typeRoom != 'out':
							if roomPC not in rooms_with_already_pc:
								pc = PC(id_pc, self, roomPC)
								id_pc = id_pc + 1
								pc.owner = a
								self.workplaces.append(pc)
								a.PCs[state_use_PCs] = pc
								pc.states_when_is_used.append(state_use_PCs)
								roomPC.PCs.append(pc)
							else:
								for pcaux in roomPC.PCs:
									if pcaux.owner == a:
										a.PCs[state_use_PCs] = pcaux
										pc.states_when_is_used.append(state_use_PCs)
					self.schedule.add(a)
					self.grid.place_agent(a, self.outBuilding.pos)
					self.pushAgentRoom(a, self.outBuilding.pos)
					self.num_occupants = self.num_occupants + 1
				n_agents_good = int((n_type_occupants['N'] * n_type_occupants['environment'][1]) / 100)
				for i in range(0, n_agents_good):
					rooms_with_already_pc = []
					a = Occupant(id_occupant, self, n_type_occupants, 2)
					self.agents.append(a)
					id_occupant = 1 + id_occupant
					for state_use_PCs in n_type_occupants['PCs']:
						roomPC = False
						name_room_with_pc = a.positionByState[state_use_PCs]
						for room in self.rooms:
							if room.name.split(r".")[0] == name_room_with_pc:
								roomPC = room
						if roomPC != False and roomPC.typeRoom != 'out':
							if roomPC not in rooms_with_already_pc:
								pc = PC(id_pc, self, roomPC)
								id_pc = id_pc + 1
								pc.owner = a
								self.workplaces.append(pc)
								a.PCs[state_use_PCs] = pc
								pc.states_when_is_used.append(state_use_PCs)
								roomPC.PCs.append(pc)
							else:
								for pcaux in roomPC.PCs:
									if pcaux.owner == a:
										a.PCs[state_use_PCs] = pcaux
										pc.states_when_is_used.append(state_use_PCs)
					self.schedule.add(a)
					self.grid.place_agent(a, self.outBuilding.pos)
					self.pushAgentRoom(a, self.outBuilding.pos)
					self.num_occupants = self.num_occupants + 1
				n_agents_bad = int(n_type_occupants['N'] * n_type_occupants['environment'][2] / 100)
				allAgents = n_agents_perfect + n_agents_good + n_agents_bad
				if allAgents < n_type_occupants['N']:
					n_agents_bad = n_type_occupants['N'] - (n_agents_perfect + n_agents_good)
				for i in range(0, n_agents_bad):
					rooms_with_already_pc = []
					a = Occupant(id_occupant, self, n_type_occupants, 3)
					self.agents.append(a)
					id_occupant = 1 + id_occupant
					for state_use_PCs in n_type_occupants['PCs']:
						roomPC = False
						name_room_with_pc = a.positionByState[state_use_PCs]
						for room in self.rooms:
							if room.name.split(r".")[0] == name_room_with_pc:
								roomPC = room
						if roomPC != False and roomPC.typeRoom != 'out':
							if roomPC not in rooms_with_already_pc:
								pc = PC(id_pc, self, roomPC)
								id_pc = id_pc + 1
								pc.owner = a
								self.workplaces.append(pc)
								a.PCs[state_use_PCs] = pc
								pc.states_when_is_used.append(state_use_PCs)
								roomPC.PCs.append(pc)
							else:
								for pcaux in roomPC.PCs:
									if pcaux.owner == a:
										a.PCs[state_use_PCs] = pcaux
										pc.states_when_is_used.append(state_use_PCs)
					self.schedule.add(a)
					self.grid.place_agent(a, self.outBuilding.pos)
					self.pushAgentRoom(a, self.outBuilding.pos)
					self.num_occupants = self.num_occupants + 1
		else:
			for n_type_occupants in configuration.defineOccupancy.occupancy_json:
				self.placeByStateByTypeAgent[n_type_occupants['type']] = n_type_occupants['states']
				n_agents = n_type_occupants['N']
				for i in range(0, n_agents):
					rooms_with_already_pc = []
					a = Occupant(id_occupant, self, n_type_occupants, '')
					self.agents.append(a)
					id_occupant = 1 + id_occupant
					for state_use_PCs in n_type_occupants['PCs']:
						roomPC = False
						name_room_with_pc = a.positionByState[state_use_PCs]
						for room in self.rooms:
							if room.name.split(r".")[0] == name_room_with_pc:
								roomPC = room
						if roomPC != False and roomPC.typeRoom != 'out':
							if roomPC not in rooms_with_already_pc:
								pc = PC(id_pc, self, roomPC)
								id_pc = id_pc + 1
								pc.owner = a
								self.workplaces.append(pc)
								a.PCs[state_use_PCs] = pc
								pc.states_when_is_used.append(state_use_PCs)
								roomPC.PCs.append(pc)
							else:
								for pcaux in roomPC.PCs:
									if pcaux.owner == a:
										a.PCs[state_use_PCs] = pcaux
										pc.states_when_is_used.append(state_use_PCs)
					self.schedule.add(a)
					self.grid.place_agent(a, self.outBuilding.pos)
					self.pushAgentRoom(a, self.outBuilding.pos)
					self.num_occupants = self.num_occupants + 1

		#Add to schedule
		for pc in self.workplaces:
			self.schedule.add(pc)
		for light in self.lights:
			self.schedule.add(light)
		for hvac in self.HVACs:
			self.schedule.add(hvac)

		self.schedule.add(self.clock)

	def getPosState(self, name, typeA):
		placeByStateByTypeAgent = self.placeByStateByTypeAgent
		n = 0
		for state in self.placeByStateByTypeAgent[typeA]:
			if state.get('name') == name:
				pos1 = state.get('position')
				if isinstance(pos1, dict):
					for k,v in pos1.items():
						if v > 0:
							placeByStateByTypeAgent[typeA][n]['position'][k] = v - 1
							self.placeByStateByTypeAgent = placeByStateByTypeAgent
							return k
					return list(pos1.keys())[-1]
				else:
					return pos1
			n = n +1

	def thereIsClosedDoor(self, beforePos, nextPos):
		oldRoom = False
		newRoom = False
		for room in rooms:
			if room.pos == beforePos:
				oldRoom = room
			if room.pos == nextPos:
				newRoom = room
		for door in self.doors:
			if (door.room1.name == oldRoom.name and door.room2.name == newRoom.name) or (door.room2.name == oldRoom.name and door.room1.name == newRoom.name):
				if door.state == False:
					return True
		return False

	def thereIsPC(self, pos):
		x,y = pos
		for pc in self.workplaces:
			if pc.x == x and pc.y == y:
				return True
		return False

	def thereIsOccupant(self,pos):
		possible_occupant = self.grid.get_cell_list_contents([pos])
		if (len(possible_occupant) > 0):
			for occupant in possible_occupant:
				if isinstance(occupant,Occupant):
					return True
		return False

	def ThereIsOtherOccupantInRoom(self, room, agent):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant) and occupant != agent:
					return True
		return False

	def ThereIsSomeOccupantInRoom(self, room):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant):
					return True
		return False

	def thereIsOccupantInRoom(self, room, agent):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant) and occupant == agent:
					return True
		return False

	def getRoom(self, pos):
		for room in self.rooms:
			if room.pos == pos:
				return room
		return False

	def pushAgentRoom(self, agent, pos):
		room = self.getRoom(pos)
		room.agentsInRoom.append(agent)

	def popAgentRoom(self, agent, pos):
		room = self.getRoom(pos)
		room.agentsInRoom.remove(agent)

	def getLightWithRoom(self, room):
		for light in self.lights:
			if light.room == room:
				return light
		return False

	def crossDoor(self, agent, room1, room2):
		numb = random.randint(0, 10)
		for door in self.doors:
			if ((door.room1 == room1 and door.room2 == room2) or (door.room1 == room2 and door.room2 == room1)):
				if  agent.leftClosedDoor >= numb:
					door.state = False
				else:
					door.state = True

	def getMatrix(self,agent):
		new_matrix = configuration.defineOccupancy.returnMatrix(agent, self.clock.clock)
		agent.markov_matrix = new_matrix
	
	def getTimeInState(self, agent):
		matrix_time_in_state = configuration.defineOccupancy.getTimeInState(agent, self.clock.clock)
		return matrix_time_in_state

	def end_work(self, agent, pc):
		change = configuration.defineOccupancy.environmentBehaviour(agent, self.clock.clock, 'pc')[int(agent.environment)-1]
		print(change)
		if change == 'off':
			pc.turn_off()
		elif change == 'standby':
			pc.turn_standby()
		else:
			pass

	def switchLights(self, agent, currentRoom, nextRoom):
		change = configuration.defineOccupancy.environmentBehaviour(agent, self.clock.clock, 'light')[int(agent.environment)-1]
		light_switch_on = nextRoom.light
		if light_switch_on != False and light_switch_on.state == 'off':
				light_switch_on.switch_on()
		if change == 'off':
			light_switch_off = currentRoom.light
			if self.ThereIsOtherOccupantInRoom(currentRoom, agent) == False:
				if light_switch_off != False:
					light_switch_off.switch_off()
		else:
			pass

	def step(self):
		if (self.running == False):
			os.system("kill -9 %d"%(os.getppid()))
			os.killpg(os.getpgid(os.getppid()), signal.SIGTERM)

		if (self.clock.day == 5):
			self.energy.finalDay(self.NStep)
			self.energy.finalWeek()
			self.running = False
			self.log.collectEnergyValues(self.modelWay, self.energy.energyByDayTotal, self.energy.energyByDayHVAC, self.energy.energyByDayLPC, configuration.settings.time_by_step, self.energy.energyByStepTotal, self.energy.energyByStepHVACsTotal, self.energy.energyByStepLPCTotal)
			self.log.collectComfortValues(self.modelWay, configuration.settings.time_by_step, self.agentSatisfationByStep, self.fangerSatisfationByStep)
			self.log.collectScheduleValues(self.modelWay, configuration.settings.time_by_step, self.agentsActivityByTime)
			if self.modelWay == 0:
				self.log.saveScheduleRooms(self.roomsSchedule)
				dictAgents = {}
				for agent in self.agents:
					agent.scheduleLog.append([self.day, agent.arrive, agent.leave])
					scheduleByDay = {}
					for e in agent.scheduleLog:
						d = 'day'+str(e[0])
						scheduleByDay[d] = {'arrive':e[1], 'leave': e[2]}
					posByState = {}
					for k,v in agent.positionByState.items():
						posByState[k] = v
					dictAgents[str(agent.unique_id)] = {'TComfort': agent.TComfort, 'posByState': posByState, 'schedule': scheduleByDay}
				self.log.saveOccupantsValues(dictAgents)
			return

		
		if self.modelWay == 0 or self.modelWay == 1:
			for hvac in self.HVACs:
				if ((self.clock.clock > (configuration.defineMap.ScheduleByTypeRoom.get(hvac.thermalZone.rooms[0].typeRoom)[0])) and (configuration.defineMap.ScheduleByTypeRoom.get(hvac.thermalZone.rooms[0].typeRoom)[1]> self.clock.clock)):
					hvac.working = True
				else:
					hvac.working = False
		elif self.modelWay == 2:
			for hvac in self.HVACs:
				for hours in hvac.thermalZone.schedule[self.clock.day]:
					if hours != [False]:
						if ((self.clock.getCorrectHour(self.clock.clock+configuration.settings.timeSetOnHVACBeforeGetT))>hours[0]) and ((self.clock.getDownCorrectHour(hours[1]-configuration.settings.timeSetOffHVACBeforeloseT)) > self.clock.clock):
							hvac.working = True
						elif ((hvac.thermalZone.rooms[0].typeRoom == 'class') and ((self.clock.getCorrectHour(self.clock.clock+configuration.settings.timeSetOnHVACBeforeGetTClass))>hours[0]) and ((self.clock.getDownCorrectHour(hours[1]-configuration.settings.timeSetOffHVACBeforeloseT)) > self.clock.clock)):
							hvac.working = True
						else:
							usr = False
							if self.clock.getDownCorrectHour(hours[1]) > self.clock.clock:
								for room in hvac.thermalZone.rooms:
									if self.ThereIsSomeOccupantInRoom(room) == True:
										usr = True
							if usr == True:
								hvac.working = True
							else:
								hvac.working = False
					else:
						hvac.working = False

		#Temperature in TZ
		if(self.timeToSampling == 'init'):
			for tz in self.thermalZones:
				tz.getQ(self, configuration.settings.timeToSampling)
			self.timeToSampling = configuration.settings.timeToSampling*(1/configuration.settings.time_by_step)
		elif(self.timeToSampling > 1):
			self.timeToSampling = self.timeToSampling - 1
		else:
			for tz in self.thermalZones:
				tz.step()
				tz.getQ(self, configuration.settings.timeToSampling)
			self.timeToSampling = configuration.settings.timeToSampling*(1/configuration.settings.time_by_step)

		self.schedule.step()
		
		#Rooms occupancy
		time = self.clock.clock
		day = self.clock.day
		for room in self.rooms:
			if len(room.agentsInRoom) > 0 and room.typeRoom != 'out' and room.typeRoom != 'restRoom':
				self.roomsSchedule.append([room.name, day, time])

		#Satisfation collection
		time = configuration.settings.time_by_step*self.NStep
		sumat = 0
		number = 0
		for agent in self.agents:
			if self.getRoom(agent.pos).typeRoom != 'out' and self.getRoom(agent.pos).typeRoom != 'restroom' and self.getRoom(agent.pos).typeRoom != 'hall' and self.getRoom(agent.pos).typeRoom != 'corridor':
				sumat = sumat + agent.comfort
				number = number + 1
		if number > 0:
			self.agentSatisfationByStep.append(sumat/number)
		else:
			self.agentSatisfationByStep.append(0)

		sumat = 0
		number = 0
		for hvac in self.HVACs:
			varaux = False
			for room in hvac.thermalZone.rooms:
				if self.ThereIsSomeOccupantInRoom(room) and room.typeRoom != 'out' and room.typeRoom != 'restroom' and room.typeRoom != 'corridor' and room.typeRoom != 'hall':
					varaux = True
			if varaux == True:
				sumat = sumat + hvac.fangerValue
				number = number + 1
		if number > 0:
			self.fangerSatisfationByStep.append(sumat/number)
		else:
			self.fangerSatisfationByStep.append(0)

		#Ocupancy activity collection
		time = configuration.settings.time_by_step*self.NStep
		sumat = 0
		number = 0
		for agent in self.agents:
			if (agent.state == 'working in my office') or (agent.state == 'in a meeting') or (agent.state == 'working in my laboratory') or (agent.state == 'giving class'):
				sumat = sumat + 1
		self.agentsActivityByTime.append(sumat)



		if len(self.lightsOn) > 0 and (self.clock.clock > configuration.settings.offLights):
			for light in self.lightsOn:
				light.switch_off()

		self.energy.finalStep()
		if (self.clock.day > self.day):
			self.energy.finalDay(self.NStep)
			if self.modelWay == 0:
				for agent in self.agents:
					timeA = self.clock.getDownCorrectHour(agent.arrive - 0.10)
					timeB = self.clock.getDownCorrectHour(agent.leave - 0.10)
					agent.scheduleLog.append([self.day, timeA, timeB])
					agent.arrive = False
					agent.leave = False
			if self.occupantsValues != False:
				for agent in self.agents:
					day = 'day' + str(self.day + 1)
					agent.behaviour['arriveTime'] = self.occupantsValues[str(agent.unique_id)]['schedule'][day]['arrive']
					agent.behaviour['leaveWorkTime'] = self.occupantsValues[str(agent.unique_id)]['schedule'][day]['leave']
			self.day = self.day + 1
		self.NStep = self.NStep + 1