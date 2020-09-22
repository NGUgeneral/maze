import copy
from enum import Enum
from typing import Dict, List, Tuple

# ----- START AREA: DATA MODEL

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
	_finish_location = (0, 0)

	def __init__(self, maze: Dict[int, Dict[int, Cell]], finish: Tuple[int, int], cell_height: int):
		self.frame_maze(maze)
		self._MAZE_DATA = maze
		self._finish_location = finish
		self._cell_height = cell_height

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

	def get_cell(self, x: int, y: int) -> Cell:
		return self._MAZE_DATA[y][x]

	def get_maze_size(self):
		return len(self._MAZE_DATA.keys())

	def get_maze_cell_height(self):
		return self._cell_height

	def get_finish_location(self):
		return self._finish_location

class State(Enum):
	active = 0
	victory = 1
	failed = 2

class Arrow(Enum):
	up = 0
	down = 1
	right = 2
	left = 3


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

import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def read_arrow():
        inkey = _Getch()
        while(1):
            k=inkey()
            if k!='':break
        if k=='\x1b[A':
            return Arrow.up
        elif k=='\x1b[B':
            return Arrow.down
        elif k=='\x1b[C':
            return Arrow.right
        elif k=='\x1b[D':
            return Arrow.left
        else:
            return None

# ----- END AREA: UTILS

# ----- START AREA: MOCK DATA
maze_cells_data_level_1 = {
	0: {
		0: Cell(0, 0, side_e=True),
		1: Cell(0, 1, side_w=True),
		2: Cell(0, 2)
	},
	1: {
		0: Cell(1, 0, side_e=True),
		1: Cell(1, 1, side_e=True, side_w=True),
		2: Cell(1, 2, side_w=True)
	},
	2: {
		0: Cell(2, 0),
		1: Cell(2, 1, side_e=True),
		2: Cell(2, 2, side_w=True)
	}
}

maze_level_1 = Maze(maze=maze_cells_data_level_1, finish=(2, 2), cell_height=3)

maze_cells_data_level_2 = {
	0: {
		0: Cell(0, 0, side_e=True),
		1: Cell(0, 1, side_e=True, side_w=True),
		2: Cell(0, 2, side_w=True),
		3: Cell(0, 3, side_s=True),
		4: Cell(0, 4, side_s=True),
		5: Cell(0, 5),
	},
	1: {
		0: Cell(1, 0, side_e=True),
		1: Cell(1, 1, side_e=True, side_w=True),
		2: Cell(1, 2, side_w=True),
		3: Cell(1, 3, side_n=True, side_s=True),
		4: Cell(1, 4, side_n=True, side_e=True),
		5: Cell(1, 5, side_w=True),
	},
	2: {
		0: Cell(2, 0),
		1: Cell(2, 1, side_e=True),
		2: Cell(2, 2, side_w=True, side_s=True),
		3: Cell(2, 3, side_n=True, side_e=True),
		4: Cell(2, 4, side_w=True, side_s=True, side_e=True),
		5: Cell(2, 5, side_w=True),
	},
	3: {
		0: Cell(3, 0, side_e=True),
		1: Cell(3, 1, side_w=True, side_s=True),
		2: Cell(3, 2, side_s=True, side_n=True),
		3: Cell(3, 3, side_e=True, side_s=True),
		4: Cell(3, 4, side_w=True, side_n=True),
		5: Cell(3, 5, side_s=True),
	},
	4: {
		0: Cell(4, 0, side_s=True),
		1: Cell(4, 1, side_s=True, side_n=True, side_e=True),
		2: Cell(4, 2, side_n=True, side_w=True),
		3: Cell(4, 3, side_n=True, side_s=True),
		4: Cell(4, 4, side_e=True, side_s=True),
		5: Cell(4, 5, side_w=True, side_n=True),
	},
	5: {
		0: Cell(5, 0, side_n=True),
		1: Cell(5, 1, side_n=True),
		2: Cell(5, 2),
		3: Cell(5, 3, side_n=True),
		4: Cell(5, 4, side_n=True),
		5: Cell(5, 5),
	},
}

maze_level_2 = Maze(maze=maze_cells_data_level_2, finish=(4, 5), cell_height=3)

maze_cells_data_level_3 = {
	0: {
		0: Cell(0, 0, side_e=True),
		1: Cell(0, 1, side_w=True),
		2: Cell(0, 2)
	},
	1: {
		0: Cell(1, 0, side_e=True),
		1: Cell(1, 1, side_e=True, side_w=True),
		2: Cell(1, 2, side_w=True)
	},
	2: {
		0: Cell(2, 0, side_e=True),
		1: Cell(2, 1, side_e=True, side_w=True),
		2: Cell(2, 2, side_w=True)
	},
	3: {
		0: Cell(3, 0),
		1: Cell(3, 1, side_e=True),
		2: Cell(3, 2, side_w=True)
	}
}

maze_level_3 = Maze(maze=maze_cells_data_level_3, finish=(3, 2), cell_height=3)

# ----- END AREA: MOCK DATA

# ----- START AREA: EXECUTE SEQUENCE

def game_instance(maze: Maze):
	_steps = 0
	_maze_height = maze.get_maze_size() * maze.get_maze_cell_height() + 2
	_player_location = 0, 0

	# placing finish
	_finish = maze.get_finish_location()
	maze.get_cell(_finish[1], _finish[0]).place_finish()
	state = State.active

	x, y = _player_location

	while True:
		
		maze.get_cell(x=x, y=y).place_player()
		
		view = render_maze(maze)
		if _steps > 0:
			rewrite_last_n_rows(view, _maze_height + 1)
		else:
			print(view)
		print(f'STEPS: {_steps}')

		if (y, x) == _finish:
			state = State.victory
		if state == State.victory:
			break

		output = None
		if (key := read_arrow()):
			cell = maze.get_cell(x=x, y=y)
			cell.remove_character()
			if key == Arrow.up:
				if y > 0 and not cell.side_n:
					y -= 1
			elif key == Arrow.down:
				if y < maze.get_maze_size() and not cell.side_s:
					y += 1
			elif key == Arrow.right:
				if x < maze.get_maze_size() and not cell.side_e:
					x += 1
			elif key == Arrow.left:
				if x > 0 and not cell.side_w:
					x -= 1
		else:
			break

		_steps += 1

	if state == State.victory:
		text = '=== V I C T O R Y ==='
	else:
		text = '=== G A M E  O V E R ==='
	span = (int(_maze_height / 2) - 1) * '\n'
	tab = int(_maze_height / 3) * '\t'
	rewrite_last_n_rows(span + tab + text + span, _maze_height + 1)
	print(f'STEPS: {_steps}')
		

game_instance(maze_level_2)

# ----- END AREA: EXECUTE SEQUENCE
