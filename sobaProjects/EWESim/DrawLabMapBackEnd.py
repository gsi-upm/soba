from collections import defaultdict
from mesa.visualization.ModularVisualization import VisualizationElement
from LabModel import LabModel
import numpy as np

class DrawLabMapBackEnd(VisualizationElement):
 
    local_includes = ["./view/DrawLabMapCanvas.js"]
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
                    portrayal = self.portrayal_method(obj)
                    if portrayal:
                        portrayal["x"] = x
                        portrayal["y"] = y
                        grid_state[portrayal["Layer"]].append(portrayal)

        offSet_Walls = 30
        for wall in model.Walls:
            JSON_Wall = {"x":wall.x,
                         "y": wall.y
            }
            grid_state[offSet_Walls].append(JSON_Wall)

        offSet_Doors = offSet_Walls + 30
        for door in model.doors:
            JSON_Door = {"x":door.x,
                         "y": door.y,
                         "state": door.state
            }
            grid_state[offSet_Doors].append(JSON_Door)

        return grid_state

class RepresentationModule(VisualizationElement):

    package_includes = ["Chart.min.js"]
    local_includes = ["./view/DrawLabMapCanvas.js"]
    local_includes = ["./lib/canvasjs.min.js"]

    def __init__(self):
        new_element = "new RepresentationModule()"
        new_element = new_element.format()
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        data = []
        clock = '0.0'
        day = model.clock.day

        if model.NStep != 0:
            clock = model.clock.clock

        data.append(day)
        data.append(clock)
        
        return data
