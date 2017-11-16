from mesa import Agent, Model
from mesa.time import BaseScheduler
import random
from UserAgent import UserAgent
from CoffeMakerAgent import CoffeMakerAgent 
from TVAgent import TVAgent
from AccessAgent import AccessAgent
from mesa.space import MultiGrid
from mesa.space import ContinuousSpace
from collections import defaultdict
from Wall import Wall
from Door import Door
from LightBulb import Bulb
from PC import PC
from Room import Room
import post
from Time import Time
import defineAgents

class LabModel(Model):

    def __init__(self, width, height):

        defineAgents.init()

        self.num_Users = 0
        self.schedule = BaseScheduler(self)
        self.running = True
        self.grid = MultiGrid(width, height, False)

        self.agents_json = []

        self.clock = Time()
        self.day = self.clock.day

        self.NStep = 0
        self.createWalls(width, height)
        self.createDoors(width, height)
        self.savePosOutOfMap()
        self.setRooms()
        self.setAgents()

        self.getRules()


    def getRules(self):
        listdata1 = post.getEvents(0)
        self.actionsNear = listdata1[0]
        print('Near actions: ', self.actionsNear)
        listdata2 = post.getEvents(2)
        self.actionsFar = listdata2[0]
        print('Far actions: ', self.actionsFar)
        
    def createWalls(self, width, height):
        self.Walls = []
        for y in range(int(height*0.2),height):
            x = width
            wall = Wall(x, y)
            self.Walls.append(wall)
        for x in range(0,int(width/2)):
            y = 0
            wall = Wall(x,y)
            self.Walls.append(wall)
        for x in range(0,width):
            y = height*0.2
            wall = Wall(x,y)
            self.Walls.append(wall)
        for y in range(0,height+1):
            x = 0
            wall = Wall(x,y)
            self.Walls.append(wall)
        for y in range(0, height+1):
            x = width/2
            wall = Wall(x,y)
            self.Walls.append(wall)
        for x in range(int(width/2), width):
            y = height* 0.6
            wall = Wall(x,y)
            self.Walls.append(wall)
        for x in range(0, width):
            y = height
            wall = Wall(x,y)
            self.Walls.append(wall)

    def createDoors(self, width, height):
        door1 = Door(0,2,False, True)
        door2 = Door(4,3, True)
        door3 = Door(7,8)
        door4 = Door(7,12)
        self.doors = [door1, door2, door3, door4]
        # Clean positions of doors
        for wall in self.Walls:
            for door in self.doors:
                if ((wall.x == door.x) and (wall.y == door.y )):
                    self.Walls.remove(wall)

    def savePosOutOfMap(self):
        self.pos_out_of_map = []
        for x in range(8,15):
            for y in range(0,3):
                pos = (x,y)
                self.pos_out_of_map.append(pos)

    def setRooms(self):
        positions_room_out = []
        positions_room_out.append((self.doors[0].x, self.doors[0].y)) #I understand that door 1 is out of the laboratory
        self.roomOut = Room(positions_room_out)
        positions_room1 = []
        for x in range(1,7):
            for y in range(1,3):
                pos = (x, y)
                positions_room1.append(pos)
        room1 = Room(positions_room1)
        positions_room2 = []
        for x in range(1,7):
            for y in range(4,17):
                pos = (x, y)
                positions_room2.append(pos)
        positions_room2.append((self.doors[1].x, self.doors[1].y))
        room2 = Room(positions_room2)
        positions_room3 = []
        for x in range(8,14):
            for y in range(4,10):
                pos = (x, y)
                positions_room3.append(pos)
        positions_room2.append((self.doors[2].x, self.doors[2].y))
        room3 = Room(positions_room3)
        positions_room4 = []
        for x in range(8,14):
            for y in range(11,17):
                pos = (x, y)
                positions_room4.append(pos)
        positions_room2.append((self.doors[3].x, self.doors[3].y))
        room4 = Room(positions_room4)
        self.rooms = [room1, room2, room3, room4, self.roomOut]

    def isInMap(self, possible_steps_out_of_map):
        possible_step = possible_steps_out_of_map
        for each_pos in self.pos_out_of_map:
            xp, yp = each_pos
            xu, yu = possible_step
            if ((xp == xu) and (yp == yu)):
                return False
        return True

    def thereIsPC(self, pos):
        x,y = pos
        for pc in self.workplaces:
            if pc.x == x and pc.y == y:
                return True
        return False        

    def thereIsWall(self, possible_steps_before_walls):
        possible_step = possible_steps_before_walls
        for each_wall in self.Walls:
            xw = each_wall.x
            yw = each_wall.y
            xu, yu = possible_step
            if ((xw == xu) and (yw == yu)):
                return True
        return False

    def thereIsClosedDoor(self, possible_steps_before_doors):
        xu,yu = possible_steps_before_doors
        for door in self.doors:
            if ((xu == door.x) and (yu == door.y)):
                if door.state == False:
                    return True
        return False

    def ThereIsUserInRoom(self, room):
        for pos in room.pos_room:
            possible_user = self.grid.get_cell_list_contents([pos])
            if (len(possible_user) > 0):
                for user in possible_user:
                    if isinstance(user,UserAgent):
                        return True
        return False

    def setAgents(self):
        # Identifications
        id_offset = 100

        id_sensorCoffe = self.num_Users + id_offset
        id_sensorTV = id_sensorCoffe + id_offset
        id_sensorAccess = id_sensorTV + id_offset
        id_bulb = id_sensorAccess + id_offset
        id_pc = id_sensorAccess + id_bulb

        # Height and Width
        height = self.grid.height
        width = self.grid.width

        # CREATE AGENT 

        # Create Coffe Maker
        capacity_coffeMaker = 30
        self.cm = CoffeMakerAgent(id_sensorCoffe, self, capacity_coffeMaker)
        self.grid.place_agent(self.cm, (1, height-1))
        # Create TV
        self.tv = TVAgent(id_sensorTV, self)
        self.grid.place_agent(self.tv, (4,height-1))
        # Create Control Access
        self.ca = AccessAgent(id_sensorAccess, self, self.doors[1])
        self.grid.place_agent(self.ca, (2, 3))
        # Create LightBulbs
        self.bulbs = []
        LB1 = Bulb(id_bulb, self, self.rooms[0])
        self.bulbs.append(LB1)
        LB2 = Bulb(id_bulb+1, self, self.rooms[1])
        self.bulbs.append(LB2)
        LB3 = Bulb(id_bulb+2, self, self.rooms[2])
        self.bulbs.append(LB3)
        LB4 = Bulb(id_bulb+3, self, self.rooms[3])
        self.bulbs.append(LB4)
        # Create PC
        self.workplaces = []
        PC1 = PC(id_pc, self, 9, 6, 'd')
        self.grid.place_agent(PC1, (9, 6))
        self.workplaces.append(PC1)
        PC2 = PC(id_pc+1, self, 11, 6, 'd')
        self.grid.place_agent(PC2, (11, 6))
        self.workplaces.append(PC2)
        PC3 = PC(id_pc+2, self, 12, 6, 'd')
        self.grid.place_agent(PC3, (12, 6))
        self.workplaces.append(PC3)
        PC4 = PC(id_pc+3, self, 11, 7, 'u')
        self.grid.place_agent(PC4, (11, 7))
        self.workplaces.append(PC4)
        PC5 = PC(id_pc+4, self, 12, 7, 'u')
        self.grid.place_agent(PC5, (12, 7))
        self.workplaces.append(PC5)
        PC6 = PC(id_pc+5, self, 9, 14, 'd')
        self.grid.place_agent(PC6, (9, 14))
        self.workplaces.append(PC6)
        PC7 = PC(id_pc+6, self, 11, 14, 'u')
        self.grid.place_agent(PC7, (11, 14))
        self.workplaces.append(PC7)
        PC8 = PC(id_pc+7, self, 12, 14, 'u')
        self.grid.place_agent(PC8, (12, 14))
        self.workplaces.append(PC8)
        PC9 = PC(id_pc+8, self, 11, 13, 'd')
        self.grid.place_agent(PC9, (11, 13))
        self.workplaces.append(PC9)
        PC10 = PC(id_pc+9, self, 12, 13, 'd')
        self.grid.place_agent(PC10, (12, 13))
        self.workplaces.append(PC10)

        def getFreePlace():
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            position = (x,y)
            possible_free_place = self.grid.get_cell_list_contents([position])
            if len(possible_free_place) == 0:
                there_is_wall = self.thereIsWall(position)
                if there_is_wall == False:
                    place_in_map = self.isInMap(position)
                    if place_in_map == True:
                        return position
            return getFreePlace()

         # Create users
        countPC = 0
        for n_type_users in defineAgents.agents_json:
            n_agents = n_type_users['N']
            for i in range(0, n_agents):
                a = UserAgent(i, self, self.workplaces[countPC], n_type_users)
                self.schedule.add(a)
                self.grid.place_agent(a, (0, 2))
                countPC = countPC + 1

        #Add to schedule
        for pc in self.workplaces:
            self.schedule.add(pc)
        for bulb in self.bulbs:
            self.schedule.add(bulb)
        self.schedule.add(self.cm)
        self.schedule.add(self.tv)
        self.schedule.add(self.ca)
        self.schedule.add(self.clock)

    def createAgent(self, pos):
        if self.thereIsUser((0,2)) == False:
            self.num_Users = self.num_Users + 1
            a = UserAgent(self.num_Users - 1, self, self.workplaces[self.num_Users - 1])
            self.schedule.add(a)
            #x, y = getFreePlace()
            self.grid.place_agent(a, (0, 2))

    def ThereIsUserNear(self, pos):
        xa, ya = pos
        round_pos = []
        round_pos.append((xa-1,ya-1))
        round_pos.append((xa-1,ya))
        round_pos.append((xa-1,ya+1)) 
        round_pos.append((xa+1,ya+1))
        round_pos.append((xa,ya+1))
        round_pos.append((xa,ya-1))
        round_pos.append((xa+1,ya))
        round_pos.append((xa+1,ya-1))
        for pos in round_pos:
            xp, yp = pos
            if (xp>=0 and yp>=0 and yp < self.grid.height and xp < self.grid.width):
                possible_user = self.grid.get_cell_list_contents([pos])
                if (len(possible_user) > 0):
                    for user in possible_user:
                        if isinstance(user,UserAgent):
                            return True
                        else:
                            continue
            else:
                continue
        return False

    def ThereIsUserUp(self, pos, id_pc):
        xa, ya = pos
        possible_user = self.grid.get_cell_list_contents([(xa,ya+1)])
        if (len(possible_user) > 0):
                for user in possible_user:
                    if isinstance(user,UserAgent) and user.pc.unique_id == id_pc:
                        return True
        return False

    def ThereIsUserDown(self, pos, id_pc):
        xa, ya = pos
        possible_user = self.grid.get_cell_list_contents([(xa,ya-1)])
        if (len(possible_user) > 0):
            for user in possible_user:
                if isinstance(user,UserAgent) and user.pc.unique_id == id_pc:
                    return True
        return False

    def ThereIsUserDownCM(self, pos):
        xa, ya = pos
        agents = []
        possible_user = self.grid.get_cell_list_contents([(xa,ya-1)])
        if (len(possible_user) > 0):
            for user in possible_user:
                if isinstance(user,UserAgent):
                    agents.append(user)
        return agents

    def thereIsUser(self,pos):
        possible_user = self.grid.get_cell_list_contents([pos])
        if (len(possible_user) > 0):
            for user in possible_user:
                if isinstance(user,UserAgent):
                    return True
        return False

    def ThereIsOtherUserInRoom(self, room, agent):
        for pos in room.pos_room:
            possible_user = self.grid.get_cell_list_contents([pos])
            if (len(possible_user) > 0):
                for user in possible_user:
                    if isinstance(user,UserAgent) and user != agent:
                        return True
        return False

    def getRoom(self, pos):
        for room in self.rooms:
            if pos in room.pos_room:
                return room
        return False

    def getLightWithRoom(self, room):
        for light in self.bulbs:
            if light.room == room:
                return light
        return False
        
    def openDoor(self,pos,agent = 0):
        x_pos, y_pos = pos
        doors = self.doors
        for door in doors:
            x = door.x
            y = door.y
            if ((x == x_pos) and (y == y_pos)):
                if isinstance(agent, AccessAgent):
                    door.open(True)
                else:
                    door.open()

    def closeDoor(self,pos):
        x_pos, y_pos = pos
        doors = self.doors
        for door in doors:
            x = door.x
            y = door.y
            if ((x == x_pos) and (y == y_pos)):
                door.close()

    def getMatrix(self,agent):
        new_matrix = defineAgents.returnMatrix(agent, self.clock.clock)
        agent.markov_matrix = new_matrix
    
    def getTimeInState(self, agent):
        matrix_time_in_state = defineAgents.getTimeInState(agent, self.clock.clock)
        return matrix_time_in_state

    def step(self):
        self.schedule.step()
        self.NStep = self.NStep + 1