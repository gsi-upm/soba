import random
import datetime
from soba.agents.agent import Agent

class Time(Agent):

    def __init__(self, model, timeByStep = 1, day = 1, hour = 7, minute = 0, seg = 0, microsecond = 0):
        super().__init__(100000, model)

        self.timeByStep = timeByStep

        today = datetime.date.today()
        self.startDay = datetime.datetime(today.year, today.month, day, hour, minute, seg, microsecond)
        self.endDay = datetime.datetime(today.year, today.month, 1, 20, 0, 0, 0)

        self.clock = self.startDay

    def step(self):
        self.clock = self.increaseTime(self.timeByStep)
        print(self.clock.strftime("%d:%H:%M:%S"))

    def increaseTime(self, seconds=0, days=0, hours=0, minutes=0, microseconds=0):
        clockOld = self.clock
        dayOld = clockOld.day
        clockNew = clockOld + datetime.timedelta(days=days, minutes=minutes, seconds=seconds, microseconds=microseconds)
        if clockNew.hour >= self.endDay.hour and clockNew.minute > self.endDay.minute:
            clockNew = datetime.datetime(2107, 1, dayOld+1, self.startDay.hour, self.startDay.minute, 0, 0)
            + (clockNew - self.endDay)
        return clockNew

    def decreaseTime(self, days=0, hours=0, minutes=0, seconds=0, microseconds=0):
        clockOld = self.clock
        clockNew = clockOld - datetime.timedelta(days=days, minutes=minutes, seconds=seconds, microseconds=microseconds)
        return clockNew

# Activation with defined order of the agents
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

    def getAgentCount(self):
        return len(self.agents)

# Activation with random order of the agents
class RandomActivation(BaseScheduler):
    def step(self):
        random.shuffle(self.agents)
        for agent in self.agents:
            agent.step()
        self.steps += 1
        self.time += 1