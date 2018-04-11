from mesa import Agent, Model

class Time(Agent):

    def __init__(self):

        self.timeByStep = 60 # 0.8 to real simulation
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
        print (self.clock)

    def getCorrectHour(self, hour):
        dec = float('0'+str(hour-int(hour))[1:])
        response = hour
        if dec > 0.59:
            responseH = int(hour) + 1
            responseD = dec - 0.60
            response = responseH + responseD
        return round(response,2)