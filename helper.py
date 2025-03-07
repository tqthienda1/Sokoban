import numpy as np

def heuristic(stones, switches):
    total = 0 
    for index, stone in enumerate(stones):
        total += min(abs(stone[0] - s[0]) + abs(stone[1] - s[1]) for s in switches)
    return total

def GetMapFromFile(file_name):  
    lines = []
    with open(file_name, "r") as f:
        for line in f:
            lines.append(line.rstrip("\n")) 

    costs = list(map(int, lines[0].split()))
    map_lines = lines[1:]

    max_len = max(len(line) for line in map_lines)

    map_lines = [list(line) + [' '] * (max_len - len(line)) for line in map_lines]
    
    map_array = np.array(map_lines)
    
    f.close()
    return map_array, costs

def find_pos(grid): 
    ares_pos = None
    stones = []
    switches_pos = []

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x,y] == '@' or grid[x,y] == '+':
                ares_pos = (x,y)
            if grid[x,y] == '$' or grid[x,y] == '*':
                stones.append((x,y,))
            if grid[x,y] == '.':
                switches_pos.append((x,y))
                

    return ares_pos, stones, switches_pos

def isDeadlock(new_stone_pos_x, new_stone_pos_y, grid):
    if grid[new_stone_pos_x, new_stone_pos_y] == '.':
        return False
    
    return  (grid[new_stone_pos_x, new_stone_pos_y - 1] == '#' and grid[new_stone_pos_x - 1, new_stone_pos_y] == '#') or \
        (grid[new_stone_pos_x, new_stone_pos_y - 1] == '#' and grid[new_stone_pos_x + 1, new_stone_pos_y] == '#') or \
        (grid[new_stone_pos_x, new_stone_pos_y + 1] == '#' and grid[new_stone_pos_x - 1, new_stone_pos_y] == '#') or \
        (grid[new_stone_pos_x, new_stone_pos_y + 1] == '#' and grid[new_stone_pos_x + 1, new_stone_pos_y] == '#')

def is_valid(grid, x, y):
    return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1] and grid[x,y] != '#'