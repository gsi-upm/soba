from mesa import Agent, Model
import random

class CoffeMakerAgent(Agent):

    def __init__(self, unique_id, model, capacity=5):
        super().__init__(unique_id, model)
        self.capacity = capacity
        self.amount = capacity
        self.recentUsers = dict()
        self.timeBetweenCoffe = 20

    def sensorCheck(self):
        x, y = self.pos
        userNear = self.model.ThereIsUserDownCM(self.pos)
        if ((len(userNear) > 0) and (self.amount > 0)):
            actions = self.model.actionsNear
            if actions['channel'] == 'CoffeMaker' and actions['action'] == 'MakeCoffe':
                for user in userNear:
                    if (user.unique_id in self.recentUsers) and (self.recentUsers[user.unique_id] == 1):
                        del self.recentUsers[user.unique_id]
                    elif (user.unique_id in self.recentUsers):
                        self.recentUsers[user.unique_id] = self.recentUsers[user.unique_id] - 1
                    else:
                        self.amount  = self.amount - 1
                        self.recentUsers[user.unique_id] = self.timeBetweenCoffe
        else:
            pass
            
    def refill(self):
        self.amount = self.capacity

    def step(self):
        self.sensorCheck()

