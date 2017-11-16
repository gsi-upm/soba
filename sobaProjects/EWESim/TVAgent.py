from mesa import Agent, Model
import random


class TVAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = False

    def sensorCheck(self):
        userNear = self.model.ThereIsUserNear(self.pos)
        if (userNear == True):
            actions = self.model.actionsNear
            if actions['channel'] == 'TV' and actions['action'] == 'TurnTVOn':
                self.state = True
        else:
            actions = self.model.actionsFar
            if actions['channel'] == 'TV' and actions['action'] == 'TurnTVOff':
                self.state = False
            self.state = False
            
    def step(self):
    	self.sensorCheck()