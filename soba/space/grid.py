import itertools
import random
import math

class Grid:
    def __init__(self, width, height, torus = False):

        self.height = height
        self.width = width
        self.torus = torus
        self.grid = []

        for x in range(self.width):
            col = []
            for y in range(self.height):
                col.append(set())
            self.grid.append(col)

    def get_all_item(self):
        items = []
        for row in range(self.width):
            for col in range(self.height):
                items.append(self.get_items_in_pos(row, col))

    def get_items_in_pos(self, pos):
        x, y = pos
        return self.grid[x][y]

    def move_item(self, item, pos):
        self.remove_item(item.pos, item)
        self.place_item(item, pos)

    def place_item(self, item, pos):
        x, y = pos
        self.grid[x][y].add(item)
        item.pos = pos

    def remove_item(self, pos, item):
        x, y = pos
        self.grid[x][y].remove(item)

    def is_cell_empty(self, pos):
        x, y = pos
        return True if len(self.grid[x][y]) > 0 else False