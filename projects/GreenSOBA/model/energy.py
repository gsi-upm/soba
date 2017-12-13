import configuration.settings

class Energy():

    def __init__(self):
    
        #init
        self.time = configuration.settings.time_by_step

            #Energy - kW
        #Control
        self.energyByStepPCs = []
        self.energyByStepLights = []
        self.energyByStepHVACs = []

        self.lastStep = 0

        #Results
        self.energyByStepPCsTotal = []
        self.energyByStepLightsTotal = []
        self.energyByStepLPCTotal = []
        self.energyByStepHVACsTotal = []

        self.energyByStepTotal = []

        self.energyByDayPC = []
        self.energyByDayLight = []
        self.energyByDayLPC = []
        self.energyByDayHVAC =  []

        self.energyByDayTotal = []

        self.energyByWeekPC = 0
        self.energyByWeekLight = 0
        self.energyByWeekHVAC = 0

        self.energyTotalWeek = 0

    def consumeEnergyAppliance(self, appliance, consume):
        if appliance == 'PC':
            self.energyByStepPCs.append(consume*self.time/3600)
        elif appliance == 'Light':
            self.energyByStepLights.append(consume*self.time/3600)
        elif appliance == 'HVAC':
            self.energyByStepHVACs.append(consume*self.time/3600)
        else:
            pass

    def finalStep(self):
        valuePC = 0
        for consume in self.energyByStepPCs:
            valuePC = valuePC + consume
        self.energyByStepPCsTotal.append(valuePC)
        self.energyByStepPCs = []
        valueLight = 0
        for consume in self.energyByStepLights:
            valueLight = valueLight + consume
        self.energyByStepLightsTotal.append(valueLight)
        self.energyByStepLights = []
        self.energyByStepLPCTotal.append(valuePC + valueLight)
        valueHVAC = 0
        for consume in self.energyByStepHVACs:
            valueHVAC = valueHVAC + consume
        self.energyByStepHVACsTotal.append(valueHVAC)
        self.energyByStepHVACs = []
        self.energyByStepTotal.append(valueLight + valuePC + valueHVAC)

    def finalDay(self, NStep):
        energyDayPC = 0
        energyDayLight = 0
        energyDayHVAC = 0
        energyDayTotal = 0
        for i in range(self.lastStep, NStep):
            energyDayPC = energyDayPC + self.energyByStepPCsTotal[i]
            energyDayLight = energyDayLight + self.energyByStepLightsTotal[i]
            energyDayHVAC = energyDayHVAC + self.energyByStepHVACsTotal[i]
            energyDayTotal = energyDayTotal + self.energyByStepTotal[i]
        self.energyByDayPC.append(energyDayPC)
        self.energyByDayLight.append(energyDayLight)
        self.energyByDayLPC.append(energyDayPC+energyDayLight)
        self.energyByDayHVAC.append(energyDayHVAC)
        self.energyByDayTotal.append(energyDayTotal)
        self.lastStep = NStep

    def finalWeek(self):
        for i in range(0, 5):
            self.energyByWeekPC = self.energyByWeekPC + self.energyByDayPC[i]
            self.energyByWeekLight = self.energyByWeekLight + self.energyByDayLight[i]
            self.energyTotalWeek = self.energyTotalWeek + self.energyByDayTotal[i]