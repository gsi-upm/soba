import json

steps = [[] for _ in range(1210)]

def addAgentMovement(agent, step, direction, speed, sentiment = "happiness"):
	steps[step].append({"agent": agent.unique_id, "direction": direction, "speed": speed, "sentiment": sentiment})

def stopAgent(agent, step):
	steps[step].append({ "agent": agent.unique_id, "stop": True})

def createAgent(agent, step, pos, rotation, sentiment = "happiness"):
	x, y = pos
	steps[step].append({ "agent": agent.unique_id, "position": {'x': (25*(2*(x+500)-20)), 'y': (25*(20-2*y))}, "sentiment": sentiment})

def removeAgent(agent, step):
	steps[step].append({ "agent": agent.unique_id, "outBuilding": True})

def generateJSON():
	data = {"type":2, "steps": steps}
	print('salida', data)
	with open('/home/merinom/Desktop/ramen/blueprint3d/example/js/movement/lab_move2.json', 'w') as outfile:
		json.dump(data, outfile)
		outfile.close()

'''
steps[0].append({"light":'low', "room": 'Hall.1'})
steps[0].append({"light":'low', "room": 'Lab1.1'})
steps[0].append({"light":'low', "room": 'Lab2.1'})

def addLightState(room, state, step):
	steps[step+2].append({"light":state, "room": room.name})

def stateTV(state, step):
	stateTV = 'false'
	if state == True:
		stateTV = 'true'
	steps[step].append({"video": stateTV, "room": "Hall.4"})
'''