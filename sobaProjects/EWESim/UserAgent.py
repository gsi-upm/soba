from mesa import Agent, Model
from transitions import Machine
from transitions import State
from behaviourMarkov import Markov
import random
from AStar import AStar

class UserAgent(Agent):

    def __init__(self, unique_id, model, workplace, json):
        super().__init__(unique_id, model)

        self.pc = workplace
        if self.pc.down_up == 'u':
            self.workspace_pos = (self.pc.x, self.pc.y+1)
        else: 
            self.workspace_pos =  (self.pc.x, self.pc.y-1)
        self.type = json['type']
        self.behaviour = json['lifeWay']
        self.positionByState = {}

        #State machine
        states = []
        for state in json['states']:
            name = state['name']
            pos = state['position']
            on_enter = 'start_activity'
            on_exit = 'pass_method'
            self.positionByState[name] =  pos
            states.append(State(name=name, on_enter=[on_enter], on_exit=[on_exit]))

        self.machine = Machine(model=self, states=states, initial=states[0].name)
        
        self.triggers = {}
        n_state = 0
        for state in json['states']:
            name = state['name']
            self.machine.add_transition('setState'+str(n_state), '*', name)
            self.triggers[name] = 'setState'+str(n_state)+'()'
            n_state = n_state + 1

        self.markov_matrix = json['matrix']
        self.markov_machine = Markov(self)

        #control
        self.markov = True
        self.in_room = False
        self.time_activity = 0
        self.place_to_go = (0, 2)
        self.movements = []
        self.N = 0
        self.opened_door1 = False
        self.opened_door2 = False
        self.currentRoom = self.model.roomOut

    # Methods when entering/exit states

    def start_activity(self):
        self.markov = False
        self.place_to_go = self.getPlaceToGo()
        self.movements = AStar(self, self.pos, self.place_to_go).process()
        time_in_state = self.model.getTimeInState(self)[list(self.positionByState.keys()).index(self.state)]
        self.time_activity = int(time_in_state*60*100 /self.model.clock.timeByStep)

    def pass_method(self):
        pass

    # Movement
        #Random
    def getNewPosition(self,possible_steps):
        possible_steps_aux = possible_steps
        new_position = random.choice(possible_steps)
        is_wall = self.model.thereIsWall(new_position)
        if is_wall == False:
            is_closed_door = self.model.thereIsClosedDoor(new_position)
            if is_closed_door == False:
                if self.opened_door2 == True:
                    self.model.closeDoor(self.door_position)
                    self.opened_door2 = False
                    return new_position
                elif self.opened_door1 == True:
                    self.opened_door2 = True
                    self.opened_door1 = False
                    return self.door_position
                else:
                    return new_position
            else:
                self.model.openDoor(new_position)
                self.opened_door1 = True
                self.door_position = new_position
                self.N = self.N - 1
                return self.pos
        if len(possible_steps_aux)> 1:
            possible_steps_aux.remove(new_position)
            return self.getNewPosition(possible_steps_aux)
        else:
            self.N =self.N - 1 
            return self.pos
        #Random
    def userMoveRandom(self, pos):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        position_to_move = self.getNewPosition(possible_steps)
        if position_to_move == False:
            pass
        else:
            self.model.grid.move_agent(self, position_to_move)

        #AStar
    def userMovePos(self, new_position):
        is_closed_door = self.model.thereIsClosedDoor(new_position)
        if is_closed_door == False:
            if self.opened_door2 == True:
                self.model.closeDoor(self.door_position)
                self.opened_door2 = False
                self.model.grid.move_agent(self, new_position)
            elif self.opened_door1 == True:
                self.opened_door2 = True
                self.opened_door1 = False
                self.model.grid.move_agent(self, self.door_position)
            else:
                self.model.grid.move_agent(self, new_position)
        else:
            self.model.openDoor(new_position)
            self.opened_door1 = True
            self.door_position = new_position
            self.N = self.N - 1
            self.model.grid.move_agent(self, self.pos)

    def getPlaceToGo(self):
        place_to_go = self.positionByState[self.state]
        if place_to_go == 'workspace':
            return self.workspace_pos
        elif place_to_go == 'coffeMaker':
            x ,y = self.model.cm.pos
            cmPosUse = (x, y-1)
            return cmPosUse
        elif place_to_go == 'outOffice':
            return (0, 2)
        elif type(place_to_go) is type(self.pos):
            return place_to_go
        else:
            return self.pos

    # Step from mesa
    def step(self):
        print(self.state)
        self.model.getMatrix(self)
        if self.markov == True:
            self.markov_machine.runStep(self.markov_matrix)
            return
        elif self.pos != self.place_to_go:
            self.userMovePos(self.movements[self.N])
            self.N = self.N + 1
        else:
            self.N = 0
            if self.time_activity > 0:
                self.time_activity = self.time_activity - 1
            else:
                self.markov = True
                self.step()