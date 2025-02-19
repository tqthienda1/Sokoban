import numpy as np

def GetMapFromFile(file_name):  
    lines = []
    with open(file_name, "r") as f:
        for line in f:
            lines.append(line.rstrip("\n")) 

    costs = list(map(int, lines[0].split()))
    map_lines = lines[1:]

    # Tìm độ dài lớn nhất
    max_len = max(len(line) for line in map_lines)

    # Đệm khoảng trắng vào các dòng ngắn hơn
    map_lines = [list(line) + [' '] * (max_len - len(line)) for line in map_lines]
    
    map_array = np.array(map_lines)
    return map_array, costs

def find_pos(grid): 
    ares_pos = None
    stones = []
    switches = []

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x,y] == '@' or grid[x,y] == '+':
                ares_pos = (x,y)
            if grid[x,y] == '$' or grid[x,y] == '*':
                stones.append((x,y,))

    return ares_pos, stones

def find_switches(grid):
    switches = []
    
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == '.' or grid[r,c] == '*':
                switches.append((r,c))

    return switches

def is_valid(grid, x, y):
    return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1] and grid[x,y] != '#' 