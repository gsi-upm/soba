from mesa import Agent, Model
import random

class AccessAgent(Agent):

    def __init__(self, unique_id, model, associated_door):
        super().__init__(unique_id, model)
        self.door = associated_door

    def sensorCheck(self):
    	userNear = self.model.ThereIsUserNear(self.pos)
    	if (userNear == True):
            actions = self.model.actionsNear
            if actions['channel'] == 'AccessAgent' and actions['action'] == 'OpenDoor':
                self.model.openDoor((self.door.x, self.door.y), self)
    	else:
    		pass

    def step(self):
        self.sensorCheck()