from mesa.visualization.ModularVisualization import ModularServer
from LabModel import LabModel
from CoffeMakerAgent import CoffeMakerAgent
from TVAgent import TVAgent
from AccessAgent import AccessAgent
from PC import PC
from DrawLabMapBackEnd import DrawLabMapBackEnd
from DrawLabMapBackEnd import RepresentationModule
from UserAgent import UserAgent

def agent_portrayal(agent):
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}

    if isinstance(agent, UserAgent) and agent.pos == (0, 2):
        portrayal['Color'] = 'green'

    if isinstance(agent, CoffeMakerAgent):
        portrayal = {"Shape": "rect",
                "Filled": "true",
                "Layer": 0,
                "Color": "black",
                "text": agent.amount
                }
        if agent.amount == 0:
            portrayal["text_color"] = "red"
        else:
            portrayal["text_color"] = "green"

    if isinstance(agent, TVAgent):
        portrayal = {"Shape": "rect",
                "Filled": "false",
                "Layer": 0,
                "Color": "grey"
                }
        if agent.state == True:
             portrayal["Color"] = "yellow"

    if isinstance(agent, AccessAgent):
        portrayal = {"Shape": "rect",
                "Filled": "false",
                "Layer": 0,
                "Color": "black"
                }

    if isinstance(agent, PC):
        portrayal = {"Shape": "rect",
                "Filled": "true",
                "Layer": 0,
                "Color": "black",
                "text": 'PC',
                "text_color": 'blue'
                }

        if agent.state == 'on':
             portrayal["Color"] = "yellow"

        if agent.state == 'standby':
             portrayal["Color"] = "grey"

    return portrayal


grid = DrawLabMapBackEnd(agent_portrayal,  15, 18, 600, 600)

representation = RepresentationModule()

server = ModularServer(LabModel,
                       [grid, representation],
                       "Lab Model",
                       14, 17)

server.port = 8882
server.launch()
