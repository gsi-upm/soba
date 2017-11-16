from transitions import Machine
from mesa import Agent, Model
from transitions import State

class Bulb(Agent):

    states = [
        State(name='off', on_enter=['set_off']),
        State(name='on', on_enter=['set_on'])
        ]

    def __init__(self, unique_id, model, room):
        super().__init__(unique_id, model)
        self.room = room        
        self.machine = Machine(model=self, states=Bulb.states, initial='off')

        self.machine.add_transition('switch_on', '*', 'on')
        self.machine.add_transition('switch_off', '*', 'off')

    def sensorCheck(self):
        userInRoom = self.model.ThereIsUserInRoom(self.room)
        if userInRoom == True:
            if self.state == 'on':
                pass
            else:
                actions = self.model.actionsNear
                if actions['channel'] == 'Bulb' and actions['action'] == 'SwitchOn':
                    self.switch_on()
        else:
            if self.state == 'off':
                pass
            else:
                actions = self.model.actionsFar
                if actions['channel'] == 'Bulb' and actions['action'] == 'SwitchOff':
                    self.switch_off()
                else:
                    pass
                    
    def step(self):
        print(self.unique_id, self.state)
        self.sensorCheck()

    def set_off(self):
        pass
    def set_on(self):
        pass
