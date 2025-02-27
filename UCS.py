import numpy as np
import heapq

WALL = '#'
STONE = '$'
ARES = '@'
SWITCH = '.'
STONE_ON_SWITCH = '*'
ARES_ON_SWITCH = '+'

directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]

def GetMapFromFile(file_name):
    lines = []
    with open(file_name, "r") as f:
        weights = list(map(int, f.readline().strip().split())) 
        for line in f:
            lines.append(list(line.rstrip("\n")))

    max_len = max(len(line) for line in lines)
    lines = [line + [' '] * (max_len - len(line)) for line in lines]
    map_array = np.array(lines)
    return map_array, weights


def find_initial_state(game_map, weights):
    ares_pos, stones, switches = None, [], []
    stone_weights = []
    stone_idx = 0  
    for i in range(game_map.shape[0]):
        for j in range(game_map.shape[1]):
            cell = game_map[i, j]
            if cell == ARES:
                ares_pos = (i, j)
            elif cell == STONE:
                stones.append((i, j))
                stone_weights.append(((i, j), weights[stone_idx]))
                stone_idx += 1
            elif cell == SWITCH:
                switches.append((i, j))
    
    return ares_pos, frozenset(stones), frozenset(switches), frozenset(stone_weights)


def is_goal_state(stones, switches):
    return stones == switches

def is_valid_move(game_map, pos):
    x, y = pos
    return 0 <= x < game_map.shape[0] and 0 <= y < game_map.shape[1] and game_map[x, y] != WALL

def isDeadlock(new_stone_pos_x, new_stone_pos_y, grid):
    if grid[new_stone_pos_x, new_stone_pos_y] == '.':
        return False
    
    return  (grid[new_stone_pos_x, new_stone_pos_y - 1] == '#' and grid[new_stone_pos_x - 1, new_stone_pos_y] == '#') or \
        (grid[new_stone_pos_x, new_stone_pos_y - 1] == '#' and grid[new_stone_pos_x + 1, new_stone_pos_y] == '#') or \
        (grid[new_stone_pos_x, new_stone_pos_y + 1] == '#' and grid[new_stone_pos_x - 1, new_stone_pos_y] == '#') or \
        (grid[new_stone_pos_x, new_stone_pos_y + 1] == '#' and grid[new_stone_pos_x + 1, new_stone_pos_y] == '#')

def get_next_states(state, game_map):
    ares_pos, stones, switches, stone_weights = state
    next_states = []
    stone_weight_dict = dict(stone_weights)
    
    for dx, dy, move_char, push_char in directions:
        nx, ny = ares_pos[0] + dx, ares_pos[1] + dy
        if not is_valid_move(game_map, (nx, ny)):
            continue
        
        if (nx, ny) in stones:  
            next_stone_pos = (nx + dx, ny + dy)
            if (is_valid_move(game_map, next_stone_pos) and next_stone_pos not in stones) and not isDeadlock(next_stone_pos[0], next_stone_pos[1], game_map):
                cost = stone_weight_dict[(nx, ny)]
                new_stones = frozenset(s for s in stones if s != (nx, ny)) | {next_stone_pos}
                new_stone_weights = frozenset((s, w) if s != (nx, ny) else (next_stone_pos, w) for s, w in stone_weights)
                next_states.append(((nx, ny), new_stones, switches, new_stone_weights, push_char, cost))
        else:
            next_states.append(((nx, ny), stones, switches, stone_weights, move_char, 0))  
    
    return next_states


def sokoban_ucs(game_map, weights):
    start_state = find_initial_state(game_map, weights)
    pq = [(0, start_state, "")]
    visited = {}
    node_counter = 0

    while pq:
        cost, state, path = heapq.heappop(pq)
        ares_pos, stones, switches, stone_weights = state
        
        if is_goal_state(stones, switches):
            return path, cost, node_counter

        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        for next_state in get_next_states(state, game_map):
            new_ares_pos, new_stones, new_switches, new_stone_weights, move, step_cost = next_state
            new_state = (new_ares_pos, new_stones, new_switches, new_stone_weights)
            heapq.heappush(pq, (cost + step_cost, new_state, path + move))
            node_counter += 1
    
    return None, None, None

def launchUCS(file_name):
    game_map, weights = GetMapFromFile(file_name)
    solution, total_cost, node_counter = sokoban_ucs(game_map, weights)

    return solution, total_cost, node_counter