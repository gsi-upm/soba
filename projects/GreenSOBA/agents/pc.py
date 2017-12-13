from mesa import Agent, Model
from transitions import Machine
from transitions import State
import json
import configuration.settings

class PC(Agent):

    states = [
        State(name='off', on_enter=['set_off']),
        State(name='on', on_enter=['set_on']),
        State(name='standby', on_enter=['set_standby'])
        ]

    def __init__(self, unique_id, model, room):
        super().__init__(unique_id, model)

        self.room = room
        self.owner = False
        self.states_when_is_used = []

        self.consumeOn = configuration.settings.consume_pc_on
        self.consumeStandby = configuration.settings.consume_pc_standby 

        self.wait_off = int(configuration.settings.time_to_off_PC_from_standby * 60 * 100 /configuration.settings.time_by_step)
        self.wait_standby = int(configuration.settings.time_to_standby_PC_from_on * 60 * 100 /configuration.settings.time_by_step)

        self.count_down_without_usage = int(configuration.settings.time_to_set_standby_pc_from_on_whitout_usage * 60 * 100 /configuration.settings.time_by_step)

        self.machine = Machine(model=self, states=PC.states, initial='off')
        self.machine.add_transition('turn_on', '*', 'on')
        self.machine.add_transition('turn_standby', '*', 'standby')
        self.machine.add_transition('turn_off', '*', 'off')

    def sensorCheck(self):
        userNear = self.model.thereIsOccupantInRoom(self.room, self.owner)
        if userNear == True:
            if self.state == 'on':
                return
            else:
                self.turn_on()
        else:
            if self.state == 'on':    
                if self.wait_standby > 0:
                    self.wait_standby = self.wait_standby - 1
                else:
                    self.turn_standby()
                    self.wait_standby = int(configuration.settings.time_to_standby_PC_from_on * 60 * 100 /configuration.settings.time_by_step)
                
            elif self.state == 'standby':
                if self.wait_off > 0:
                    self.wait_off = self.wait_off - 1
                else:
                    self.turn_off()
                    self.wait_off = int(configuration.settings.time_to_off_PC_from_standby * 60 * 100 /configuration.settings.time_by_step)
            else:
                return

    def regularBehaviour(self):
        userNear = self.model.thereIsOccupantInRoom(self.room, self.owner)
        if userNear == True:
            if self.state == 'on':
                return
            else:
                self.turn_on()
        else:
            if self.state == 'on':
                if self.count_down_without_usage > 0:
                    self.count_down_without_usage = self.count_down_without_usage - 1
                else:
                    self.count_down_without_usage = configuration.settings.time_to_set_standby_pc_from_on_whitout_usage
                    self.turn_standby()
            else:
                pass
                
    def step(self):
        #print('pc: ', self.unique_id, self.state, self.room)
        self.model.consumeEnergy(self)
        if (self.model.modelWay != 0):
            self.sensorCheck()
        else:
            self.regularBehaviour()

    def set_off(self):
        pass

    def set_on(self):
        pass

    def set_standby(self):
        pass