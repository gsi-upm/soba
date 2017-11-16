from mesa import Agent, Model
from transitions import Machine
from transitions import State
import post

class PC(Agent):

    states = [
        State(name='off', on_enter=['set_off']),
        State(name='on', on_enter=['set_on']),
        State(name='standby', on_enter=['set_standby'])
        ]

    def __init__(self, unique_id, model, x, y, downUp):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.down_up = downUp

        self.machine = Machine(model=self, states=PC.states, initial='off')
        self.machine.add_transition('turn_on', '*', 'on')
        self.machine.add_transition('turn_standby', 'on', 'standby')
        self.machine.add_transition('turn_off', '*', 'off')

    def sensorCheck(self):
        if(self.down_up == 'u'):
            userNear = self.model.ThereIsUserUp((self.x, self.y), self.unique_id)
        else:
            userNear = self.model.ThereIsUserDown((self.x, self.y), self.unique_id)
        if userNear == True:
            if self.state == 'on':
                pass
            else:
                actions = self.model.actionsNear
                if actions['channel'] == 'PCOff' and actions['action'] == 'TurnOnPC':
                    self.turn_on()
        else:
            if self.state == 'on':
                actions = self.model.actionsFar
                if actions['channel'] == 'PCOn' and actions['action'] == 'TurnStandbyPC':
                    self.turn_standby()
                if actions['channel'] == 'PCOn' and actions['action'] == 'TurnOffPC':
                    self.turn_off()
            else:
                pass
                
    def step(self):
        self.sensorCheck()

    def set_off(self):
        pass

    def set_on(self):
        pass

    def set_standby(self):
        pass