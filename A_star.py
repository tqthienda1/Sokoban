from BFS import *
from map_processor import *
import math
import heapq
from collections import deque

def heuristic(stones, switches):
    total = 0 
    for stone in stones:
        total += min(abs(stone[0] - s[0]) + abs(stone[1] - s[1]) for s in switches)
    return total

def order_A_star(grid, start_node, stones, costs, switches):
    totalCost = 0
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(stones, switches), 0, start_node, tuple(stones), [], totalCost ))
    closed_list = set()
    directions = [(-1, 0, 'U', 'u'), (1, 0, 'D', 'd'), (0, -1, 'L', 'l'), (0, 1, 'R', 'r')] # đi đến 4 hướng

    while open_list:
        f, g, (ares_r, ares_c), stones_pos, path, totalCost = heapq.heappop(open_list)

        if ((ares_r, ares_c), stones_pos) in closed_list:
            continue

        closed_list.add(((ares_r,ares_c), stones_pos))

        if all(grid[r,c] == '.' for r,c in stones_pos):
            return path, totalCost
        
        for dr, dc, push, move in directions:
            new_r, new_c = ares_r + dr, ares_c + dc

            if not is_valid(grid, new_r, new_c):
                continue

            cur_cost = totalCost + 1
            new_stones = list(stones_pos)
            isPush = False

            if(new_r, new_c) in stones_pos: 
                for stone_index, (sr, sc) in enumerate(stones_pos):
                    if (sr, sc) == (new_r, new_c):
                        break

                new_stone_r = new_r + dr
                new_stone_c = new_c + dc

                if not is_valid(grid, new_stone_r, new_stone_c) or (new_stone_r, new_stone_c) in stones_pos:
                    continue
                    
                new_stones[stone_index] = (new_stone_r, new_stone_c)
                cur_cost += costs[stone_index]
                isPush = True
            
            new_g = g + 1
            new_f = new_g + heuristic(new_stones, switches)
            
            if isPush:
                new_path =  path +[push]
            else:
                new_path = path +[move]
            
            heapq.heappush(open_list, (new_f, new_g, (new_r, new_c), tuple(new_stones), new_path, cur_cost))

    return None

                             
