import json
import time

steps = [[] for _ in range(1000)]

def addAgentMovement(agent, step, direction, speed, sentiment = "happiness"):
	steps[step].append({"agent": agent.unique_id, "direction": direction, "speed": speed, "sentiment": sentiment})

def stopAgent(agent, step):
	steps[step].append({ "agent": agent.unique_id, "stop": True})

def createAgent(agent, step, pos, rotation, sentiment = "happiness"):
	x, y = pos
	steps[step].append({ "agent": agent.unique_id, "position": {'x': x*100*0.5, 'y': ((10-y*0.5+0.25)*100)}, "sentiment": sentiment})

def removeAgent(agent, step):
	steps[step].append({ "agent": agent.unique_id, "outBuilding": True})

# Called methods
def reportCreation(agent, rotation):
    createAgent(agent, agent.model.NStep, agent.pos, rotation, sentiment = "happiness")

def reportExit(agent):
    removeAgent(agent, agent.model.NStep)

def reportMovement(agent, direction):
    addAgentMovement(agent, agent.model.NStep, direction, agent.speed)

def reportStop(agent):
    stopAgent(agent, agent.NStep)

def generateJSON():
	data = {"type":2, "steps": steps}
	print(steps)
	with open('outRamen.json', 'w') as outfile:
		json.dump(data, outfile)
		outfile.close()