"""
In the file grid.py it is defined the class Grid, which implements the space where take place the simulation as a grid (x, y).
"""

class Grid:
	"""
	Class to implement the space where take place the simulation as a grid (x, y).

		Attributes:
			height: Height in number of grid cells.
			width: Width in number of grid cells.
			grid: List of rows x, rows are lists of positions y. That is, a matrix of positions [x][y].
		Methods:
			get_all_item: Get all the elements that have been placed in the grid.
			get_items_in_pos: Gets the elements located in a grid position.
			move_item: Change the position of a grid element.
			place_item: Place an element in a grid position.
			remove_item: Remove an item from the grid.
			is_cell_empty: Evaluate if a cell does not contain any item.
	"""

	def __init__(self, width, height):
		"""
		Create a new Grid object.
			Args: 
				height: Height in number of grid cells.
				width: width in number of grid cells.
			Return: Grid object
		"""
		self.height = height
		self.width = width
		self.grid = []

		for x in range(self.width):
			col = []
			for y in range(self.height):
				col.append(set())
			self.grid.append(col)

	def get_all_item(self):
		"""
		Get all the elements that have been placed in the grid.
			Return: List of items.
		"""
		items = []
		for row in range(self.width):
			for col in range(self.height):
				items.append(self.get_items_in_pos(row, col))
		return items

	def get_items_in_pos(self, pos):
		"""
		Gets the elements located in a grid position.
			Args: 
				pos: Position of the grid as (x, y).
			Return: List of items.
		"""
		x, y = pos
		return self.grid[x][y]

	def move_item(self, item, pos):
		"""
		Change the position of a grid element.
			Args: 
				item: Element in the grid.
				pos: New position of the item.
		"""
		self.remove_item(item.pos, item)
		self.place_item(item, pos)

	def place_item(self, item, pos):
		"""
		Place an element in a grid position.
			Args: 
				pos: Position of the grid as (x, y).
				item: Element outside the grid.
		"""
		x, y = pos
		self.grid[x][y].add(item)
		item.pos = pos

	def remove_item(self, pos, item):
		"""
		Remove an item from the grid.
			Args: 
				pos: Position of the grid as (x, y).
				item: Element inside the grid.
		"""
		x, y = pos
		self.grid[x][y].remove(item)

	def is_cell_empty(self, pos):
		"""
		Evaluate if a cell does not contain any item.
			Args: 
				pos: Position of the grid as (x, y).
			Return: True (yes) or False (no).
		"""
		x, y = pos
		return False if len(self.grid[x][y]) > 0 else True