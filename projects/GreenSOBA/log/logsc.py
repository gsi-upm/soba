import csv
import json

class Logsc():

#Results
	#Energy
	def collectEnergyValues(self, model, energyByDayTotal, energyByDayHVAC, energyByDayLPC, timeByStep, energyByStepTotal, energyByStepHVACsTotal, energyByStepLPCTotal):
		dir = 'results/'+str(model.voting_method)+'/'

		with open(dir+'energyByDayTotal.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['day', 'energy'])
			totalDays = 0
			for n in range(1, 6):
				totalDays = totalDays + energyByDayTotal[n-1]
				outPut.append([n,energyByDayTotal[n-1]])
			outPut.append(['total', totalDays])
			writer = csv.writer(f)
			writer.writerows(outPut)
		with open(dir+'energyByDayHVAC.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['day', 'energy'])
			totalDays = 0
			for n in range(1, 6):
				totalDays = totalDays + energyByDayHVAC[n-1]
				outPut.append([n, energyByDayHVAC[n-1]])
			outPut.append(['total', totalDays])
			writer = csv.writer(f)
			writer.writerows(outPut)
		with open(dir+'energyByDayLPC.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['day', 'energy'])
			totalDays = 0
			for n in range(1, 6):
				totalDays = totalDays + energyByDayLPC[n-1]
				outPut.append([n, energyByDayLPC[n-1]])
			outPut.append(['total', totalDays])
			writer = csv.writer(f)
			writer.writerows(outPut)

		with open(dir+'energyByStepTotal.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['sec', 'energy'])
			for n in range(0, len(energyByStepTotal)-1):
				outPut.append([n*timeByStep, energyByStepTotal[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)
		with open(dir+'energyByStepHVACsTotal.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['sec', 'energy'])
			for n in range(0, len(energyByStepHVACsTotal)-1):
				outPut.append([n*timeByStep, energyByStepHVACsTotal[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)
		with open(dir+'energyByStepLPCTotal.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['sec', 'energy'])
			for n in range(0, len(energyByStepLPCTotal)-1):
				outPut.append([n*timeByStep, energyByStepLPCTotal[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)

	#Comformity
	def collectComfortValues(self, model, timeByStep, agentsSatisfationByTime, fangerSatisfationByTime):
		dir = 'results/'+str(model.voting_method)+'/'
		with open(dir+'agentsSatisfationByTime.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['sec', 'comfort'])
			for n in range(0, len(agentsSatisfationByTime)-1):
				outPut.append([n*timeByStep,agentsSatisfationByTime[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)
		with open(dir+'fangerSatisfationByTime.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['sec', 'comfort'])
			for n in range(0, len(fangerSatisfationByTime)-1):
				outPut.append([n*timeByStep, fangerSatisfationByTime[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)

	#Satisfaction
	def collectSatisfactionValues(self, model, timeByStep, totalSatisfationByTime, averageSatisfationByTime):
		dir = 'results/'+str(model.voting_method)+'/'
		with open(dir+'agentsSatisfationTotalSCByTime.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['sec', 'satisfaction'])
			for n in range(0, len(totalSatisfationByTime)-1):
				outPut.append([n*timeByStep,totalSatisfationByTime[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)
		with open(dir+'agentsSatisfationAverageSCByTime.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['sec', 'satisfaction'])
			for n in range(0, len(averageSatisfationByTime)-1):
				outPut.append([n*timeByStep, averageSatisfationByTime[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)

	#Occupancy schedule
	def collectScheduleValues(self, model, timeByStep, agentsActivityByTime):
		dir = 'results/'+str(model.voting_method)+'/'
		with open(dir+'agentsActivityByTime.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['sec', 'number'])
			for n in range(0, len(agentsActivityByTime)-1):
				outPut.append([n*timeByStep,agentsActivityByTime[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)


#Temps
	#Occupants
	def saveOccupantsValues(self, data):
		with open('log/tmp/occupants.txt', 'w') as f:
			json.dump(data, f)

	def getOccupantsValues(self):
		with open('log/tmp/occupants.txt') as f:
			data = json.load(f)
			return data

	#Rooms
	def saveScheduleRooms(self, array):
		with open('log/tmp/rooms.csv', 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(array)

	def getScheduleRooms(self):
		with open('log/tmp/rooms.csv', newline='') as f:
			reader = csv.reader(f)
			returned = []
			for row in reader:
				returned.append(row)
			return returned