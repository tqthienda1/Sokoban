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
        weights = list(map(int, f.readline().strip().split()))  # Đọc trọng lượng
        for line in f:
            lines.append(list(line.rstrip("\n")))

    max_len = max(len(line) for line in lines)
    lines = [line + [' '] * (max_len - len(line)) for line in lines]
    map_array = np.array(lines)
    return map_array, weights


def find_initial_state(game_map):
    ares_pos, stones, switches = None, [], []
    for i in range(game_map.shape[0]):
        for j in range(game_map.shape[1]):
            cell = game_map[i, j]
            if cell == ARES:
                ares_pos = (i, j)
            elif cell == STONE:
                stones.append((i, j))
            elif cell == SWITCH:
                switches.append((i, j))
    return ares_pos, tuple(stones), tuple(switches)


def is_goal_state(stones, switches):
    return all(pos in switches for pos in stones)

def is_valid_move(game_map, pos):
    x, y = pos
    return 0 <= x < game_map.shape[0] and 0 <= y < game_map.shape[1] and game_map[x, y] != WALL

def get_next_states(state, game_map, weights):
    ares_pos, stones, switches = state  # Trạng thái bao gồm ares_pos, stones, và switches
    next_states = []
    for dx, dy, move_char, push_char in directions:
        nx, ny = ares_pos[0] + dx, ares_pos[1] + dy
        if not is_valid_move(game_map, (nx, ny)):
            continue
        if (nx, ny) in stones:  # Nếu Ares muốn di chuyển vào viên đá
            next_stone_pos = (nx + dx, ny + dy)
            if is_valid_move(game_map, next_stone_pos) and next_stone_pos not in stones:
                stone_index = stones.index((nx, ny))  # Lấy index để tìm trọng lượng
                cost = 1 + weights[stone_index]  # Đẩy viên đá
                new_stones = tuple(s for s in stones if s != (nx, ny)) + (next_stone_pos,)
                next_states.append(((nx, ny), new_stones, switches, push_char, cost))
        else:
            next_states.append(((nx, ny), stones, switches, move_char, 1))  # Di chuyển bình thường
    return next_states


def sokoban_ucs(game_map, weights):
    start_state = find_initial_state(game_map)
    pq = [(0, start_state, "")]  # (cost, state, path)
    visited = {}

    while pq:
        cost, state, path = heapq.heappop(pq)
        ares_pos, stones, switches = state
        
        if is_goal_state(stones, switches):  # Kiểm tra điều kiện thắng
            return path, cost

        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        for next_state in get_next_states(state, game_map, weights):
            new_ares_pos, new_stones, new_switches, move, step_cost = next_state
            heapq.heappush(pq, (cost + step_cost, (new_ares_pos, new_stones, new_switches), path + move))
    
    print("No solution found")
    return None, None


def launchUCS(file_name):
    game_map, weights = GetMapFromFile(file_name)
    return sokoban_ucs(game_map, weights)
