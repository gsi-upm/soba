import random
import time

generalItemsPos = []
doorsPos = []

class Cell(object):
    def __init__(self, pos):
        self.x, self.y = pos
        self.parent = None

def getPathRooms(model, start, finish):
    finish = Cell(finish)
    start = Cell(start)
    not_visited = [start]
    visited = []
    finishCell = None
    notFinished = True
    while notFinished:
        for cell_not_visited in not_visited:
            if cell_not_visited.x == finish.x and cell_not_visited.y == finish.y:
                finishCell = cell_not_visited
                notFinished = False
            else:
                cells = get_conected_cells1(model, cell_not_visited) #create adject cells with conection
                for cell in cells:
                    cell_already_visited = isCellVisited(cell, visited)
                    if not cell_already_visited:
                        cell.parent = cell_not_visited
                        not_visited = not_visited + [cell]
                        visited = visited + [cell]
                not_visited.remove(cell_not_visited)
            break
    cellWay = [finishCell]
    cell = finishCell
    while not (cellWay[len(cellWay)-1] is start):
        cell = cell.parent;
        cellWay = cellWay + [cell]
    cellWay.pop()
    way = []
    for cell in cellWay:
        pos = (cell.x, cell.y)
        way = way + [pos]
    way.reverse()
    return way

def getPathContinuous(model, start, finish, other = []):
    finish = Cell(finish)
    start = Cell(start)
    not_visited = [start]
    visited = []
    finishCell = None
    notFinished = True
    while notFinished:
        for cell_not_visited in not_visited:
            if cell_not_visited.x == finish.x and cell_not_visited.y == finish.y:
                finishCell = cell_not_visited
                notFinished = False
            else:
                cells = get_conected_cells2(model, cell_not_visited, other) #create adject cells with conection
                for cell in cells:
                    cell_already_visited = isCellVisited(cell, visited)
                    if not cell_already_visited:
                        cell.parent = cell_not_visited
                        if not cell in not_visited:
                            not_visited = not_visited + [cell]
                        visited = visited + [cell]
                not_visited.remove(cell_not_visited)
            break      
    cellWay = [finishCell]
    cell = finishCell
    while not (cellWay[len(cellWay)-1] is start):
        cell = cell.parent;
        cellWay = cellWay + [cell]
    cellWay.pop()
    way = []
    for cell in cellWay:
        pos = (cell.x, cell.y)
        way = way + [pos]
    way.reverse()
    return way

def get_conected_cells1(model, cell):
    room = model.getRoom((cell.x, cell.y))
    rooms = room.roomsConected
    cells = []
    for room in rooms:
        cell = Cell(room.pos)
        cells = cells + [cell]
    return cells

def get_conected_cells2(model, cell, others):
    cellPos = (cell.x, cell.y)
    cells = []
    possiblePosition1 = [(cell.x, cell.y + 1), (cell.x + 1, cell.y), (cell.x - 1, cell.y), (cell.x, cell.y - 1)]
    possiblePosition2 = [(cell.x + 1, cell.y + 1), (cell.x + 1, cell.y - 1), (cell.x - 1, cell.y - 1), (cell.x - 1, cell.y + 1)]
    possiblePosition1 = possiblePosition1 + possiblePosition2
    for posAux in possiblePosition1:
        pos1 = (0, 0)
        pos2 = (0, 0)
        aux = True
        if canMovePos(model, cellPos, posAux, others):
            cellAdded = Cell(posAux)
            cells.append(cellAdded)
    return cells

def getObtacles(model):
    for i in model.generalItems:
        generalItemsPos.append(i.pos)
    for d in model.doors:
        doorsPos.append(d.pos)
    return {'doors':doorsPos, 'general': generalItemsPos}


def canMovePos(model, cellPos, posAux, others = []):
    move = True
    for wall in model.walls:
        if (cellPos in wall.block1 and posAux in wall.block1) or (cellPos in wall.block2 and posAux in wall.block2) or (cellPos in wall.block3 and posAux in wall.block3):
            move = False
    if not move:
        if (cellPos in doorsPos or posAux in doorsPos):
            move = True
    if move:
        if not (cellPos in generalItemsPos or posAux in generalItemsPos):
            if not (cellPos in others):
                return True
    return False

def isCellVisited(cell, visited):
    for cells in visited:
        if cells.x == cell.x and cells.y == cell.y:
            return True
    return False