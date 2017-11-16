import operator
import random
from collections import OrderedDict
import datetime
from transitions import Machine
from transitions import State
import datetime
import soba.agents.aStar as aStar
import soba.agents.fov as fov
from soba.agents.behaviourMarkov import Markov
from soba.space.continuousItems import Door

class Agent():

    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model
        self.model.schedule.add(self)

    def step(self):
        pass

class Occupant(Agent):

    def __init__(self, unique_id, model, json, speed = 0.7):
        super().__init__(unique_id, model)

        self.schedule = {}
        for k, v in json['schedule'].items():
            self.schedule[k] = datetime.datetime(2017, 10, 1, int(v[0]+v[1]), int(v[3]+v[4]), int(v[6]+v[7]), 0)
        self.type = json['type']

        self.markovActivity = json['markovActivity']
        self.timeActivity = json['timeActivity']

        self.positionByStateAux = json['states']

        #State machine
        self.positionByState = {}
        self.states = []
        for k, v in json['states'].items():
            name = k
            on_enter = 'start_activity'
            on_exit = 'finish_activity'
            self.states.append(State(name=name, on_enter=[on_enter], on_exit=[on_exit]))
        self.machine = Machine(model=self, states=self.states, initial=list(json['states'].items())[0][0])

        self.triggers = {}
        n_state = 0
        for k, v in json['states'].items():
            name = k
            self.machine.add_transition('setState'+str(n_state), '*', name)
            self.triggers[name] = 'setState'+str(n_state)+'()'
            n_state = n_state + 1

        self.markov_machine = Markov(self)

        self.speed = speed
        self.markov = True
        self.time_activity = 0
        self.lastSchedule = 0.0
        self.N = 0
        self.pos = (0, 0)
        self.pos_to_go = 0
        self.movements = []

        # Methods when entering/exit states
    def start_activity(self):
        self.markov = False
        self.pos_to_go = self.getPlaceToGo()
        if self.pos != self.pos_to_go:
            self.movements = self.getWay()
        else:
            self.movements = [self.pos]
        time_in_state = self.timeActivity[self.getPeriod()][list(self.positionByState.keys()).index(self.state)]
        self.time_activity = (time_in_state*60)/self.model.clock.timeByStep
        self.N = 0

    def finish_activity(self):
        pass

    def changeSchedule(self):
        beh = sorted(self.schedule.items(), key=operator.itemgetter(1))
        nextSchedule = False
        for i in beh:
            a, b = i
            if b < self.model.clock.clock:
                nextSchedule = a
        if nextSchedule != self.lastSchedule:
            self.lastSchedule = nextSchedule
            return True
        else:
            return False

    def getPeriod(self):
        t1 = datetime.datetime(2017, 10, 1, 0, 0, 0, 0)
        t2 = datetime.datetime(2017, 10, 1, 23, 59, 59, 59)
        t1k = 's'
        t2k = 'e'
        schedule = self.schedule
        if 's' in schedule:
            t1 = schedule['s']
        if 'e' in schedule:
            t2 = schedule['e']
        for k, v in schedule.items():
            if((self.model.clock.clock.hour == v.hour and self.model.clock.clock.minute >= v.minute) or (self.model.clock.clock.hour > v.hour)) and ((v.hour > t1.hour) or (v.hour == t1.hour and v.minute >= t1.minute)):
                t1 = v
                t1k = k
            if((v.hour > self.model.clock.clock.hour) or (v.hour == self.model.clock.clock.hour and v.minute > self.model.clock.clock.minute)) and ((t2.hour > v.hour) or (t2.hour == v.hour and t2.minute > v.minute)):
                t2 = v
                t2k = k
        period = t1k + '-' + t2k
        return period

    def step(self):
        pass

class RoomsOccupant(Occupant):

    def __init__(self, unique_id, model, json, speed = 0.7):
        super().__init__(unique_id, model, json, speed)

        #State machine
        for k, v in json['states'].items():
            pos = self.getPosState(k, v)
            self.positionByState[k] = pos

        possible_rooms = []
        roomsNames = self.positionByState[self.state]
        for room in self.model.rooms:
            if isinstance(roomsNames, dict):
                for roomName, v in roomsNames.items():
                    if room.name.split(r".")[0] == roomName:
                        possible_rooms.append(room)
            else:
                if room.name.split(r".")[0] == self.positionByState[self.state]:
                        possible_rooms.append(room)
        if len(possible_rooms) > 1:
            roomaux = random.choice(possible_rooms)
        else:
            roomaux = possible_rooms[0]

        self.model.grid.place_item(self, roomaux.pos)
        self.model.pushAgentRoom(self, roomaux.pos)

        #control
        self.onMyWay1 = False
        self.onMyWay2 = False
        self.costMovementToNewRoom = 0
        self.costMovementInNewRoom = 0
        self.room1 = False
        self.room2 = False

    def getPosState(self, name, posAux): 
        if isinstance(posAux, dict):
            for k, v in posAux.items():
                if v > 0:
                    self.positionByStateAux[name][k]= v - 1
                    return k
        return posAux

    #Movement
    def getWay(self):
        return aStar.getPathRooms(self.model, self.pos, self.pos_to_go)

    def occupantMovePos(self, new_position):
        ux, uy = self.pos
        nx, ny = new_position
        for room in self.model.rooms:
            rx, ry = room.pos
            if room.pos == self.pos:
            #Cost as steps
                if (rx == nx):
                    self.costMovemenToNewRoom = room.dy/2 * (1/self.speed) * (1/self.model.clock.timeByStep)# m * seg/m * step/seg
                if (ry == ny):
                    self.costMovemenToNewRoom = room.dx/2 * (1/self.speed) * (1/self.model.clock.timeByStep)
            if room.pos == new_position:
                if (rx == ux):
                    self.costMovementInNewRoom = room.dy/2 * (1/self.speed) * (1/self.model.clock.timeByStep)
                if (ry == uy):
                    self.costMovementInNewRoom = room.dx/2 * (1/self.speed) * (1/self.model.clock.timeByStep)

    def getPlaceToGo(self):
        pos_to_go = self.pos
        roomsNames = self.positionByState[self.state]
        possible_rooms = []
        for room in self.model.rooms:
            if isinstance(roomsNames, dict):
                for roomName, v in roomsNames.items():
                    if room.name.split(r".")[0] == roomName:
                        possible_rooms.append(room.pos)
            else:
                if room.name.split(r".")[0] == self.positionByState[self.state]:
                        possible_rooms.append(room.pos)
        if len(possible_rooms) > 1:
            pos_to_go = random.choice(possible_rooms)
        else:
            pos_to_go = possible_rooms[0]
        return pos_to_go

    def startActivity(self):
        super.startActivity()

    def step(self):
        print(self.state)
        if self.markov == True or self.changeSchedule():
            self.markov_machine.runStep(self.markovActivity[self.getPeriod()])
        elif self.onMyWay1 == True:
            if self.costMovemenToNewRoom > 0:
                self.costMovemenToNewRoom = self.costMovemenToNewRoom - 1
            else:
                room1 = self.model.getRoom(self.pos)
                room2 = self.model.getRoom(self.movements[self.N])
                self.room1 = room1
                self.room2 = room2
                if room1.name.split(r".")[0] != room2.name.split(r".")[0]:
                    self.model.openDoor(self, room1, room2)
                self.model.popAgentRoom(self, self.pos)
                self.model.grid.move_item(self, self.movements[self.N])
                self.model.pushAgentRoom(self, self.pos)
                self.N = self.N + 1
                self.onMyWay1 = False
                self.onMyWay2 = True
        elif self.onMyWay2 == True:
            if self.costMovementInNewRoom > 0:
                self.costMovementInNewRoom = self.costMovementInNewRoom - 1
            else:
                room1 = self.room1
                room2 = self.room2
                if room1.name.split(r".")[0] != room2.name.split(r".")[0]:
                    self.model.closeDoor(self, room1, room2)
                self.onMyWay2 = False
                self.step()
        elif self.pos != self.pos_to_go:
            self.occupantMovePos(self.movements[self.N])
            self.onMyWay1 = True
            self.step()
        else:
            self.N = 0
            if self.time_activity > 0:
                self.time_activity = self.time_activity - 1
            else:
                self.markov = True


class ContinuousOccupant(Occupant):

    def __init__(self, unique_id, model, json, speed = 0.7):
        super().__init__(unique_id, model, json, speed)

        self.costMovement = 0
        self.collision = True
        self.door = False
        self.door2 = False
        #State machine
        for k, v in json['states'].items():
            pos = self.getPosState(v)
            self.positionByState[k] = pos
        pos = self.positionByState[list(json['states'].items())[0][0]]
        self.model.grid.place_item(self, pos)

    def getPosState(self, name):
        for poi in self.model.pois:
            if poi.id == name and (poi.share == True or  poi.used == False):
                poi.used = True
                return poi.pos

    def startActivity(self):
        super.startActivity()

    def getWay(self, pos = None, pos_to_go = None, other = []):
        posSend = pos
        pos_to_goSend = pos_to_go
        if pos == None:
            posSend = self.pos
        if pos_to_go == None:
            pos_to_goSend = self.pos_to_go
        return aStar.getPathContinuous(self.model, posSend, pos_to_goSend, other)

    def getPlaceToGo(self):
        pos_to_go = self.positionByState[self.state]
        return pos_to_go

    def posInMyFOV(self, pos):
        if pos in self.pov:
            return True
        return False

    def evalCollision(self):
        possibleOccupant = self.model.grid.get_items_in_pos(self.movements[self.N])
        for i in possibleOccupant:
            if isinstance(i, Occupant):
                x1, y1 = self.pos
                x2, y2 = self.movements[self.N]
                nextPos = False
                if x1 == x2:
                    if y2 > y1:
                        nextPos = (x2+1, y2)
                    else:
                        nextPos = (x2-1, y2)
                elif y1 == y2:
                    if x2 > x1:
                        nextPos = (x2, y2-1)
                    else:
                        nextPos = (x2, y2+1)
                else:
                    if x2 > x1 and y2 > y1:
                        nextPos = (x2, y1)
                    elif x1 > x2 and y1 > y2:
                        nextPos = (x2, y1)
                    elif x1 > x2 and y2 > y1:
                        nextPos = (x1, y2)
                    elif x2 > x1 and y1 > y2:
                        nextPos = (x1, y2)
                if aStar.canMovePos(self.model, self.pos, nextPos):
                    self.model.grid.move_item(self, nextPos)
                    self.movements = self.getWay()
                    self.N = 0
                    return True
                else:
                    return True
        return False

    def makeMovement(self):
        if self.costMovement > 1:
            self.costMovement = self.costMovement - 1
        else:
            if not self.evalCollision():
                self.model.grid.move_item(self, self.movements[self.N])
                self.N = self.N+1
                if self.pos != self.pos_to_go:
                    x1, y1 = self.pos
                    x2, y2 = self.movements[self.N]
                    rect = True
                    if x1 != x2 and y1!=y2:
                        rect = False
                    if rect == True:
                        self.costMovement = 0.5/(self.speed*self.model.clock.timeByStep)
                    else:
                        self.costMovement = 0.707/(self.speed*self.model.clock.timeByStep)
                else:
                    self.costMovement = 0.5/(self.speed*self.model.clock.timeByStep)
                self.getFOV()

    def getAsciMap(self):
        asciMapAux = []
        asciMap = []
        for i in range(self.model.height):
            asciMapAux.append([0] * self.model.width)
        for i in range(self.model.height):
            for j in range( self.model.width):
                asciMapAux[i][j] = '.'
        for wall in self.model.walls:
            x, y = wall.block1[0]
            asciMapAux[y][x] = '#'
        for door in self.model.obtacles['doors']:
            x, y = door
            asciMapAux[y][x] = '.'

        string = ''
        for line in asciMapAux:
            for element in line:
                string = string + element
            asciMap.append(string)
            string = ''
        return asciMap

    def getFOV(self):
        asciMap = self.model.asciMap
        if len(asciMap) == 0:
            asciMap = self.getAsciMap()
            self.model.asciMap = asciMap
        fovMap, flag = fov.makeFOV(asciMap, self.pos)
        self.fov = []
        for index1, line in enumerate(fovMap):
            for index2, element in enumerate(line):
                if element == flag:
                    self.fov.append((index2, index1))

    def step(self):
        print(self.state, self.pos, self.pos_to_go, self.unique_id)
        if self.markov == True or self.changeSchedule():
            self.markov_machine.runStep(self.markovActivity[self.getPeriod()])
        elif self.pos != self.pos_to_go:
            self.makeMovement()
        elif self.time_activity > 0:
            self.time_activity = self.time_activity - 1
        else:
            self.markov = True
            self.step()