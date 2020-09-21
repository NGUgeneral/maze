from typing import Dict, List
import copy
from time import sleep

# ----- START AREA: DATA MODEL

_R_TEST_FLAG = True

def rewrite_last_n_rows(string, rows):
	prefix = '\n' + rows * u'\u008D' 
	print(f"{prefix}{string}")

class Cell:
	_SYMBOL = None
	_mark_00= ' '
	_mark_01= ' '
	_mark_10= ' '
	_mark_11= ' '
	_maze = None # NEED TO GET RID OF IT
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

		self._symbol_updated = True


	def symbol(self) -> List[List[str]]:
		if self._symbol_updated:
			symbol = [
				[' ', ' ', ' ', ' ', ' '],
				[' ', self._mark_00, self._mark_01, ' ', ' '],
				[' ', self._mark_10, self._mark_11, ' ', ' ']
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
			self._symbol_updated = False
		return self._SYMBOL

	def place_character(self, _2x2):
		self._mark_00 = _2x2[0]
		self._mark_01 = _2x2[1]
		self._mark_10 = _2x2[2]
		self._mark_11 = _2x2[3]
		self._symbol_updated = True

	def remove_character(self):
		self._mark_00 = ' '
		self._mark_01 = ' '
		self._mark_10 = ' '
		self._mark_11 = ' '
		self._symbol_updated = True

	def place_player(self):
		self.place_character(['/', '\\', '\\', '/'])

	def place_enemy(self):
		self.place_character(['\\', '/', '/', '\\'])

	def place_finish(self):
		self.place_character(['+', '+', '+', '+'])

class Maze:

	_MAZE_DATA = {}

	def __init__(self, maze: Dict[int, Dict[int, Cell]]):
		self.frame_maze(maze)
		self._MAZE_DATA = maze

	def frame_maze(self, maze: Dict[int, Dict[int, Cell]]):
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

	def get_maze_cell_height(self):
		return 3


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
	return ''.join(flatten_nested_list(print_rows))[:-1]

# ----- END AREA: LOGIC / VIEW

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

maze = Maze(maze_cells_data)
steps = 0
if _R_TEST_FLAG:
	_maze_height = maze.get_maze_size() * maze.get_maze_cell_height() + 2
	_PLAYER_LOCATION = (0,0)
	x, y = _PLAYER_LOCATION
	_FINISH_LOCATION = (2,2)
	maze_cells_data[_FINISH_LOCATION[1]][_FINISH_LOCATION[0]].place_finish()
	state = 0 # convert to enum
	for i in range(10):
		if (y, x) == _FINISH_LOCATION:
			state = 1
		if state == 1:
			break
		maze_cells_data[x][y].remove_character()
		if i == 0:
			y, x = 0, 0
		if  i == 1:
			y, x = 0, 1
		if  i == 2:
			y, x = 0, 2
		if  i == 3:
			y, x = 1, 2
		if i == 4:
			y, x = 1, 1
		if i == 5:
			y, x = 1, 0
		if i == 6:
			y, x = 2, 0
		if i == 7:
			y, x = 2, 1
		if i == 8:
			y, x = 2, 2
		maze_cells_data[x][y].place_player()
		view = render_maze(maze)
		if i > 0:
			rewrite_last_n_rows(view, _maze_height + 1)
		else:
			print(view)
		steps += 1
		print(f'STEPS: {steps}')
		sleep(0.5)
	if state == 1:
		rewrite_last_n_rows('\n\n\n\n\n\t\t\t=== V I C T O R Y ===\n\n\n\n', _maze_height + 1)
		print(f'STEPS: {steps}')
else:
	answer = ''
	while not (answer in ['N', 'n']):  
		answer = input('Would you like to render maze? (Y/N):\n')
		if answer in ['Y', 'y']:
			view = render_maze(maze)
			print(view)

# ----- END AREA: EXECUTE SEQUENCE
