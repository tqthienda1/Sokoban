from collections import deque
from helper import *

def order_bfs(grid, start_node, stones, costs):
    node_counter = 0 
    totalCost = 0
    queue = deque([(start_node, tuple(stones), [], totalCost)]) 
    visited = set()
    directions = [(-1, 0, 'U', 'u'), (1, 0, 'D', 'd'), (0, -1, 'L', 'l'), (0, 1, 'R', 'r')]

    while queue:
        (ares_x, ares_y), stones_pos, path, totalCost = queue.popleft()

        if(ares_x, ares_y, stones_pos) in visited:
            continue
        visited.add((ares_x, ares_y, stones_pos))
        
        if all(grid[x,y] == '.' for x,y in stones_pos):
            return path, totalCost, node_counter
        

        for dx, dy, push, move in directions:
            new_x, new_y = ares_x + dx, ares_y + dy

            if not is_valid(grid, new_x, new_y):
                continue
            
            cur_cost = totalCost
            cur_cost += 1 
            new_stones = list(stones_pos) 
            isPush = False 
            
        
            if (new_x,new_y) in stones_pos:
                stone_index = stones_pos.index((new_x, new_y))

                new_stone_x = new_x + dx
                new_stone_y = new_y + dy

                if not is_valid(grid, new_stone_x, new_stone_y) or (new_stone_x, new_stone_y) in stones_pos or isDeadlock(new_stone_x, new_stone_y, grid):
                    continue
                
                new_stones[stone_index] = (new_stone_x, new_stone_y)
                cur_cost += costs[stone_index]
                isPush = True
            
            if isPush:
                queue.append(((new_x, new_y), tuple(new_stones), path + [push], cur_cost))
            else:
                queue.append(((new_x, new_y), tuple(new_stones), path + [move], cur_cost))
            node_counter += 1

    return None


                

