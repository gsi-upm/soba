import json

steps = [[] for _ in range(800)]

def addAgentMovement(agent, step, direction, speed, sentiment = "happiness"):
	steps[step].append({"agent": agent.unique_id, "direction": direction, "speed": speed, "sentiment": sentiment})

def stopAgent(agent, step):
	steps[step].append({ "agent": agent.unique_id, "stop": True})

def createAgent(agent, step, pos, rotation, sentiment = "happiness"):
	x, y = pos
	steps[step].append({ "agent": agent.unique_id, "position": {'x': (x)*100*0.5, 'y': ((10-y*0.5+0.25)*100)}, "sentiment": sentiment})

def removeAgent(agent, step):
	steps[step].append({ "agent": agent.unique_id, "outBuilding": True})

def generateJSON():
	data = {"type":2, "steps": steps}
	with open('/home/merinom/Desktop/ramen/blueprint3d/example/js/movement/lab_move2.json', 'w') as outfile:
		json.dump(data, outfile)
		outfile.close()