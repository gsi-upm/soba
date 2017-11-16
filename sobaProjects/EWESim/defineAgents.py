def init():

    global agents_json
    
    #Store the agents
    agents_json = []

        #Basic and default Agent

    #Number of users type Default
    NDefault = 2 #Will be created agents with N_agent = 0 and N_agent = 1

    #Define states: name (str), position(reserved word or tupla (pos as (x, y) = (5, 8)))
    states = [
        {'name':'leave', 'position': 'outOffice'}, #initial state (the first)
        {'name':'work in my workspace', 'position': 'workspace'},
        {'name':'have a coffe', 'position': 'coffeMaker'},
        {'name':'in a meeting', 'position': (4, 13)},
        {'name':'at restroom', 'position': 'outOffice'},
        {'name':'lunch', 'position': 'outOffice'}
    ]

    #Define initial markov matrix
    markov_matrix = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

    controlBehaviourDefault = {'arriveTime': 10, 'lunchTime': 13.30, 'backLunchTime': 15.0, 'leaveWork': 18.30 }

    agentDefault = {'type':'default' ,'N':NDefault, 'states': states, 'matrix': markov_matrix, 'lifeWay': controlBehaviourDefault}
    
    agents_json.append(agentDefault)


def returnMatrix(agent, time):
    new_matrix = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    behaviour = agent.behaviour
    if agent.type == 'default':
    	if time < behaviour['arriveTime']:
    		return new_matrix
    	elif behaviour['lunchTime'] >= time >= behaviour['arriveTime']:
        	new_matrix = [[60, 10, 20, 10, 0, 0], [0, 50, 0, 30, 20, 0], [0, 80, 0, 10, 10, 0], [0, 80, 0, 10, 10, 0],
        	[0, 80, 0, 10, 0, 0], [0, 0, 0, 0, 0, 0]]
    	elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
        	new_matrix = [[0, 0, 0, 0, 0, 0], [0, 50, 0, 0, 0, 50], [0, 0, 0, 0, 0, 100], [0, 0, 0, 50, 0, 50],
        	[0, 0, 0, 0, 0, 100], [0, 60, 30, 10, 0, 0]]
    	elif time >= behaviour['backLunchTime']:
        	new_matrix = [[0, 0, 0, 0, 0, 0], [0, 50, 0, 20, 30, 0], [0, 60, 0, 20, 10, 0], [0, 80, 0, 10, 10, 0],
        	[0, 80, 0, 20, 0, 0], [0, 20, 50, 10, 0, 20]]
    	elif time >= behaviour['leaveWork']:
        	new_matrix = [[0, 0, 0, 0, 0, 0], [50, 50, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0], [50, 0, 0, 50, 0, 0],
        	[0, 100, 0, 0, 0, 0], [0, 0,0 , 0, 0, 0]]
    	return new_matrix
    else:
    	return new_matrix

def getTimeInState(agent, time): #Hours.Minutes
	timeActivity_matrix = [0, 1.0, 0.1, 0.45, 0.1, 0]
	behaviour = agent.behaviour
	if agent.type == 'default':
	    if time < behaviour['arriveTime']:
	    	return timeActivity_matrix
	    elif behaviour['lunchTime'] >= time >= behaviour['arriveTime']:
	        timeActivity_matrix = [0, 1.0, 0.1, 0.45, 0.1, 0]
	    elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
	        timeActivity_matrix = [0, 0.3, 0.01, 0.20, 0, 1.3]
	    elif time >= behaviour['backLunchTime']:
	        timeActivity_matrix = [0, 1.0, 0.1, 0.45, 0.1, 0]
	    elif time >= behaviour['leaveWork']:
	        timeActivity_matrix = [0, 0.30, 0.01, 0.15, 0, 0]
	    return timeActivity_matrix
	else:
		return timeActivity_matrix