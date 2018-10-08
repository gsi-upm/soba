import csv
import json

class Log():

	#Vars
	def __init__(self):
		
		self.nOccupantsInBuildingReport = []
		self.nOccupantsNormalInBuildingReport = []
		self.nOccupantsDisInBuildingReport = []
		self.nFamiliesInBuildingReport = []
		self.startEmergencyReport = []
		self.endEmergencyReport = []
		self.nOccupantsWorkingReport = []


	#Report
	def reportSimulationState(self, nOccupantsInBuilding = 0,  nOccupantsNormalInBuilding = 0, nOccupantsDisInBuilding = 0, 
		nFamiliesInBuilding = 0, startEmergency = False, endEmergency = False, nOccupantsWorking = 0):

		self.nOccupantsInBuildingReport.append(nOccupantsInBuilding)
		self.nOccupantsNormalInBuildingReport.append(nOccupantsNormalInBuilding)
		self.nOccupantsDisInBuildingReport.append(nOccupantsDisInBuilding)
		self.nFamiliesInBuildingReport.append(nFamiliesInBuilding)
		self.startEmergencyReport.append(startEmergency)
		self.endEmergencyReport.append(endEmergency)
		self.nOccupantsWorkingReport.append(nOccupantsWorking)


	#Save in file
	def saveSimulationState(self, time_by_step=60):
		dir = 'results/'

		print(self.nOccupantsInBuildingReport)
		print(self.nOccupantsNormalInBuildingReport)
		print(self.nOccupantsDisInBuildingReport)
		print(self.nFamiliesInBuildingReport)
		print(self.startEmergencyReport)
		print(self.endEmergencyReport)
		print(self.nOccupantsWorkingReport)

		with open(dir+'nOccupantsInBuilding.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['Time', 'Occupants inside the building'])
			n = 1
			for i in self.nOccupantsInBuildingReport:
				outPut.append([time_by_step*n, i])
				n += 1
			writer = csv.writer(f)
			writer.writerows(outPut)

		with open(dir+'nOccupantsNormalInBuilding.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['Time', 'Normal ocupants inside the building'])
			n = 1
			for i in self.nOccupantsNormalInBuildingReport:
				outPut.append([time_by_step*n, i])
				n += 1
			writer = csv.writer(f)
			writer.writerows(outPut)

		with open(dir+'nOccupantsDisInBuilding.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['Time', 'Dis occupants inside the building'])
			n = 1
			for i in self.nOccupantsDisInBuildingReport:
				outPut.append([time_by_step*n, i])
				n += 1
			writer = csv.writer(f)
			writer.writerows(outPut)

		with open(dir+'nFamiliesInBuilding.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['Time', 'Families inside the building'])
			n = 1
			for i in self.nFamiliesInBuildingReport:
				outPut.append([time_by_step*n, i])
				n += 1
			writer = csv.writer(f)
			writer.writerows(outPut)

		with open(dir+'startEndEmergency.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['Event', "Time"])
			outPut.append(['Start Emergency', time_by_step*self.startEmergencyReport.index(next(item for item in self.startEmergencyReport if item is not False))])
			outPut.append(['End Emergency', time_by_step*self.endEmergencyReport.index(next(item for item in self.endEmergencyReport if item is not False))])
			writer = csv.writer(f)
			writer.writerows(outPut)

		with open(dir+'nOccupantsWorking.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['Time', 'Occupants working'])
			n = 1
			for i in self.nOccupantsWorkingReport:
				outPut.append([time_by_step*n, i])
				n += 1
			writer = csv.writer(f)
			writer.writerows(outPut)