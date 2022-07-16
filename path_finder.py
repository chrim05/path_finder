from copy import deepcopy

name_direction2direction_changer = {
  'up': (0, -1),
  'down': (0, +1),
  'left': (-1, 0),
  'right': (+1, 0),
}

name_direction2direction_symbol = {
  'up': '↑',
  'down': '↓',
  'left': '←',
  'right': '→',
}

class Branch:
  def __init__(self, up, down, left, right):
    self.up = up
    self.down = down
    self.left = left
    self.right = right

  def __repr__(self):
    return repr(self.__dict__)

class PathFinder:
  def __init__(self, world_map, a, b):
    '''
    `world_map`: list[list[chr]] -> the map
    `a`: tuple(int, int) -> the starting point
    `b`: tuple(int, int) -> the target point
    '''
    self.map = world_map
    self.a = a
    self.b = b
    # it's gonna contain all the position for each branch and its sub branches
    self.positions = [a]
  
  @property
  def pos(self):
    return self.positions[-1]
  
  @property
  def prev_pos(self):
    try:
      return self.positions[-3]
    except IndexError:
      pass
  
  @property
  def cur(self):
    return self.at(self.pos)
  
  def at(self, pos):
    '''
    returns the slot value at a specific position
    '''
    # checking the validity of the coordinates
    if not self.is_valid_coord((pos[1], pos[0])):
      raise ValueError(f'invalid coord (x: {pos[0]}, y: {pos[1]})')

    return self.map[pos[1]][pos[0]]
  
  def is_valid_coord(self, coord):
    '''
    checks whether `coord` is valid (points to an existing map's slot)
    `coord`: tuple[int, int]
    '''
    # the coordinates must be positive, its x must be less than the map's columns length and its y must be less than the map's rows length
    return coord[0] >= 0 and coord[1] >= 0 and coord[0] < len(self.map[0]) and coord[1] < len(self.map)
  
  def look(self, direction):
    '''
    returns the state of the block in the direction indicated by `direction` (go_up, go_down, ...)
    '''
    # updating the position to the one of the block the function is looking at
    self.positions.append(sum_positions(self.pos, name_direction2direction_changer[direction]))

    # the block state is gonna be None when its pos coordinate points to an invalid slot (the slot is outside the map)
    # or when on pos he has already passed one of the parents of the branch (excluding the current pos)
    # or when the slot is occupied by a wall
    if not self.is_valid_coord(self.pos) or self.pos in [self.a] + self.positions[:-1] or self.cur != ' ':
      r = None
    # otherwise the block sate is gonna be '!' when the pos is the same of the target one, so the branch reached the target pos
    # or it's gonna recursively create a branch about the next block
    else:
      r = '!' if self.pos == self.b else self.create_branch_tree()

    # updating the pos to the previous
    self.positions.pop()

    return r

  def create_branch_tree(self):
    '''
    returns a branch containing the state of the 4 blocks from which it is surrounded
    
    the state can be:
    * `None` whether the block is outside the map or the it's a wall
    * `Branch` whether it's an empty slot, that branch's instance is recursive
    '''
    return Branch(
      self.look('up'),
      self.look('down'),
      self.look('left'),
      self.look('right')
    )
  
  def get_paths_that_reach_target(self):
    '''
    returns a list containing all the paths reaching the target pos
    '''
    tree = path_finder.create_branch_tree()
    result = []
    tree2linear_selecting_only_target_reacher(tree, [], result)

    return result
  
def tree2linear_selecting_only_target_reacher(branch, current_list, result):
  '''
  converts a tree into a linear array containing all combination between a branch and all its sub branches
  '''
  branch = branch.__dict__

  for field in branch:
    # when the branch's field is a sub branch
    if isinstance(branch[field], Branch):
      tree2linear_selecting_only_target_reacher(branch[field], current_list + [field], result)
    # otherwise when the field is not a sub branch but a terminating branch (
    #   it can be None to indicate the end of the parent's branch
    #   or it can be '!' to indicates the reaching of the target pos
    # )
    # adding the path to the resulting paths only whether it's not None (so it reaches the target)
    elif branch[field] == '!':
      result.append(current_list + [field])

def get_fastest_paths(paths):
  '''
  returns a List[List[str]] (a list of paths) of fastest paths (less passes to reach target)
  `paths`: List[List[str]] -> all valid paths (paths reaching the target)
  '''  
  return list(filter(lambda path: len(path) == min(map(len, paths)), paths))

def sum_positions(l, r):
  '''
  adds two Tuple[int, int] which are interpreted as position (x, y)

  examples:
  * `(1, 2) + (3, 4) = (4, 6)`
  * `(0, 1) + (0, -1) = (0, 0)`

  `l`: Tuple[int, int] -> left pos
  `r`: Tuple[int, int] -> right pos
  '''
  return (l[0] + r[0], l[1] + r[1])

def print_map(m):
  '''
  prints the map with edges and indexes
  `m`: List[List[chr]]
  '''
  print_edges = lambda: print(' ' * len(str(len(m))) + ' ' + '= ' * (len(m[0]) + 2))

  # printing column indexes
  print('    ' + ' '.join(map(str, range(len(m[0])))))
  # printing upper edges
  print_edges()

  for i, row in enumerate(m):
    # calculating the padding to get the edge aligned with other columns
    left_index_padding = " " * (len(str(len(m))) - len(str(i)))
    # printing the row index + left edge + row + right edge
    print(*([f'{i}{left_index_padding} |'] + row + ['|']))
  
  # printing lower edges
  print_edges()
  print()

#
# Simple test for the library
#

if __name__ == '__main__':
  #
  # Map structure:
  #  ' ' -> empty slot (can move in)
  #  '#' -> wall slot (cannot move in)
  #  '°' -> the traveled path
  #  A   -> the starting point
  #  B   -> the target point
  #

  path_finder = PathFinder(
    [
      # A
      [' ', ' ', ' ', ' ', '#'],
      [' ', ' ', ' ', ' ', '#'],
      [' ', '#', ' ', ' ', ' '],
      [' ', '#', ' ', '#', ' '],
      [' ', ' ', ' ', ' ', ' '], # B
    ],      # the map

    (0, 0), # the starting point
    (4, 4)  # the target point
  )

  # printing the original map
  print('ORIGINAL')
  print_map(path_finder.map)

  # getting a List[List[direction (aka str)]] containing all possible paths found to reach the target pos
  valid_paths = path_finder.get_paths_that_reach_target()
  
  # checking whether the target is unreachable
  if len(valid_paths) == 0:
    exit('UNSOLVABLE')

  # getting a list containing refs to faster paths
  faster_paths = get_fastest_paths(valid_paths)

  # printing all solution maps + whether they are one of faster or not
  for i, path in enumerate(valid_paths):
    # cloning the map to replace only the empty slots with direction instructions without getting side effects on the original map (path_finder.map)
    new_map = deepcopy(path_finder.map)
    # pos = starting pos
    pos = path_finder.a
    
    # indexing a map is [y][x] (because the map is a List[List[str]] which contains rows (List[str]) which contain columns)
    # drawing 'A' in the starting point
    new_map[pos[1]][pos[0]] = 'A'

    # for direction instruction in path (go_up, go_down, ...)
    for direction in path:
      # updating the pos with the instruction
      pos = sum_positions(pos, name_direction2direction_changer[direction])
      # drawing the direction instruction into the clone map
      new_map[pos[1]][pos[0]] = name_direction2direction_symbol[direction]
    
    # drawing 'B' in the target point
    new_map[pos[1]][pos[0]] = 'B'
    
    # printing the map and the solution number
    print(f'SOLUTION{i}', '(one of faster)' if path in faster_paths else '')
    print_map(new_map)