import numpy as np

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
        weights = list(map(int, f.readline().strip().split()))  # Đọc trọng lượng
        for line in f:
            lines.append(list(line.rstrip("\n")))

    max_len = max(len(line) for line in lines)
    lines = [line + [' '] * (max_len - len(line)) for line in lines]
    map_array = np.array(lines)
    return map_array, weights


def find_initial_state(game_map, weights):
    ares_pos, stones, switches = None, [], []
    stone_weights = []
    stone_idx = 0  # Dùng để ánh xạ trọng lượng
    
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


def get_next_states(state, game_map):
    ares_pos, stones, switches, stone_weights = state
    next_states = []
    stone_weight_dict = dict(stone_weights)
    
    for dx, dy, move_char, push_char in directions:
        nx, ny = ares_pos[0] + dx, ares_pos[1] + dy
        if not is_valid_move(game_map, (nx, ny)):
            continue
        
        if (nx, ny) in stones:  # Nếu Ares muốn di chuyển vào viên đá
            if (nx, ny) in switches:
                continue  # Không thể đẩy viên đá đã nằm trên switch
            next_stone_pos = (nx + dx, ny + dy)
            if is_valid_move(game_map, next_stone_pos) and next_stone_pos not in stones:
                cost = 1 + stone_weight_dict[(nx, ny)]
                new_stones = frozenset(s for s in stones if s != (nx, ny)) | {next_stone_pos}
                new_stone_weights = frozenset((s, w) if s != (nx, ny) else (next_stone_pos, w) for s, w in stone_weights)
                next_states.append(((nx, ny), new_stones, switches, new_stone_weights, push_char, cost))
        else:
            next_states.append(((nx, ny), stones, switches, stone_weights, move_char, 1))  # Di chuyển bình thường
    
    return next_states


def sokoban_dfs(game_map, weights):
    start_state = find_initial_state(game_map, weights)
    stack = [(start_state, "", 0)]
    visited = set()
    node_counter = 0

    while stack:
        state, path, cost = stack.pop()
        ares_pos, stones, switches, stone_weights = state
        
        if is_goal_state(stones, switches):
            print("Solution path:", path)
            print("Total cost:", cost)
            return path, cost

        if state in visited:
            continue
        visited.add(state)

        for next_state in get_next_states(state, game_map):
            new_ares_pos, new_stones, new_switches, new_stone_weights, move, step_cost = next_state
            if is_goal_state(new_stones, new_switches):  # Dừng ngay khi đạt trạng thái mục tiêu
                print("Solution path:", path + move)
                print("Total cost:", cost + step_cost)
                return path + move, cost + step_cost
            stack.append(((new_ares_pos, new_stones, new_switches, new_stone_weights), path + move, cost + step_cost))
            node_counter += 1
    

def launchDFS(file_name):
    node_counter = 0
    game_map, weights = GetMapFromFile(file_name)
    solution, total_cost, node_counter = sokoban_dfs(game_map, weights, node_counter)

    return solution, total_cost, node_counter
