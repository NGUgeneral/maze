from typing import Dict, List
import copy

# ----- START AREA: DATA MODEL

class Cell:

	_SYMBOL = []
	_mark = ' '
	_maze = None
	coord_i = -1
	coord_j = -1
	side_n = False
	side_e = False
	side_s = False
	side_w = False


	def __init__(
		self,
		coord_i: int,
		coord_j: int,
		side_n: bool = False,
		side_e: bool = False,
		side_s: bool = False,
		side_w: bool = False
		):
		self.coord_i = coord_i
		self.coord_j = coord_j
		self.side_n = side_n
		self.side_e = side_e
		self.side_s = side_s
		self.side_w = side_w


	def symbol(self) -> List[List[str]]:
		# TODO: SAVE SYMBOL STATE
		if not self._SYMBOL:
			print(f'I am about to build symbol for cell {self.coord_i}:{self.coord_j}')
			symbol = [
				[' ', ' ', ' ', ' ', ' '],
				[' ', ' ', self._mark, ' ', ' '],
				[' ', ' ', ' ', ' ', ' ']
			]
			if self.side_e:
				for smb in symbol:
					smb[-1] = '|'
			if self.coord_j == 0:
				for smb in symbol:
					smb.insert(0, '|')
			if self.side_s:
				replace_list_item(symbol[-1], ' ', '_')
			if self.coord_i == 0:
				symbol.insert(0, [' ', '_', '_', '_', '_'])
			if self.coord_j == self._maze.get_maze_size() - 1:
				for smb in symbol:
					smb[-1] += '\n'
			self._SYMBOL = symbol
		return self._SYMBOL
	# TODO: BUILT-IN CELL MARK SUPPORT

	def place_mark(self, mark: str):
		if not len(mark) == 1:
			raise ValueError('Invalid mark provided to place')
		self._mark = mark

	def clear_mark(self):
		self._mark = ' '

class Maze:

	_MAZE_DATA = {}

	def __init__(self, maze: Dict[int, Dict[int, Cell]]):
		print('init maze')
		self.frame_maze(maze)
		self._MAZE_DATA = maze

	def frame_maze(self, maze: Dict[int, Dict[int, Cell]]):
		print('I am about to build maze frame')
		size = len(maze.keys())
		for i in maze:
			for j in maze[i]:
				cell = maze[i][j]
				if i == 0:
					cell.side_n = True
				if i == size - 1:
					cell.side_s = True
				if j == 0:
					cell.side_w = True
				if j == size - 1:
					cell.side_e = True
				cell._maze = self


	def get_maze(self) -> Dict[int, Dict[int, Cell]]:
		return self._MAZE_DATA

	def get_maze_size(self):
		return len(self._MAZE_DATA.keys())


# ----- END AREA: DATA MODEL

# ----- START AREA: LOGIC / VIEW

def render_maze(maze: Maze) -> str:
	rows = maze.get_maze()
	print_rows = []
	for i in rows:
		print_row = []
		for j in rows[i]:
			cell = rows[i][j]
			symbol = cell.symbol()
			# TODO: smels like there is a way to merge branches below
			if not print_row:
				#TODO: try to get rid of deepcopy, use custom 3d deep copy
				print_row += copy.deepcopy(symbol)
			else:
				c = 0
				while c < len(symbol):
					print_row[c] += symbol[c]
					c += 1
		print_rows.append(print_row)
	return ''.join(flatten_nested_list(print_rows))

# ----- START AREA: LOGIC / VIEW

# ----- START AREA: UTILS

def flatten_nested_list(nested_list):
	flatten_list = list(nested_list)
	if flatten_list:
		while isinstance(flatten_list[0], list):
			flatten_list = [y for x in flatten_list for y in x]
	return flatten_list


def replace_list_item(items, old_value, new_value):
	for index, item in enumerate(items):
	    if item == old_value:
	        items[index] = new_value
	if items[-1] == '_':
		items[-1] = ' '



# ----- END AREA: UTILS

# ----- START AREA: MOCK DATA
maze_cells_data = {
	0: {
		0: Cell(0, 0, side_e=True),
		1: Cell(0, 1),
		2: Cell(0, 2)
	},
	1: {
		0: Cell(1, 0, side_e=True),
		1: Cell(1, 1, side_e=True),
		2: Cell(1, 2)
	},
	2: {
		0: Cell(2, 0),
		1: Cell(2, 1, side_e=True),
		2: Cell(2, 2)
	}
}

# ----- END AREA: MOCK DATA

# ----- START AREA: EXECUTE SEQUENCE

answer = ''
maze = Maze(maze_cells_data)
maze_cells_data[0][0].place_mark('*')
while not (answer in ['N', 'n']):  
	answer = input('Would you like to render maze? (Y/N):\n')
	if answer in ['Y', 'y']:
		maze_cells_data[0][0].clear_mark()
		view = render_maze(maze)
		print(view)

# ----- END AREA: EXECUTE SEQUENCE
