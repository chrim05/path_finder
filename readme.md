# how to use the lib
* open terminal: ```bash
git clone https://github.com/christallo/path_finder
cd path_finder
code .
```

* create a `main.py`: ```python
# start by creating a path finder instance containing the map, the starting point and the target point
path_finder = PathFinder(
  [
    # A
    [' ', ' ', ' ', ' ', '#'],
    [' ', ' ', ' ', ' ', '#'],
    [' ', '#', ' ', ' ', ' '],
    [' ', '#', ' ', '#', ' '],
    [' ', ' ', ' ', ' ', ' '], # B
  ],      # the map ('#' = wall, ' ' = empty slot in which the player can move in)

  (0, 0), # the starting point
  (4, 4)  # the target point
)

paths = path_finder.get_paths_that_reach_target()
faster_paths_refs = get_fastest_paths(paths)
```

NOTE: check the file at `if __name__ == '__main__'` to see a complete example

# how to run the test(s)
* open terminal ```bash
git clone https://github.com/christallo/path_finder
cd path_finder
python3.10 path_finder.py
```

# requirements
nothing just python 3.10
