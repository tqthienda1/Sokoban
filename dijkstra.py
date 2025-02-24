from gbfs import *

def solve(map_data, stone_costs):
    node_counter = 0
    directions = [[-1, 0, 'U', 'u'], [1, 0, 'D', 'd'], [0, -1, 'L', 'l'], [0, 1, 'R', 'r']]
    ares_first_pos, stones_first_pos, switches_pos = findPos(map_data)
    frontier = PriorityQueue()
    frontier.put((0, ares_first_pos, stones_first_pos, []))
    explored = set()
    
    while(not frontier.empty()):
        
        cost, ares_cur_pos, stones_cur_pos, path = frontier.get()
        ares_cur_pos_y, ares_cur_pos_x = ares_cur_pos
        
        if (ares_cur_pos, tuple(stones_cur_pos)) in explored:
            continue
        explored.add((ares_cur_pos, tuple(stones_cur_pos)))
        
        if goal(map_data, stones_cur_pos):
            return path, cost, node_counter
        

        for dy, dx, push, move, _ in directions:
            next_pos_y, next_pos_x =  dy + ares_cur_pos[0], dx + ares_cur_pos[1]
            
            tmp_stones_cur_pos = stones_cur_pos[:]
 
            if map_data[next_pos_y][next_pos_x] == '#':
                continue
            
            is_pushed = False
            
            if (next_pos_y, next_pos_x) in stones_cur_pos:
                num_stone_explored = stones_cur_pos.index((next_pos_y, next_pos_x))
                stones_cur_pos_y, stones_cur_pos_x = stones_cur_pos[num_stone_explored] 
                
                new_stone_pos_y, new_stone_pos_x = stones_cur_pos_y + dy, stones_cur_pos_x + dx
                if map_data[new_stone_pos_y][new_stone_pos_x] == '#' or (new_stone_pos_y, new_stone_pos_x) in stones_cur_pos:
                    continue
                if isDeadlock(new_stone_pos_x, new_stone_pos_y, map_data, stones_cur_pos):
                    continue
                
                tmp_stones_cur_pos[num_stone_explored] = (new_stone_pos_y, new_stone_pos_x)
                is_pushed = True
                

            if is_pushed:
                frontier.put((cost + 1 + stone_costs[num_stone_explored], (next_pos_y, next_pos_x), tmp_stones_cur_pos, path + [push]))
            else:
                frontier.put((cost + 1, (next_pos_y, next_pos_x), tmp_stones_cur_pos, path + [move]))
            node_counter += 1
    
    return None, None, None
    
def launchDijkstra(file_name):
    map_data = []
    stone_costs = []
    
    map_data, stone_costs = loadMap(file_name)
    
    
    solution, total_cost, node_counter = solve(map_data, stone_costs)
    
    
    return solution, total_cost, node_counter