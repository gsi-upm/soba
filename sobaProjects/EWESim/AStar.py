import heapq
import random

class Cell(object):
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class AStar(object):

    def __init__(self, agent, start, finish):
        self.agent = agent
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = self.agent.model.grid.height
        self.grid_width = self.agent.model.grid.width
        self.count = 0
        
        walls = self.agent.model.Walls
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                pos = (x,y)
                if self.agent.model.thereIsWall(pos) or self.agent.model.thereIsPC(pos):
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        start_x, start_y = start
        end_x, end_y = finish
        self.start = self.get_cell(start_x, start_y)
        self.end = self.get_cell(end_x, end_y)

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        way = []
        cell = self.end
        if cell is None:
            return way
        way.append((cell.x,cell.y))
        if cell.parent is None:
            pass
        else:
            while cell.parent is not self.start:
                cell = cell.parent
                if cell is None:
                    pass
                else:
                    way.append((cell.x,cell.y))
        way.reverse()
        return way    

    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        heapq.heappush(self.opened, (self.start.f,0, self.start))
        while len(self.opened):
            f,r, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                return self.display_path()
                break
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        heapq.heappush(self.opened, (adj_cell.f, self.count, adj_cell))
                        self.count = self.count + 1