from collections import defaultdict
from mesa.visualization.ModularVisualization import VisualizationElement
from model.model import SOBAModel
import numpy as np
from agents.occupant import Occupant

class MapVisualization(VisualizationElement):
 
    local_includes = ["drawModelFront.js"]
    package_includes = ["Chart.min.js"]

    portrayal_method = None  # Portrayal function
    canvas_width = 500
    canvas_height = 500

    def __init__(self, portrayal_method,  cellW, cellH,canvas_width=500, canvas_height=500):
        self.portrayal_method = portrayal_method
        self.grid_width = cellW
        self.grid_height = cellH
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        new_element = ("new CanvasModule({}, {}, {}, {})"
            .format(self.canvas_width, self.canvas_height,
                self.grid_width, self.grid_height ))

        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        grid_state = defaultdict(list)
        for x in range(model.grid.width):
            for y in range(model.grid.height):
                cell_objects = model.grid.get_cell_list_contents([(x, y)])
                for obj in cell_objects:
                    if isinstance(obj, Occupant):
                        portrayal = self.portrayal_method(obj)
                        if portrayal:
                            portrayal["x"] = x
                            portrayal["y"] = y
                            grid_state[portrayal["Layer"]].append(portrayal)

        offSet_Rooms = 10
        roomsSends = []
        for room in model.rooms:
            send = False
            for roomAux in roomsSends:
                if (roomAux.name.split(r".")[0] == room.name.split(r".")[0]):
                    send = True
            if send == False:

                nAgents = 0
                for room2 in model.rooms:
                     if (room2.name.split(r".")[0] == room.name.split(r".")[0]):
                        nAgents = nAgents + len(room2.agentsInRoom)

                nPcsOn = 0
                for room2 in model.rooms:
                     if (room2.name.split(r".")[0] == room.name.split(r".")[0]):
                        for pc2 in room2.PCs:
                            if pc2.state == 'on' or pc2.state == 'standby':
                                nPcsOn = nPcsOn + 1

                x, y = room.pos

                JSON_room = {"x":x,
                             "y": y,
                             "nAgents": nAgents,
                             "perAgents": int((nAgents/model.num_occupants)* 100),
                             "name": room.name.split(r".")[0],
                             "text": room.name.split(r".")[0],
                             "type": room.typeRoom,
                }
                if room.typeRoom != 'out' and room.typeRoom != 'restroom':
                    JSON_room["TZ"] = room.thermalZone.name
                    JSON_room["tra"] = int(room.thermalZone.temperature*10)/10
                    JSON_room["light"] = room.light.state
                    JSON_room["pc"] = nPcsOn
                    JSON_room["hvac"] = room.thermalZone.hvac.state
                    if room.thermalZone.hvac != False:
                        JSON_room["fanger"] = int(room.thermalZone.hvac.fangerValue)
                        JSON_room["comfort"] = int(room.thermalZone.hvac.comfortMedium)
                    else:
                        JSON_room["comfort"] = ''
                        JSON_room["fanger"] = ''
                else:
                    JSON_room["pc"] = ''
                    JSON_room["TZ"] =''
                    JSON_room["tra"] = ''
                    JSON_room["comfort"] = ''
                    JSON_room["fanger"] = ''
                    JSON_room["hvac"] = ''
                grid_state[offSet_Rooms].append(JSON_room)
                roomsSends.append(room)
            else:
                x, y = room.pos
                JSON_room = {"x":x,
                             "y": y,
                             "nAgents":'',
                             "perAgents": '',
                             "name": room.name.split(r".")[0],
                             "text": '',
                             "tra": '',
                             "comfort": '',
                             "type": room.typeRoom
                }
                JSON_room["TZ"] = ''
                JSON_room["hvac"] = ''
                JSON_room["fanger"] = ''
                JSON_room["pc"] = ''
                grid_state[offSet_Rooms].append(JSON_room)


        offSet_Doors = offSet_Rooms + 10
        for door in model.doors:
            x1, y1 = door.room1.pos
            x2, y2 = door.room2.pos
            JSON_Door = {"x1": x1,
                         "y1": y1,
                         "x2": x2,
                         "y2": y2,
                         "state": door.state
            }
            grid_state[offSet_Doors].append(JSON_Door)
        return grid_state

class GraphVisualization(VisualizationElement):

    package_includes = ["Chart.min.js"]
    local_includes = ["visualization/drawModelFront.js", "lib/canvasjs.min.js"]

    def __init__(self):
        new_element = "new GraphVisualization()"
        new_element = new_element.format()
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        data = []
        energy = 0
        clock = 0
        ePCByDay = [0, 0, 0, 0, 0]
        eLightByDay = [0, 0, 0, 0, 0]
        eHVACByDay = [0, 0, 0, 0, 0]
        ePCTotal = 0
        eLightTotal = 0
        eHVACTotal = 0
        day = model.clock.day

        if model.NStep != 0:
            energyPCLight = model.energy.energyByStepPCsTotal[model.NStep - 1] + model.energy.energyByStepLightsTotal[model.NStep - 1]
            energyHVAC = model.energy.energyByStepHVACsTotal[model.NStep - 1]
            energy = energyHVAC + energyPCLight
            clock = model.clock.clock

        if day != 0 and 5>day:
            for n in range(0, day):
                ePCByDay.insert(n, model.energy.energyByDayPC[n])
                eLightByDay.insert(n, model.energy.energyByDayLight[n])
                eHVACByDay.insert(n, model.energy.energyByDayHVAC[n])

        if model.complete == True:
            ePCTotal = model.energy.energyByWeekPC
            eLightTotal = model.energy.energyByWeekLight
            eHVACTotal = model.energy.energyByWeekHVAC

        data.append(day)
        data.append(clock)
        data.append(energy)
        data.append(ePCByDay)
        data.append(eLightByDay)
        data.append(eHVACByDay)
        data.append(ePCTotal)
        data.append(eLightTotal)
        data.append(eHVACTotal)
        
        return data