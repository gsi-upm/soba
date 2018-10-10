import soba.visualization.ramen.mapGenerator as ramen
import soba.run
from collections import OrderedDict
from model import SEBAModel
from time import time
import os
import signal
from unittest import TestCase
import json, requests
from jsonschema import validate
import socket
import unittest
import listener 

## Rest Service variables ##

ipServer = socket.gethostbyname(socket.gethostname())

port = "10000"
URLBASE = "http://127.0.0.1:" + port
URISOBA = "/api/soba/v1/occupants"
URISEBA = "/api/seba/v1/occupants"
URIFIRE = "/api/seba/v1/fire"
stringTemplate = {"type": "string"}
numberTemplate = {"type": "number"}


## Test Class ##

class SebaApiTest(SEBAModel, TestCase):

	def __init__(self, width, height, jsonMap, jsonsOccupants, sebaConfiguration, seed ):
		super().__init__(width, height, jsonMap, jsonsOccupants, sebaConfiguration, seed)
		
		## Running the test to evaluate the values of the model ##

		self.updateOccupancyInfo()

		occupantsId = [0, 1, 2]
		occupantsIdSim = []
		for o in self.occupants:
			occupantsIdSim.append(o.unique_id)

		self.updateOccupancyInfo()
		self.testListOccupants(occupantsId, occupantsIdSim)




		occupantTest0 = self.getOccupantId(0)
		occupantTest1 = self.getOccupantId(1)
		occupantTest2 = self.getOccupantId(2)

		pos0 = (6, 7)
		pos1 = (3, 8)
		pos2 = (5, 4)
		
		self.grid.move_agent(occupantTest0, pos0)
		self.grid.move_agent(occupantTest1, pos1)
		self.grid.move_agent(occupantTest2, pos2)
		self.updateOccupancyInfo()


		occupantsPos = {
			'0': {'y': 7, 'x': 6}, 
			'1': {'y': 8, 'x': 3}, 
			'2': {'y': 4, 'x': 5}, 
		}

		pos0Sim = occupantTest0.pos
		pos1Sim = occupantTest1.pos
		pos2Sim = occupantTest2.pos

		x0, y0 = pos0Sim
		x1, y1 = pos1Sim
		x2, y2 = pos2Sim

		occupantsPosSim = {
			'0': {'y': y0, 'x': x0}, 
			'1': {'y': y1, 'x': x1}, 
			'2': {'y': y2, 'x': x2}, 
		}

		self.testPositionsOccupants(occupantsPos , occupantsPosSim)

		print('Testing GET states of the occupants')

		state1 = 'testState1'
		state2 = 'testState2'

		occupantsSta1 = {
			'0': 'testState1', 
			'1': 'testState1', 
			'2': 'testState1', 
		}
		occupantsStaSim1 = {
			'0': occupantTest0.state, 
			'1': occupantTest1.state, 
			'2': occupantTest2.state, 
		}

		self.testStatesOccupants(occupantsSta1 ,occupantsStaSim1)

		
		occupantTest0.state = state2
		occupantTest1.state = state2
		occupantTest2.state = state2
		self.updateOccupancyInfo()
		
		occupantsSta2 = {
			'0': 'testState2', 
			'1': 'testState2', 
			'2': 'testState2', 
		}

		occupantsStaSim2 = {
			'0': occupantTest0.state, 
			'1': occupantTest1.state, 
			'2': occupantTest2.state, 
		}

		self.testStatesOccupants(occupantsSta2 ,occupantsStaSim2)

		#self.movement = {'speed': self.speed, 'orientation':'out'}

		occupantsMov = {
			'0': {'orientation': 'out', 'speed': 0.71428},
			'1': {'orientation': 'out', 'speed': 0.71428},
			'2': {'orientation': 'out', 'speed': 0.71428},
		}

		speed0Sim = occupantTest0.movement['speed']
		speed1Sim = occupantTest1.movement['speed']
		speed2Sim = occupantTest2.movement['speed']
		orientation0Sim = occupantTest0.movement['orientation']
		orientation1Sim = occupantTest1.movement['orientation']
		orientation2Sim = occupantTest2.movement['orientation']

		occupantsMovSim = {
			'0': {'orientation': orientation0Sim, 'speed': speed0Sim}, 
			'1': {'orientation': orientation1Sim, 'speed': speed1Sim}, 
			'2': {'orientation': orientation2Sim, 'speed': speed2Sim}, 
		}


		self.testMovementsOccupants(occupantsMov , occupantsMovSim)

		occupantTest0.movement = {'orientation': 'E', 'speed': 1}
		occupantTest1.movement = {'orientation': 'S', 'speed': 1}
		occupantTest2.movement = {'orientation': 'N', 'speed': 1}
		self.updateOccupancyInfo()

		occupantsMov = {
			'0': {'orientation': 'E', 'speed': 1},
			'1': {'orientation': 'S', 'speed': 1},
			'2': {'orientation': 'N', 'speed': 1},
		}

		speed0Sim = occupantTest0.movement['speed']
		speed1Sim = occupantTest1.movement['speed']
		speed2Sim = occupantTest2.movement['speed']
		orientation0Sim = occupantTest0.movement['orientation']
		orientation1Sim = occupantTest1.movement['orientation']
		orientation2Sim = occupantTest2.movement['orientation']

		occupantsMovSim = {
			'0': {'orientation': orientation0Sim, 'speed': speed0Sim}, 
			'1': {'orientation': orientation1Sim, 'speed': speed1Sim}, 
			'2': {'orientation': orientation2Sim, 'speed': speed2Sim}, 
		}


		self.testMovementsOccupants(occupantsMov , occupantsMovSim)

		occupantInfo = {
			"occupant": {
				"movement": {"orientation": "E", "speed": 1},
				"unique_id": "0",
				"position":{"x": 6,"y": 7},
				"fov":[],
				"state": "testState2"
			}
		}


		occupantInfoSim = {
			"occupant": {
				"movement": occupantTest0.movement,
				"unique_id": str(occupantTest0.unique_id),
				"position":{"x": occupantTest0.pos[0],"y": occupantTest0.pos[1]},
				"fov": occupantTest0.fov,
				"state": occupantTest0.state
			}
		}

		occupantTest0.movement = {'orientation': 'E', 'speed': 1}

		idOc0 = occupantTest0.unique_id

		self.testInformationOccupant(idOc0, occupantInfo, occupantInfoSim)



		occupantMov = { "movement": {'orientation': "E", 'speed': 1} }

		speed0Sim = occupantTest0.movement['speed']
		orientation0Sim = occupantTest0.movement['orientation']
		
		occupantsMovSim = { "movement": {'orientation': orientation0Sim, 'speed': speed0Sim} }

		idOc0 = occupantTest0.unique_id

		self.testMovementOccupant(idOc0, occupantMov, occupantsMovSim)


		occupantPos = { 'position': {'y': 7, 'x': 6} }

		occupantPosSim = { 'position': {'y': occupantTest0.pos[1], 'x': occupantTest0.pos[0]} }

		idOc0 = occupantTest0.unique_id


		self.testPositionOccupant(idOc0, occupantPos, occupantPosSim)

		

		idOc0 = occupantTest0.unique_id

		occupantState2 = { 'state': 'testState2' }

		occupantStateSim2 = { 'state': occupantTest0.state }

		self.testStateOccupant(idOc0, occupantState2, occupantStateSim2)


		occupantFov = { "fov": [] }

		occupantFovSim = { "fov": occupantTest0.fov }

		self.testFovOccupant(idOc0, occupantFov, occupantFovSim)

		occupantTest0.getFOV()
		self.updateOccupancyInfo()

		fovKnonwn = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (7, 7), (8, 7), (9, 7), (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (8, 11), (9, 11), (10, 11), (11, 11), (9, 12), (10, 12), (11, 12), (12, 12), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16), (12, 17), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17), (12, 18), (13, 18), (14, 18), (15, 18), (16, 18), (17, 18), (18, 18)]

		fovDicts = []
		for pos in fovKnonwn:
			fovDicts.append({"x": pos[0], "y": pos[1]})

		fovDictsSim = []
		for pos in occupantTest0.fov:
			fovDictsSim.append({"x": pos[0], "y": pos[1]})

		occupantFov = { "fov": fovDicts }

		occupantFovSim = { "fov": fovDictsSim }


		self.testFovOccupant(idOc0, occupantFov, occupantFovSim)



		idAvCreation = 1
		avatarXPos = 3
		avatarYPos = 6
		idAvCreationResponse = idAvCreation + 100000 


		avatarCreation = { 'avatar': { 'position': {'y': avatarYPos, 'x': avatarXPos}, 'id': idAvCreationResponse}}


		self.testCreateSobaAvatar(idAvCreation, avatarXPos, avatarYPos, avatarCreation)
		self.updateOccupancyInfo()

		avatarTestSOBA = self.getOccupantId(idAvCreationResponse)

		avatarPos = {'position': {'y': 6, 'x': 3}}

		avatarPosSim = {'position': {'y': avatarTestSOBA.pos[1], 'x': avatarTestSOBA.pos[0]}}

		self.testPositionOccupant(idAvCreationResponse, avatarPos, avatarPosSim)



		idAvCreation = idAvCreationResponse

		avatarXPos = 5
		avatarYPos = 8


		avatarMove = { 'avatar': { 'position': {'y': avatarYPos, 'x': avatarXPos}, 'id': idAvCreation}}

		self.testMoveAvatar(idAvCreation, avatarXPos, avatarYPos, avatarMove)
		self.updateOccupancyInfo()

		avatarPos = { 'position': {'y': avatarYPos, 'x': avatarXPos}}
		avatarPosSim = {'position': {'y': avatarTestSOBA.pos[1], 'x': avatarTestSOBA.pos[0]}}

		self.testPositionOccupant(idAvCreationResponse, avatarPos, avatarPosSim)


		occupantRoute = { "positions": [{'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 2, 'y': 7}, {'x': 1, 'y': 6}, {'x': 0, 'y': 6}]}

		self.testRouteOccupant(idAvCreation, occupantRoute)
		self.updateOccupancyInfo()

		lastPosRouteDict = occupantRoute["positions"][-1]
		lastPosRouteX = lastPosRouteDict["x"]
		lastPosRouteY = lastPosRouteDict["y"]
		lastPosRoute = (lastPosRouteX, lastPosRouteY)
		lastPosRouteSim = avatarTestSOBA.pos_to_go

		self.testRouteOccupantAux(lastPosRoute, lastPosRouteSim)



		idAvCreation = 2
		avatarXPos = 3
		avatarYPos = 6
		idAvCreationResponse = idAvCreation + 100000 


		avatarCreation = { 'avatar': { 'position': {'y': avatarYPos, 'x': avatarXPos}, 'id': idAvCreationResponse}}


		self.testCreateSobaAvatar(idAvCreation, avatarXPos, avatarYPos, avatarCreation)
		self.updateOccupancyInfo()

		avatarTestSEBA = self.getOccupantId(idAvCreationResponse)

		avatarPos = {'position': {'y': 6, 'x': 3}}

		avatarPosSim = {'position': {'y': avatarTestSEBA.pos[1], 'x': avatarTestSEBA.pos[0]}}

		self.testPositionOccupant(idAvCreationResponse, avatarPos, avatarPosSim)

		posFire1 = (5, 2)
		posFire2 = (7, 4)

		self.createFire(posFire1)
		self.FireControl.createFirePos(posFire2)

		idAvSEBA = idAvCreationResponse

		occupantFireSimAux = avatarTestSEBA.getPosFireFOV()
		occupantFireSimPos = []
		for pos in occupantFireSimAux:
			occupantFireSimPos.append({'x': pos[0],'y': pos[1]})

		occupantFire = {"positions": [{'y': posFire1[1], 'x': posFire1[0]}, {'y': posFire2[1], 'x': posFire2[0]}]}
		occupantFireSim = {"positions": occupantFireSimPos}

		self.testFireInFovOccupant(idAvSEBA, occupantFire, occupantFireSim)

		FirePosAux = []
		for pos in self.FireControl.fireMovements:
			FirePosAux.append({'x': pos[0],'y': pos[1]})

		firePos = {"positions": [{'y': posFire1[1], 'x': posFire1[0]}, {'y': posFire2[1], 'x': posFire2[0]}]}
		firePosSim = {"positions": FirePosAux}


		self.testFirePositions(firePos, firePosSim)


		## Method to run the test to evaluate the Api responses schema ##

		self.testSchema(N=1)



		# End test
		print("Testing finished.")
		os.system("kill -9 %d"%(os.getpid()))
		os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)


	## Test methods ##

	def testListOccupants(self, occupantsId, occupantsIdSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants'))
		url = URLBASE + URISOBA
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse = datajson['occupants']				
		self.assertCountEqual(occupantsIdSim, occupantsId)
		self.assertCountEqual(APIResponse, occupantsIdSim)

	def testPositionsOccupants(self, occupantsPos , occupantsPosSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/positions'))
		url = URLBASE + URISOBA + "/positions"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson				
		self.assertDictContainsSubset(occupantsPosSim, occupantsPos)
		self.assertDictContainsSubset(APIResponse, occupantsPosSim)

	def testStatesOccupants(self, occupantsSta , occupantsStaSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/states'))
		url = URLBASE + URISOBA + "/states"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson			
		self.assertDictContainsSubset(occupantsStaSim, occupantsSta)
		self.assertDictContainsSubset(APIResponse, occupantsStaSim)

	def testMovementsOccupants(self, occupantsMov , occupantsMovSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/movements'))
		url = URLBASE + URISOBA + "/movements"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson			
		self.assertDictContainsSubset(occupantsMovSim, occupantsMov)
		self.assertDictContainsSubset(APIResponse, occupantsMovSim)

	def testInformationOccupant(self, idOc, occupantInfo, occupantInfoSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}'))
		url = URLBASE + URISOBA + "/" + str(idOc)
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantInfoSim, occupantInfo)
		self.assertDictContainsSubset(APIResponse, occupantInfoSim)

	def testMovementOccupant(self, idOc, occupantMov, occupantMovSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/movement'))
		url = URLBASE + URISOBA + "/" + str(idOc) + "/movement"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantMovSim, occupantMov)
		self.assertDictContainsSubset(APIResponse, occupantMovSim)

	def testPositionOccupant(self, idOc, occupantPos, occupantPosSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/position'))
		url = URLBASE + URISOBA + "/" + str(idOc) + "/position"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantPosSim, occupantPos)
		self.assertDictContainsSubset(APIResponse, occupantPosSim)

	def testStateOccupant(self, idOc, occupantState, occupantStateSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/state'))
		url = URLBASE + URISOBA + "/" + str(idOc) + "/state"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantStateSim, occupantState)
		self.assertDictContainsSubset(APIResponse, occupantStateSim)

	def testFovOccupant(self, idOc, occupantFov, occupantFovSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/fov'))
		url = URLBASE + URISOBA + "/" + str(idOc) + "/fov"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantFovSim, occupantFov)
		self.assertDictContainsSubset(APIResponse, occupantFovSim)

	def testCreateSobaAvatar(self, idAvCreation, avatarXPos, avatarYPos, avatarCreation):
		print(str('Testing {}').format('PUT /api/soba/v1/occupants/{id}'))
		dataBody = {"x": avatarXPos, "y": avatarYPos}
		url = URLBASE + URISOBA + "/" + str(idAvCreation)
		data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(APIResponse, avatarCreation)

	def testMoveAvatar(self, idAvCreation, avatarXPos, avatarYPos, avatarMove):
		print(str('Testing {}').format('POST /api/soba/v1/occupants/{id}/position'))
		dataBody = {"x": avatarXPos, "y": avatarYPos}
		url = URLBASE + URISOBA + "/" + str(idAvCreation) + "/position"
		data = requests.post(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(APIResponse, avatarMove)

	def testRouteOccupant(self, idAvCreation, occupantRoute):
		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/route/{route_id}'))
		url = URLBASE + URISEBA + "/" + str(idAvCreation) + "/route/1"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(APIResponse, occupantRoute)

	def testRouteOccupantAux(self, lastPosRoute, lastPosRouteSim):
		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/route/{route_id}'))
		print("Pos_to_go", lastPosRoute)
		self.assertCountEqual(lastPosRoute, lastPosRouteSim)

	def testCreateSebaAvatar(self, idAvCreation, avatarXPos, avatarYPos, avatarCreation):
		print(str('Testing {}').format('PUT /api/seba/v1/occupants/{id}'))
		dataBody = {"x": avatarXPos, "y": avatarYPos}
		url = URLBASE + URISEBA + "/" + str(idAvCreation)
		data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(APIResponse, avatarCreation)

	def testFireInFovOccupant(self, idAvSEBA, occupantFire, occupantFireSim):
		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/fire'))
		url = URLBASE + URISEBA + "/" + str(idAvSEBA) + "/fire"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantFireSim, occupantFire)
		self.assertDictContainsSubset(APIResponse, occupantFireSim)

	def testFirePositions(self, firePos, firePosSim):
		print(str('Testing {}').format('GET /api/seba/v1/fire'))
		url = URLBASE + URIFIRE
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(firePosSim, firePos)
		self.assertDictContainsSubset(APIResponse, firePosSim)



	def testSchema(self, N):
		print(str('Testing {}').format('GET /api/soba/v1/occupants'))
		template = {
			"type": "object",
			"properties": {
				"occupants": {
					"type": "array"
					}
			},
			"required": ["occupants"]
		}

		for i in range(N):
			url = URLBASE + URISOBA
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for o in datajson["occupants"]:
				validate(o, numberTemplate)

		print(str('Testing {}').format('GET /api/soba/v1/occupants/movements'))
		template = {
			"type": "object",
			"properties": {
				"orientation": {
					"type": "string"
					},
				"speed": {
					"type": "number"
					}
			},
			"required": ["orientation", "speed"]
		}

		template2 = {
			"type": "object"
		}

		for i in range(N):
			url = URLBASE + URISOBA + "/movements"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template2)
			for k, v  in datajson.items():
				validate(k, stringTemplate)
				validate(int(k), numberTemplate)
				validate(v, template)

		print(str('Testing {}').format('GET /api/soba/v1/occupants/positions'))
		template = {
			"type": "object",
			"properties": {
				"x": {
					"type": "number"
					},
				"y": {
					"type": "number"
					}
			},
			"required": ["x", "y"]
		}

		for i in range(N):
			url = URLBASE + URISOBA + "/positions"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			for k, v in datajson.items():
				validate(k, stringTemplate)
				validate(int(k), numberTemplate)
				validate(v, template)


		print(str('Testing {}').format('GET /api/soba/v1/occupants/states'))
		for i in range(N):
			url = URLBASE + URISOBA + "/states"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			for k,v in datajson.items():
				validate(v, stringTemplate)
				validate(k, stringTemplate)
				validate(int(k), numberTemplate)

		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}'))
		template = {
			"type": "object",
			"properties": {
				"occupant":{
					"type": "object",
					"properties": {
							"state":{
								"type": "string"
							},
							"fov": {
								"type": "array"
							},
							"unique_id":{
								"type": "string"
							},
							"movement": {
								"type": "object",
								"properties": {
									"orientation":{
										"type": "string"
									},
									"speed":{
										"type": "number"
									},
								},
								"required": ["orientation", "speed"]
							},
							"position": {
								"type": "object",
								"properties": {
									"x":{
										"type": "number"
									},
									"y":{
										"type": "number"
									}
								},
								"required": ["x", "y"]
							}
					},
			"required": ["state", "fov", "unique_id", "movement", "position"]
				}
			},
			"required": ["occupant"]
		}

		template2 = {
			"type": "object",
			"properties": {
				"x": {
					"type": "number"
					},
				"y": {
					"type": "number"
				}
			},
			"required": ["x", "y"]
		}

		for i in range(N):
			url = URLBASE + URISOBA + "/" + str(0)
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			validate(int(datajson['occupant']['unique_id']), numberTemplate)
			print(template)
			for p in datajson['occupant']['fov']:
				validate(p, template2)


		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/movement'))
		
		template = {
			"type": "object",
			"properties": {
				"movement":{
					"type": "object",
					"properties": {
							"orientation": {
								"type": "string"
							},
							"speed": {
								"type": "number"
							}
					},
				"required": ["orientation", "speed"]
				}
			},
			"required": ["movement"]
		}

		for i in range(N):
			url = URLBASE + URISOBA + "/" + str(0) + "/movement"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/position'))
		template = {
			"type": "object",
			"properties": {
				"position":{
					"type": "object",
					"properties": {
						"x": {
							"type": "number"
							},
						"y": {
							"type": "number"
						}
					},
					"required": ["x", "y"]
				}
			},
			"required": ["position"]
		}

		for i in range(N):
			url = URLBASE + URISOBA + "/" + str(0) + "/position"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)


		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/state'))
		template = {
			"type": "object",
			"properties":{
				"state": {
					"type": "string"
				}
			},
			"required": ["state"]
		}

		for i in range(N):
			url = URLBASE + URISOBA + "/" + str(0) + "/state"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)


		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/fov'))
		template = {
			"type": "object",
			"properties": {
				"fov": {
					"type": "array"
					}
			},
			"required": ["fov"]
		}
		

		template2 = {
			"type": "object",
			"properties": {
				"x": {
					"type": "number"
					},
				"y": {
					"type": "number"
				}
			},
			"required": ["x", "y"]
		}

		for i in range(N):
			url = URLBASE + URISOBA + "/" + str(0) + "/fov"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for p in datajson['fov']:
				validate(p, template2)



		print(str('Testing {}').format('PUT /api/soba/v1/occupants/{id}'))
		template = {
			"type": "object",
				"properties": {
					"avatar":{
						"type": "object",
						"properties": {
							"position":{
								"type": "object",
								"properties": {
									"x": {
										"type": "number",
									},
									"y": {
										"type": "number"
									}
								},
								"required": ["x", "y"]
							},
							"id":{
								"type": "number"
							}
					},
					"required": ["position", "id"]
				}
			},
			"required": ["avatar"]
		}

		dataBody = {"x": 10, "y": 10}

		for i in range(N):
			url = URLBASE + URISOBA + "/" + str(0)
			data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

		print(str('Testing {}').format('POST /api/soba/v1/occupants/{id}/position'))
		template = {
			"type": "object",
				"properties": {
					"avatar":{
						"type": "object",
						"properties": {
							"position":{
								"type": "object",
								"properties": {
									"x": {
										"type": "number",
									},
									"y": {
										"type": "number"
									}
								},
								"required": ["x", "y"]
							},
							"id":{
								"type": "number"
							}
					},
					"required": ["position", "id"]
				}
			},
			"required": ["avatar"]
		}
	
		dataBody = {"x": 11, "y": 11}

		for i in range(N):
			url = URLBASE + URISOBA + "/" + str(100000) + "/position"
			data = requests.post(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/route/{route_id}'))
		template = {
			"type": "object",
			"properties": {
				"positions": {
					"type": "array"
					}
			}
		}

		template2 = {
			"type": "object",
			"properties": {
				"x": {
					"type": "number"
					},
				"y": {
					"type": "number"
					}
			},
			"required": ["x", "y"]
		}

		for i in range(N):
			url = URLBASE + URISEBA + "/" + str(100000) + "/route/1"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for m in datajson["positions"]:
				validate(m, template2)


		print(str('Testing {}').format('PUT /api/seba/v1/occupants/{id}'))
		template = {
			"type": "object",
			"properties": {
				"avatar": {
					"type": "object",
					"properties":{
						"position":{
							"type": "object",
							"properties":{
								"x": {
									"type": "number"
								},
								"y": {
									"type": "number"
								}
							},
							"required": ["x", "y"]
						},
						"id": {
							"type": "number"
						}
					},
					"required": ["position", "id"]
				}
			},
			"required": ["avatar"]
		}

		dataBody = {"x": 13, "y": 13}

		for i in range(N):
			url = URLBASE + URISEBA + "/" + str(1)
			data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)


		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/fire'))
		template = {
			"type": "object",
			"properties": {
				"positions": {
					"type": "array"
					}
			},
			"required": ["positions"]
		}

		template2 = {
			"type": "object",
			"properties": {
				"x": {
					"type": "number"
					},
				"y": {
					"type": "number"
					}
			},
			"required": ["x", "y"]
		}

		for i in range(N):
			url = URLBASE + URISEBA + "/" + str(100000) + "/fire"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for m in datajson["positions"]:
				validate(m, template2)


		print(str('Testing {}').format('GET /api/seba/v1/fire'))
		template = {
			"type": "object",
			"properties": {
				"positions": {
					"type": "array"
					}
			},
			"required": ["positions"]
		}

		template2 = {
			"type": "object",
			"properties": {
				"x": {
					"type": "number"
					},
				"y": {
					"type": "number"
					}
			},
			"required": ["x", "y"]
		}

		for i in range(N):
			url = URLBASE + URIFIRE
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for m in datajson["positions"]:
				validate(m, template2)


## Defining the Test Model and running the test ##

strategy = 'nearest'
N = 3
states = OrderedDict([('testState1','out')])

json = [{'type': 'regular' , 'N': N, 'states': states , 'schedule': {}, 'variation': {}, 'markovActivity': {}, 'timeActivity': {}, 'timeActivityVariation': {}, 'strategy': strategy, 'speedEmergency': 1}]
conf = {'families': [], 'hazard': "10:00:00"}
with open('auxiliarFiles/labgsi.blueprint3d') as data_file:
	jsonMap = ramen.returnMap(data_file, offsety = 9, offsetx = 0)


fixed_params = {"width": 20, "height": 20, "jsonMap": jsonMap, "jsonsOccupants": json, 'sebaConfiguration': conf}
variable_params = {"seed": range(10, 500, 10)}
soba.run.run(SebaApiTest, fixed_params, variable_params)