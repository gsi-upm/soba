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

ipServer = socket.gethostbyname(socket.gethostname())

port = "10000"
URLBASE = "http://127.0.0.1:" + port
URISOBA = "/api/soba/v1/occupants"
URISEBA = "/api/seba/v1/occupants"
URIFIRE = "/api/seba/v1/fire"
stringTemplate = {"type": "string"}
numberTemplate = {"type": "number"}



class SEBATest(SEBAModel, TestCase):

	def __init__(self, width, height, jsonMap, jsonsOccupants, sebaConfiguration, seed ):
		super().__init__(width, height, jsonMap, jsonsOccupants, sebaConfiguration, seed)
		
		self.updateOccupancyInfo()



		print('Testing GET a list of occupants')

		occupantsId = [0, 1, 2]
		occupantsIdSim = []
		for o in self.occupants:
			occupantsIdSim.append(o.unique_id)

		self.updateOccupancyInfo()
		self.testListOccupants(occupantsId)



		print('Testing GET positions of the occupants')

		occupantTest0 = self.getOccupantId(0)
		occupantTest1 = self.getOccupantId(1)
		occupantTest2 = self.getOccupantId(2)

		pos0 = (6, 7)
		pos1 = (3, 8)
		pos2 = (5, 4)
		
		self.model.grid.move_agent(occupantTest0, pos0)
		self.model.grid.move_agent(occupantTest1, pos1)
		self.model.grid.move_agent(occupantTest2, pos2)
		self.updateOccupancyInfo()


		occupantsPos = {
			'0': {'y': 7, 'x': 6}, 
			'1': {'y': 8, 'x': 3}, 
			'2': {'y': 4, 'x': 5}, 
		}

		pos0Sim = occupantTest0.pos
		pos1Sim = occupantTest1.pos
		pos2Sim = occupantTest2.pos

		y0, x0 = pos0Sim
		y1, x1 = pos1Sim
		y2, x2 = pos2Sim

		occupantsPosSim = {
			'0': {'y': y0, 'x': x0}, 
			'1': {'y': y1, 'x': x1}, 
			'2': {'y': y2, 'x': x2}, 
		}

		self.testPositionsOccupants()

		print('Testing GET states of the occupants')

		state1 = 'testState1'
		state2 = 'testState2'

		occupantsSta1 = {
			'0': state1, 
			'1': state1, 
			'2': state1, 
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
			'0': state2, 
			'1': state2, 
			'2': state2, 
		}

		occupantsStaSim2 = {
			'0': occupantTest0.state, 
			'1': occupantTest1.state, 
			'2': occupantTest2.state, 
		}


		

		self.testStatesOccupants(occupantsSta2 ,occupantsStaSim2)



		# End test
		
		print("Testing finished.")
		os.system("kill -9 %d"%(os.getpid()))
		os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)

	#Test methods

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
		assertDictContainsSubset(occupantsPosSim, occupantsPos)
		assertDictContainsSubset(APIResponse, occupantsPosSim)

	def testStatesOccupants(self, occupantsSta , occupantsStaSim):
		print(str('Testing {}').format('GET /api/soba/v1/occupants/states'))
		url = URLBASE + URISOBA + "/states"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		APIResponse  = datajson				
		assertDictContainsSubset(occupantsPosSim, occupantsPos)
		assertDictContainsSubset(APIResponse, occupantsPosSim)

	def testInformationOccupant():
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}'))
		url = URLBASE + URISOBA + "/" + str(0)
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)

	def testMovementsOccupants():
		print(str('Testing {}').format('GET /api/soba/v1/occupants/movements'))
		url = URLBASE + URISOBA + "/movements"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)

	def testMovementOccupant():
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/movement'))
		url = URLBASE + URISOBA + "/" + str(0) + "/movement"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)

	def testPositionOccupant():
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/position'))
		url = URLBASE + URISOBA + "/" + str(0) + "/position"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)

	def testStateOccupant():
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/state'))
		url = URLBASE + URISOBA + "/" + str(0) + "/state"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)

	def testFovOccupant():
		print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/fov'))
		url = URLBASE + URISOBA + "/" + str(0) + "/fov"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)

	def testCreateSobaAvatar():
		print(str('Testing {}').format('PUT /api/soba/v1/occupants/{id}'))
		dataBody = {"x": 10, "y": 10}
		url = URLBASE + URISOBA + "/" + str(0)
		data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)

	def testMoveAvatar():
		print(str('Testing {}').format('POST /api/soba/v1/occupants/{id}/position'))
		dataBody = {"x": 11, "y": 11}
		url = URLBASE + URISOBA + "/" + str(100000) + "/position"
		data = requests.post(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)

	def testRouteOccupant():
		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/route/{route_id}'))
		url = URLBASE + URISEBA + "/" + str(100000) + "/route/1"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)
		
	def testCreateSebaAvatar():
		print(str('Testing {}').format('PUT /api/seba/v1/occupants/{id}'))
		dataBody = {"x": 13, "y": 13}
		url = URLBASE + URISEBA + "/" + str(1)
		data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
		datajson = data.json()
		print("Response: ", datajson)

	def testFireInFovOccupant():
		print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/fire'))
		url = URLBASE + URISEBA + "/" + str(100000) + "/fire"
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)

	def testFirePositions():
		print(str('Testing {}').format('GET /api/seba/v1/fire'))
		url = URLBASE + URIFIRE
		data = requests.get(url)
		datajson = data.json()
		print("Response: ", datajson)



		'''
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
		'''

# Launch
strategy = 'nearest'
N = 3
states = OrderedDict([('testState1','out')])

json = [{'type': 'regular' , 'N': N, 'states': states , 'schedule': {}, 'variation': {}, 'markovActivity': {}, 'timeActivity': {}, 'timeActivityVariation': {}, 'strategy': strategy, 'speedEmergency': 1}]
conf = {'families': [], 'hazard': "10:00:00"}
with open('auxiliarFiles/labgsi.blueprint3d') as data_file:
	jsonMap = ramen.returnMap(data_file, offsety = 9, offsetx = 0)


fixed_params = {"width": 20, "height": 20, "jsonMap": jsonMap, "jsonsOccupants": json, 'sebaConfiguration': conf}
variable_params = {"seed": range(10, 500, 10)}
soba.run.run(SEBATest, fixed_params, variable_params)