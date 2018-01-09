from mesa import Agent, Model
from transitions import Machine
from transitions import State
import math
import configuration.settings

class ThermalZone():

	def __init__(self, model, name, rooms):
		self.rooms = rooms
		self.QHVAC = 0
		self.name = name
		self.model = model
		self.hvac = False

		#Thermal Vars
		self.season = configuration.settings.season
		self.temperature = self.getTemperatureInit()
		self.Qtotal = 0
		self.schedule = []

		#Thermal control
		self.QWalls = 0
		self.QRoofs = 0
		self.QWindows = 0
		self.QVentilation = 0
		self.QInfiltration = 0
		self.QInnerWalls = 0
		self.QOcuppancy = 0
		self.QLights = 0
		self.QEngines = 0
		self.QEquipment = 0


	def getTemperatureInit(self):
		if self.season == 'summer':
			return (configuration.settings.temperatureSummerOut[0] + configuration.settings.varTempertarueInInitialSummer)
		else:
			return (configuration.settings.temperatureWinterOut[0] + configuration.settings.varTempertarueInInitialSummer)

	#Auxiliar methods
	def getTo(self, model):
		hour = int(model.clock.hour)
		if self.season == 'summer':
			To = configuration.settings.temperatureSummerOut[hour]
		else:
			To = configuration.settings.temperatureWinterOut[hour]
		return To

	def getCLTDWall(self, model, orientation):
		hour = int(model.clock.hour)
		CLTD_before_hour = configuration.settings.CLTDWall[orientation]
		CLTD = CLTD_before_hour[hour]
		return CLTD

	def getCLTDRoof(self, model):
		hour = int(model.clock.hour)
		CLTD = configuration.settings.CLTDRoof[hour]
		return CLTD

	def getCLTDWindow(self, model):
		hour = int(model.clock.hour)
		CLTD = configuration.settings.CLTDWindow[hour]
		return CLTD

	def getCLFWindow(self, model, orientation):
		hour = int(model.clock.hour)
		CLF_before_hour = configuration.settings.CLFWindow[orientation]
		CLF = CLF_before_hour[hour]
		return CLF

	def getMaxSHGFWindow(self, orientation):
		CLF = configuration.settings.MaxSHGFWindow[orientation]
		return CLF

	#Thermal methods
	def walls(self, U, Ti, To, model):
		QwAux = 0
		for room in self.rooms:
			for wall in room.walls:
				A = wall.l1*wall.l2
				Q1 = U*A*(Ti-To)
				Q2 = 0
				if self.season == 'summer':
					Q1 = Q1*(-1)
					Q2 = U*A*self.getCLTDWall(model, wall.orientation)
				QwAux = QwAux + Q1 + Q2
		self.QWalls = QwAux * 0.8

	def roofs(self, U, Ti, To, model):
		QwAux = 0 
		for room in self.rooms:
			l1 = room.dx
			l2 = room.dy
			A = l1 * l2
			Q2 = 0
			Q1 = U*A*(To - Ti)
			if self.season == 'summer':
						Q1 = Q1*(-1)
						Q2 = U*A*self.getCLTDRoof(model)
			QwAux = QwAux + Q1 + Q2
		self.QRoofs = QwAux

	def windows(self, U, Ti, To, SC, model):
		QwAux = 0
		for room in self.rooms:
			for window in room.windows:
				A = window.l1*window.l2
				Q1 = U*A*(Ti-To)
				Q2 = 0
				if self.season == 'summer':
					Q1 = Q1 * (-1)
					Q2 = U*A*self.getCLTDWindow(model)
				Q3 = A * self.getMaxSHGFWindow(window.orientation) * SC * self.getCLFWindow(model, window.orientation)
				QwAux = QwAux + Q1 + Q2 + Q3
		self.QWindows = QwAux

	def innerwalls(self, U, Ti):
		QwAux = 0
		for room in self.rooms:
			for otherRoom in room.roomsAdj:
				if(otherRoom not in self.rooms):
					for wall in room.innerWalls:
						if((wall.room1 == room and wall.room2 == otherRoom) or (wall.room2 == room and wall.room1 == otherRoom)):
							A = wall.l1*wall.l2
							if otherRoom.typeRoom == 'restroom':
								QwAux = QwAux + U*A*(configuration.settings.restRoomTemperature-Ti)
							else:
								QwAux = QwAux + U*A*(otherRoom.thermalZone.temperature-Ti)
		#Falta suelo
		self.QInnerWalls = QwAux * 1.2

	def innerwallsMaximun(self, U, Ti, T2):
		QwAux = 0
		for room in self.rooms:
			for otherRoom in room.roomsAdj:
				if(otherRoom not in self.rooms):
					for wall in room.innerWalls:
						if((wall.room1 == room and wall.room2 == otherRoom) or (wall.room2 == room and wall.room1 == otherRoom)):
							A = wall.l1*wall.l2
							if otherRoom.typeRoom == 'restroom':
								QwAux = QwAux + U*A*(configuration.settings.restRoomTemperature-Ti)
							else:
								QwAux = QwAux + U*A*(T2-Ti)
		self.QInnerWalls = QwAux*0.5*1.25

	def ventilation(self, ACH, CFMByOccupant, airDensity, Cp, Cpw, Ti, To, h1, h2):
		QwAux = 0
		#NUsers = 0
		VolAir = 0
		for room in self.rooms:
			VolAir = VolAir + (room.dx * room.dy * room.dh)
			#NUsers = NUsers + room.waitedUsers
		#VolAirFil = NUsers * 12.5 /1000*3600# 12.5dm³/worker*seg
		Q1_julios_seg = VolAir * airDensity * Cp *(To-Ti) * configuration.settings.ACH
		#Q2 = VolAirFil * airDensity * Cpw * (h1 - h2)
		Q1 = Q1_julios_seg/3600*0.8
		QwAux = Q1 #+ Q2
		self.QVentilation = QwAux

	def infiltration(self, airDensity, Cp, Ti):
		QwAux = 0
		for room in self.rooms:
			if room.typeRoom != 'out' and room.typeRoom != 'restroom':
				for door in room.doors:
					if door.state == True:
						roomAux = False
						if door.room1 not in self.rooms:
							roomAux = door.room1
						elif door.room2 not in self.rooms:
							roomAux = door.room2
						if roomAux != False and roomAux.typeRoom != 'out' and roomAux.typeRoom != 'restroom':
							t = abs(Ti - roomAux.thermalZone.temperature)
							velocity = 20*((math.sqrt(door.l1*3.28084)*math.sqrt(t*(9/5)+32))/((math.sqrt(7)*math.sqrt(60))))#fpm
							CFM = velocity * door.l1*3.28084*door.l2*3.28084/2
							Q1 = 1.08*CFM*(t)
							#Q2 = 4840*CFM*(h1-h2)
							QwAux = Q1 #+ Q2
							#QwAux = QwAux + (door.l1*door.l2*door.w)*airDensity*Cp*(Ti-roomAux.temperature)
						if self.season== 'summer':
							QwAux = (-1) * QwAux
		self.QInfiltration = QwAux

	def ocuppancyMaximun(self, SHG, CLF, LHG):
		QwAux = 0
		NUsers = 0
		roomsUsed = []
		for room in self.rooms:
			if room.name.split(r".")[0] in roomsUsed:
				pass
			else:
				roomsUsed.append(room.name.split(r".")[0])
				if room.typeRoom == 'class':
					NUsers = NUsers + configuration.settings.peopleClass
				elif room.typeRoom == 'office':
					NUsers = NUsers + configuration.settings.peopleOffice
				else:
					NUsers = NUsers + configuration.settings.peopleLab
		Q1 = NUsers * SHG * CLF
		Q2 = NUsers * LHG
		QwAux = Q1 + Q2
		self.QOcuppancy = QwAux

	def ocuppancy(self, SHG, CLF, LHG):
		QwAux = 0
		NUsers = 0
		for room in self.rooms:
			NUsers = NUsers + len(room.agentsInRoom)
		Q1 = NUsers * SHG * CLF
		Q2 = NUsers * LHG
		QwAux = Q1 + Q2
		self.QOcuppancy = QwAux

	def lights(self, EffLights):
		QwAux = 0
		roomsUsed = []
		for room in self.rooms:
			if room.name.split(r".")[0] in roomsUsed:
				pass
			else:
				roomsUsed.append(room.name.split(r".")[0])
				if room.light.state == 'on':
					QwAux = QwAux + (room.light.consume * (1-EffLights))
		self.QLights = QwAux

	def lightsMaximun(self, EffLights):
		QwAux = 0
		roomsUsed = []
		for room in self.rooms:
			if room.name.split(r".")[0] in roomsUsed:
				pass
			else:
				roomsUsed.append(room.name.split(r".")[0])
				QwAux = QwAux + (configuration.settings.consume_light_byroom_medium * (1-EffLights))
		self.QLights = QwAux

	def engines(self, EffHVAC):
		QwAux = 0
		if self.hvac != False and self.hvac.state == 'on':
			QwAux = 2545 * configuration.settings.powerHVAC * EffHVAC
		self.QEngines = QwAux*0.15

	def enginesMaximun(self, EffHVAC):
		QwAux = 2545 * configuration.settings.powerHVAC * EffHVAC
		self.QEngines = QwAux*0.15

	def equipment(self, EffEquipment):
		QwAux = 0
		for room in self.rooms:
			for pc in room.PCs:
				if pc.state == 'on':
					QwAux = QwAux + pc.consumeOn * (1-EffEquipment)
				elif pc.state == 'standby':
					QwAux = QwAux + pc.consumeStandby * (1-EffEquipment)
		self.QEquipment = QwAux

	def equipmentMaximun(self, EffEquipment):
		QwAux = 0
		roomsUsed = []
		for room in self.rooms:
			if room.name.split(r".")[0] in roomsUsed:
				pass
			else:
				roomsUsed.append(room.name.split(r".")[0])
				QwAux = QwAux + 4*(configuration.settings.consume_pc_on * (1-EffEquipment))
		self.QEquipment = QwAux

	#Get thermal load
	def getQ(self, model, time):
		Ti = self.temperature
		if self.season == 'summer':
			self.walls(configuration.settings.UWall, Ti, self.getTo(model), model)
			self.roofs(configuration.settings.URoof, Ti, self.getTo(model), model)
			self.windows(configuration.settings.UWindow, Ti, self.getTo(model), configuration.settings.SCWindow, model)
			self.innerwalls(configuration.settings.UInnerWall, Ti)
			self.ventilation(configuration.settings.ACH, configuration.settings.CFMByOccupant, configuration.settings.airDensity, configuration.settings.airSpecificHeat, configuration.settings.waterSpecificHeat, Ti, self.getTo(model), configuration.settings.humiditySummerIn, configuration.settings.humiditySummerOut)
			self.infiltration(configuration.settings.airDensity, configuration.settings.airSpecificHeat, Ti)   
			self.ocuppancy(configuration.settings.SHGByPerson, configuration.settings.CLF, configuration.settings.LHGByPerson)
			self.lights(configuration.settings.EffLights)
			self.engines(configuration.settings.consume_hvac_on)
			self.equipment(configuration.settings.EffEquipment)
			self.Qtotal = (self.QWalls + self.QRoofs + self.QWindows + self.QVentilation + self.QInfiltration + self.QInnerWalls + self.QOcuppancy + self.QLights + self.QEngines + self.QEquipment)*time/3600
			'''
			if 'Office1' == self.rooms[0].name:
				print()
				print('Q init')
				print(self.rooms[0].name)
				print('Temperature out: ', self.getTo(models))
				print('Temperature zone: ', self.temperature)
				print('Desired: temperature', Ti)
				print('Qtotal: ', self.Qtotal)
				print('QWalls: ', self.QWalls)
				print('Qroofs: ', self.QRoofs)
				print('Qwindows: ', self.QWindows)
				print('QinnerWalls: ', self.QInnerWalls)
				print('Qventilation: ', self.QVentilation)
				print('Qinfiltration: ', self.QInfiltration)
				print('Qoccupancy: ', self.QOcuppancy)
				print('Qlights: ', self.QLights)
				print('Qengines: ', self.QEngines)
				print('Qequipment: ', self.QEquipment)
			'''

		else: #Winter
			self.walls(configuration.settings.UWall, Ti, self.getTo(model), model)
			self.windows(configuration.settings.UWindow, Ti, self.getTo(model), 0, model)
			self.innerwalls(configuration.settings.UInnerWall, Ti)
			self.ventilation(configuration.settings.ACH, configuration.settings.CFMByOccupant, configuration.settings.airDensity, configuration.settings.airSpecificHeat, configuration.settings.waterSpecificHeat, Ti, self.getTo(model), configuration.settings.humidityWinterIn, configuration.settings.humidityWinterOut)
			self.infiltration(configuration.settings.airDensity, configuration.settings.airSpecificHeat, Ti)
			self.Qtotal = (self.QWalls + self.QWindows + self.QVentilation + self.QInfiltration + self.QInnerWalls)*time/3600

	#Get maximun thermal load
	def getMaximunQ(self, model):
		if self.season == 'summer':
			Ti = configuration.settings.temperatureSummerInMinimun
			self.walls(configuration.settings.UWall, Ti, self.getTo(model), model)
			self.roofs(configuration.settings.URoof,Ti, self.getTo(model), model)
			self.windows(configuration.settings.UWindow, Ti, self.getTo(model), configuration.settings.SCWindow, model)
			self.innerwallsMaximun(configuration.settings.UInnerWall, Ti, configuration.settings.temperatureSummerOut[model.clock.hour]) 
			self.ventilation(configuration.settings.ACH, configuration.settings.CFMByOccupant, configuration.settings.airDensity, configuration.settings.airSpecificHeat, configuration.settings.waterSpecificHeat, Ti, self.getTo(model), configuration.settings.humiditySummerIn, configuration.settings.humiditySummerOut)
			self.ocuppancyMaximun(configuration.settings.SHGByPerson, configuration.settings.CLF, configuration.settings.LHGByPerson)
			self.lightsMaximun(configuration.settings.EffLights)
			self.enginesMaximun(configuration.settings.consume_hvac_on)
			self.equipmentMaximun(configuration.settings.EffEquipment)
			self.Qtotal = self.QWalls + self.QRoofs + self.QWindows + self.QVentilation + self.QInfiltration + self.QInnerWalls + self.QOcuppancy + self.QLights + self.QEngines + self.QEquipment

			'''
			print()
			print('MAXIMA Q de HVAC')
			print(self.rooms[0].name)
			print('Temperature out: ', self.getTo(models))
			print('Temperature zone: ', self.temperature)
			print('Desired: temperature', Ti)
			print('Qtotal: ', self.Qtotal)
			print('QWalls: ', self.QWalls)
			print('Qroofs: ', self.QRoofs)
			print('Qwindows: ', self.QWindows)
			print('QinnerWalls: ', self.QInnerWalls)
			print('Qventilation: ', self.QVentilation)
			print('Qinfiltration: ', self.QInfiltration)
			print('Qoccupancy: ', self.QOcuppancy)
			print('Qlights: ', self.QLights)
			print('Qengines: ', self.QEngines)
			print('Qequipment: ', self.QEquipment)
			print('Maxima Q: ', self.Qtotal)
			'''

		else: #Winter
			Ti = configuration.settings.temperatureWinterInMaximun
			self.walls(configuration.settings.UWall, Ti, self.getTo(model), model)
			self.windows(configuration.settings.UWindow, Ti, self.getTo(model), 0, model)
			self.innerwallsMaximun(configuration.settings.UInnerWall, Ti)
			self.ventilation(configuration.settings.ACH, configuration.settings.CFMByOccupant, configuration.settings.airDensity, configuration.settings.airSpecificHeat, configuration.settings.waterSpecificHeat, Ti, self.getTo(model), configuration.settings.humidityWinterIn, configuration.settings.humidityWinterOut)
			self.infiltrationMaximun(configuration.settings.airDensity, configuration.settings.airSpecificHeat, Ti)
			self.Qtotal = (self.QWalls + self.QWindows + self.QVentilation + self.QInfiltration + self.QInnerWalls)

	def changeTemperature(self):
		VolAir = 0
		#print(self.temperature)
		#print(self.Qtotal, self.QHVAC)

		for room in self.rooms:
			VolAir = VolAir + (room.dx * room.dy * room.dh)

		Q = (self.QHVAC - self.Qtotal)*60
		#Q = (self.QHVAC*configuration.settings.time_by_step) - (self.Qtotal)*60
		VarT = Q/(configuration.settings.airSpecificHeat * (VolAir*0.7) * configuration.settings.airDensity)
		if self.season == 'summer':
			self.temperature = self.temperature - VarT
		else:
			self.temperature = self.temperature + VarT
		self.QHVAC = 0
	def step(self):
		self.changeTemperature()
		#print('temperatura:', self.temperature)