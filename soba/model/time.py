import random
import datetime
from soba.agents.agent import Agent

class Clock(Agent):

    def __init__(self, model, timeByStep = 30, day = 1, hour = 0, minute = 0, seg = 50, microsecond = 0):
        super().__init__(100000, model)
        self.timeByStep = timeByStep
        self.day = day
        self.clock = datetime.datetime(2017, 10, day, hour, minute, seg, microsecond)

    def step(self):
        self.clock = self.clock + datetime.timedelta(seconds = self.timeByStep)
        print(self.clock.strftime("%d:%H:%M:%S"))

    def increaseTime(self, clockOld, day=0, hour=0, minute=0, second=0, microsecond = 0):
        clockNew = clockOld + datetime.timedelta(0, 0, day, hour, minute, second, microsecond)
        return clockNew

    def decreaseTime(self, clockOld, day=0, hour=0, minute=0, second=0, microsecond = 0):
        clockNew = clockOld - datetime.timedelta(0, 0, day, hour, minute, second, microsecond)
        return clockNew

class BaseScheduler():
    model = None
    steps = 0
    time = 0
    agents = []

    def __init__(self, model):
        self.model = model
        self.steps = 0
        self.time = 0
        self.agents = []

    def add(self, agent):
        self.agents.append(agent)

    def remove(self, agent):
        while agent in self.agents:
            self.agents.remove(agent)

    def step(self):
        for agent in self.agents:
            agent.step()
        self.steps += 1
        self.time += 1

    def get_agent_count(self):
        return len(self.agents)

class RandomActivation(BaseScheduler):
    def step(self):
        random.shuffle(self.agents)
        for agent in self.agents:
            agent.step()
        self.steps += 1
        self.time += 1

'''
class Clock(Agent):

    def __init__(self, time_by_step = 60):
        self.timeByStep = time_by_step
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.seg = 0
        self.clock = 00.00

    def step(self):
        self.seg = self.seg + self.timeByStep
        if self.seg > 59:
            self.seg = self.seg - 60
            self.minute = self.minute + 1
            if self.minute > 59:
                self.minute = self.minute - 60
                self.hour = self.hour + 1
                if self.hour > 23:
                    self.hour = self.hour - 24
                    self.day = self.day + 1
        self.clock = (self.hour*100 + self.minute) / 100
        print('Day: ', (self.day + 1), ' - Hour: ', self.clock)

    def getCorrectHour(self, hour):
        dec = float('0'+str(hour-int(hour))[1:])
        response = hour
        if dec > 0.59:
            responseH = int(hour) + 1
            responseD = dec - 0.60
            response = responseH + responseD
        return round(response,2)

    def getDownCorrectHour(self, hour):
        dec = float('0'+str(hour-int(hour))[1:])
        response = hour
        if dec > 0.59:
            responseH = int(hour)
            responseD = dec - 0.40
            response = responseH + responseD
        return round(response,2)

    def getMinuteFromHours(self, hour):
        dec = float('0'+str(hour-int(hour))[1:])
        uni = float(int(hour))
        minutes = dec*100 + uni*60
        return minutes
'''