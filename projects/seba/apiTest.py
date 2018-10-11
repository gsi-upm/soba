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
import sys
from PyUnitReport import HTMLTestRunner

## Rest Service variables ##

ipServer = socket.gethostbyname(socket.gethostname())

port = "10000"
URLBASE = "http://127.0.0.1:" + port
URISOBA = "/api/soba/v1/occupants"
URISEBA = "/api/seba/v1/occupants"
URIFIRE = "/api/seba/v1/fire"
stringTemplate = {"type": "string"}
numberTemplate = {"type": "number"}

global modelSto
modelSto = None

## Test Class ##

class test(TestCase):

	## Test methods ##

	model = False
	occupantTest0 = True
	occupantTest1 = True
	occupantTest2 = True

	def setUp(self):
		global modelSto
		self.model = modelSto
		self.N = 1
		self.model.updateOccupancyInfo()
		self.occupantTest0 = self.model.getOccupantId(0)
		self.occupantTest1 = self.model.getOccupantId(1)
		self.occupantTest2 = self.model.getOccupantId(2)

	def test01_ListOccupants(self):

		print(str('Testing {}').format('GET /api/soba/v1/occupants'))

		occupantsId = [0, 1, 2]
		occupantsIdSim = []
		for o in self.model.occupants:
			occupantsIdSim.append(o.unique_id)
		self.model.updateOccupancyInfo()

		url = URLBASE + URISOBA
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse = datajson['occupants']				
		self.assertCountEqual(occupantsIdSim, occupantsId)
		self.assertCountEqual(APIResponse, occupantsIdSim)

	def test02_PositionsOccupants(self):

		print(str('Testing {}').format('GET /api/soba/v1/occupants/positions'))

		self.occupantTest0 = self.model.getOccupantId(0)
		self.occupantTest1 = self.model.getOccupantId(1)
		self.occupantTest2 = self.model.getOccupantId(2)

		pos0 = (6, 7)
		pos1 = (3, 8)
		pos2 = (5, 4)
		
		self.model.grid.move_agent(self.occupantTest0, pos0)
		self.model.grid.move_agent(self.occupantTest1, pos1)
		self.model.grid.move_agent(self.occupantTest2, pos2)
		self.model.updateOccupancyInfo()


		occupantsPos = {
			'0': {'y': 7, 'x': 6}, 
			'1': {'y': 8, 'x': 3}, 
			'2': {'y': 4, 'x': 5}, 
		}

		pos0Sim = self.occupantTest0.pos
		pos1Sim = self.occupantTest1.pos
		pos2Sim = self.occupantTest2.pos

		x0, y0 = pos0Sim
		x1, y1 = pos1Sim
		x2, y2 = pos2Sim

		occupantsPosSim = {
			'0': {'y': y0, 'x': x0}, 
			'1': {'y': y1, 'x': x1}, 
			'2': {'y': y2, 'x': x2}, 
		}


		url = URLBASE + URISOBA + "/positions"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson				
		self.assertDictContainsSubset(occupantsPosSim, occupantsPos)
		self.assertDictContainsSubset(APIResponse, occupantsPosSim)

	def test03_StatesOccupants(self):

		print(str('Testing {}').format('GET /api/soba/v1/occupants/states'))

		state1 = 'testState1'
		state2 = 'testState2'

		occupantsSta1 = {
			'0': 'testState1', 
			'1': 'testState1', 
			'2': 'testState1', 
		}
		occupantsStaSim1 = {
			'0': self.occupantTest0.state, 
			'1': self.occupantTest1.state, 
			'2': self.occupantTest2.state, 
		}


		url = URLBASE + URISOBA + "/states"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson			
		self.assertDictContainsSubset(occupantsStaSim1, occupantsSta1)
		self.assertDictContainsSubset(APIResponse, occupantsStaSim1)


		self.occupantTest0.state = state2
		self.occupantTest1.state = state2
		self.occupantTest2.state = state2
		self.model.updateOccupancyInfo()
		
		occupantsSta2 = {
			'0': 'testState2', 
			'1': 'testState2', 
			'2': 'testState2', 
		}

		occupantsStaSim2 = {
			'0': self.occupantTest0.state, 
			'1': self.occupantTest1.state, 
			'2': self.occupantTest2.state, 
		}


		url = URLBASE + URISOBA + "/states"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson			
		self.assertDictContainsSubset(occupantsStaSim2, occupantsSta2)
		self.assertDictContainsSubset(APIResponse, occupantsStaSim2)

	def test04_MovementsOccupants(self):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/movements'))

		occupantsMov = {
			'0': {'orientation': 'out', 'speed': 0.71428},
			'1': {'orientation': 'out', 'speed': 0.71428},
			'2': {'orientation': 'out', 'speed': 0.71428},
		}

		speed0Sim = self.occupantTest0.movement['speed']
		speed1Sim = self.occupantTest1.movement['speed']
		speed2Sim = self.occupantTest2.movement['speed']
		orientation0Sim = self.occupantTest0.movement['orientation']
		orientation1Sim = self.occupantTest1.movement['orientation']
		orientation2Sim = self.occupantTest2.movement['orientation']

		occupantsMovSim = {
			'0': {'orientation': orientation0Sim, 'speed': speed0Sim}, 
			'1': {'orientation': orientation1Sim, 'speed': speed1Sim}, 
			'2': {'orientation': orientation2Sim, 'speed': speed2Sim}, 
		}

		url = URLBASE + URISOBA + "/movements"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson			
		self.assertDictContainsSubset(occupantsMovSim, occupantsMov)
		self.assertDictContainsSubset(APIResponse, occupantsMovSim)

		self.occupantTest0.movement = {'orientation': 'E', 'speed': 1}
		self.occupantTest1.movement = {'orientation': 'S', 'speed': 1}
		self.occupantTest2.movement = {'orientation': 'N', 'speed': 1}
		self.model.updateOccupancyInfo()

		occupantsMov = {
			'0': {'orientation': 'E', 'speed': 1},
			'1': {'orientation': 'S', 'speed': 1},
			'2': {'orientation': 'N', 'speed': 1},
		}

		speed0Sim = self.occupantTest0.movement['speed']
		speed1Sim = self.occupantTest1.movement['speed']
		speed2Sim = self.occupantTest2.movement['speed']
		orientation0Sim = self.occupantTest0.movement['orientation']
		orientation1Sim = self.occupantTest1.movement['orientation']
		orientation2Sim = self.occupantTest2.movement['orientation']

		occupantsMovSim = {
			'0': {'orientation': orientation0Sim, 'speed': speed0Sim}, 
			'1': {'orientation': orientation1Sim, 'speed': speed1Sim}, 
			'2': {'orientation': orientation2Sim, 'speed': speed2Sim}, 
		}

		url = URLBASE + URISOBA + "/movements"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson			
		self.assertDictContainsSubset(occupantsMovSim, occupantsMov)
		self.assertDictContainsSubset(APIResponse, occupantsMovSim)

	def test05_InformationOccupant(self):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}'))

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
				"movement": self.occupantTest0.movement,
				"unique_id": str(self.occupantTest0.unique_id),
				"position":{"x": self.occupantTest0.pos[0],"y": self.occupantTest0.pos[1]},
				"fov": self.occupantTest0.fov,
				"state": self.occupantTest0.state
			}
		}

		self.occupantTest0.movement = {'orientation': 'E', 'speed': 1}

		idOc0 = self.occupantTest0.unique_id

		url = URLBASE + URISOBA + "/" + str(idOc0)
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantInfoSim, occupantInfo)
		self.assertDictContainsSubset(APIResponse, occupantInfoSim)

	def test06_MovementOccupant(self):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/movement'))

		occupantMov = { "movement": {'orientation': "E", 'speed': 1} }

		speed0Sim = self.occupantTest0.movement['speed']
		orientation0Sim = self.occupantTest0.movement['orientation']
		
		occupantMovSim = { "movement": {'orientation': orientation0Sim, 'speed': speed0Sim} }

		idOc0 = self.occupantTest0.unique_id

		url = URLBASE + URISOBA + "/" + str(idOc0) + "/movement"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantMovSim, occupantMov)
		self.assertDictContainsSubset(APIResponse, occupantMovSim)

	def test07_PositionOccupant(self):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/position'))
		
		occupantPos = { 'position': {'y': 7, 'x': 6} }

		occupantPosSim = { 'position': {'y': self.occupantTest0.pos[1], 'x': self.occupantTest0.pos[0]} }

		idOc0 = self.occupantTest0.unique_id


		url = URLBASE + URISOBA + "/" + str(idOc0) + "/position"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantPosSim, occupantPos)
		self.assertDictContainsSubset(APIResponse, occupantPosSim)

	def test08_StateOccupant(self):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/state'))

		idOc0 = self.occupantTest0.unique_id

		occupantState2 = { 'state': 'testState2' }

		occupantStateSim2 = { 'state': self.occupantTest0.state }


		url = URLBASE + URISOBA + "/" + str(idOc0) + "/state"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantStateSim2, occupantState2)
		self.assertDictContainsSubset(APIResponse, occupantStateSim2)

	def test09_FovOccupant(self):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/fov'))

		idOc0 = self.occupantTest0.unique_id

		occupantFov = {"fov": []}

		occupantFovSim = {"fov": self.occupantTest0.fov}

		url = URLBASE + URISOBA + "/" + str(idOc0) + "/fov"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantFovSim, occupantFov)
		self.assertDictContainsSubset(APIResponse, occupantFovSim)

		self.occupantTest0.getFOV()
		self.model.updateOccupancyInfo()

		fovKnonwn = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (7, 7), (8, 7), (9, 7), (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (8, 11), (9, 11), (10, 11), (11, 11), (9, 12), (10, 12), (11, 12), (12, 12), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16), (12, 17), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17), (12, 18), (13, 18), (14, 18), (15, 18), (16, 18), (17, 18), (18, 18)]

		fovDicts = []
		for pos in fovKnonwn:
			fovDicts.append({"x": pos[0], "y": pos[1]})

		fovDictsSim = []
		for pos in self.occupantTest0.fov:
			fovDictsSim.append({"x": pos[0], "y": pos[1]})

		occupantFov = { "fov": fovDicts }

		occupantFovSim = { "fov": fovDictsSim }

		url = URLBASE + URISOBA + "/" + str(idOc0) + "/fov"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantFovSim, occupantFov)
		self.assertDictContainsSubset(APIResponse, occupantFovSim)

	def test10_CreateSobaAvatar(self):
		print(str('Testing {}').format('PUT /api/soba/v1/occupants/{id}'))

		idAvCreation = 1
		avatarXPos = 3
		avatarYPos = 6
		idAvCreationResponse = idAvCreation + 100000 

		avatarCreation = { 'avatar': { 'position': {'y': avatarYPos, 'x': avatarXPos}, 'id': idAvCreationResponse}}

		dataBody = {"x": avatarXPos, "y": avatarYPos}
		url = URLBASE + URISOBA + "/" + str(idAvCreation)
		data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(APIResponse, avatarCreation)

		self.model.updateOccupancyInfo()

		avatarTestSOBA = self.model.getOccupantId(idAvCreationResponse)

		avatarPos = {'position': {'y': 6, 'x': 3}}

		avatarPosSim = {'position': {'y': avatarTestSOBA.pos[1], 'x': avatarTestSOBA.pos[0]}}
		
		url = URLBASE + URISOBA + "/" + str(idAvCreationResponse) + "/position"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(avatarPosSim, avatarPos)
		self.assertDictContainsSubset(APIResponse, avatarPosSim)

	def test11_MoveAvatar(self):
		print(str('Testing {}').format('POST /api/soba/v1/occupants/{id}/position'))
			
		idAvCreation = 1
		idAvCreationResponse = idAvCreation + 100000

		avatarXPos = 5
		avatarYPos = 8

		avatarTestSOBA = self.model.getOccupantId(idAvCreationResponse)

		avatarMove = { 'avatar': { 'position': {'y': avatarYPos, 'x': avatarXPos}, 'id': idAvCreationResponse}}


		dataBody = {"x": avatarXPos, "y": avatarYPos}
		url = URLBASE + URISOBA + "/" + str(idAvCreationResponse) + "/position"
		data = requests.post(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(APIResponse, avatarMove)

		self.model.updateOccupancyInfo()

		avatarTestSOBA = self.model.getOccupantId(idAvCreationResponse)

		avatarPos = { 'position': {'y': avatarYPos, 'x': avatarXPos}}
		avatarPosSim = {'position': {'y': avatarTestSOBA.pos[1], 'x': avatarTestSOBA.pos[0]}}

		url = URLBASE + URISOBA + "/" + str(idAvCreationResponse) + "/position"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(avatarPosSim, avatarPos)
		self.assertDictContainsSubset(APIResponse, avatarPosSim)

	def test12_RouteOccupant(self):
		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/route/{route_id}'))

		occupantRoute = { "positions": [{'x': 4, 'y': 8}, {'x': 3, 'y': 8}, {'x': 2, 'y': 7}, {'x': 1, 'y': 6}, {'x': 0, 'y': 6}]}

		idAvCreation = 1
		idAvCreationResponse = idAvCreation + 100000

		avatarTestSOBA = self.model.getOccupantId(idAvCreationResponse)

		url = URLBASE + URISEBA + "/" + str(idAvCreationResponse) + "/route/1"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(APIResponse, occupantRoute)

		self.model.updateOccupancyInfo()

		lastPosRouteDict = occupantRoute["positions"][-1]
		lastPosRouteX = lastPosRouteDict["x"]
		lastPosRouteY = lastPosRouteDict["y"]
		lastPosRoute = (lastPosRouteX, lastPosRouteY)
		lastPosRouteSim = avatarTestSOBA.pos_to_go

		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/route/{route_id}'))
		print("Pos_to_go", lastPosRoute)
		self.assertCountEqual(lastPosRoute, lastPosRouteSim)

	def test13_CreateSebaAvatar(self):
		print(str('Testing {}').format('PUT /api/seba/v1/occupants/{id}'))

		idAvCreation = 2
		avatarXPos = 3
		avatarYPos = 6
		idAvCreationResponse = idAvCreation + 100000 


		avatarCreation = { 'avatar': { 'position': {'y': avatarYPos, 'x': avatarXPos}, 'id': idAvCreationResponse}}

		dataBody = {"x": avatarXPos, "y": avatarYPos}
		url = URLBASE + URISEBA + "/" + str(idAvCreation)
		data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(APIResponse, avatarCreation)

		self.model.updateOccupancyInfo()

		avatarTestSEBA = self.model.getOccupantId(idAvCreationResponse)

		avatarPos = {'position': {'y': 6, 'x': 3}}

		avatarPosSim = {'position': {'y': avatarTestSEBA.pos[1], 'x': avatarTestSEBA.pos[0]}}

		url = URLBASE + URISOBA + "/" + str(idAvCreationResponse) + "/position"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(avatarPosSim, avatarPos)
		self.assertDictContainsSubset(APIResponse, avatarPosSim)

	def test14_FireInFovOccupant(self):
		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/fire'))

		idAvCreation = 2
		idAvCreationResponse = idAvCreation + 100000 

		posFire1 = (5, 2)
		posFire2 = (7, 4)

		self.model.createFire(posFire1)
		self.model.FireControl.createFirePos(posFire2)

		idAvSEBA = idAvCreationResponse

		avatarTestSEBA = self.model.getOccupantId(idAvCreationResponse)

		occupantFireSimAux = avatarTestSEBA.getPosFireFOV()
		occupantFireSimPos = []
		for pos in occupantFireSimAux:
			occupantFireSimPos.append({'x': pos[0],'y': pos[1]})

		occupantFire = {"positions": [{'y': posFire1[1], 'x': posFire1[0]}, {'y': posFire2[1], 'x': posFire2[0]}]}
		occupantFireSim = {"positions": occupantFireSimPos}

		url = URLBASE + URISEBA + "/" + str(idAvSEBA) + "/fire"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(occupantFireSim, occupantFire)
		self.assertDictContainsSubset(APIResponse, occupantFireSim)

	def test15_FirePositions(self):
		print(str('Testing {}').format('GET /api/seba/v1/fire'))

		posFire1 = (5, 2)
		posFire2 = (7, 4)

		FirePosAux = []
		for pos in self.model.FireControl.fireMovements:
			FirePosAux.append({'x': pos[0],'y': pos[1]})

		firePos = {"positions": [{'y': posFire1[1], 'x': posFire1[0]}, {'y': posFire2[1], 'x': posFire2[0]}]}
		firePosSim = {"positions": FirePosAux}

		url = URLBASE + URIFIRE
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson
		self.assertDictContainsSubset(firePosSim, firePos)
		self.assertDictContainsSubset(APIResponse, firePosSim)

		## Running the test to evaluate the values of the model##
	

	def test16_ListOccupantsSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for o in datajson["occupants"]:
				validate(o, numberTemplate)

	def test17_PositionsOccupantsSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/movements"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template2)
			for k, v  in datajson.items():
				validate(k, stringTemplate)
				validate(int(k), numberTemplate)
				validate(v, template)

	def test18_StatesOccupantsSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/positions"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			for k, v in datajson.items():
				validate(k, stringTemplate)
				validate(int(k), numberTemplate)
				validate(v, template)

	def test19_MovementsOccupantsSchema(self):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/states'))
		for i in range(self.N):
			url = URLBASE + URISOBA + "/states"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			for k,v in datajson.items():
				validate(v, stringTemplate)
				validate(k, stringTemplate)
				validate(int(k), numberTemplate)

	def test20_InformationOccupantSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/" + str(0)
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			validate(int(datajson['occupant']['unique_id']), numberTemplate)
			print(template)
			for p in datajson['occupant']['fov']:
				validate(p, template2)

	def test21_MovementOccupantSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/" + str(0) + "/movement"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

	def test22_PositionOccupantSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/" + str(0) + "/position"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

	def test23_StateOccupantSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/" + str(0) + "/state"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

	def test24_FovOccupantSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/" + str(0) + "/fov"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for p in datajson['fov']:
				validate(p, template2)


	def test25_CreateSobaAvatarSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/" + str(0)
			data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

	def test26_MoveAvatarSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISOBA + "/" + str(100000) + "/position"
			data = requests.post(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

	def test27_RouteOccupantSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISEBA + "/" + str(100000) + "/route/1"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for m in datajson["positions"]:
				validate(m, template2)

	def test28_CreateSebaAvatarSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISEBA + "/" + str(1)
			data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)

	def test29_FireInFovOccupantSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URISEBA + "/" + str(100000) + "/fire"
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for m in datajson["positions"]:
				validate(m, template2)

	def test30FirePositionsSchema(self):
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

		for i in range(self.N):
			url = URLBASE + URIFIRE
			data = requests.get(url)
			datajson = data.json()
			print("Response: ", datajson)
			validate(datajson, template)
			for m in datajson["positions"]:
				validate(m, template2)

	def setDown(self):
		print("Testing finished.")
		os.system("kill -9 %d"%(os.getpid()))
		os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)

## Defining the Test Model and running the test ##
class SebaApiTest(SEBAModel):

	def __init__(self, width, height, jsonMap, jsonsOccupants, sebaConfiguration, seed):
		super().__init__(width, height, jsonMap, jsonsOccupants, sebaConfiguration, seed)
		sys.argv = [sys.argv[0]]
		global modelSto
		modelSto = self
		unittest.TestLoader.sortTestMethodsUsing = None
		unittest.main(testRunner=HTMLTestRunner(output='APIRest_test'), failfast=True)



sys.argv.append('-b')
sys.argv.append('-s')

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