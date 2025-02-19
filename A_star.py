from BFS import *
from map_processor import *
import math
import heapq
from collections import deque

def heuristic(stones, switches):
    total = 0 
    for stone in stones:
        min(abs(stone[0] - s[0]) + abs(stone[1] - s[1]) for s in switches)
    return total

def order_A_star(grid, start_node, stones, costs, switches):
    totalCost = 0
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(stones, switches), 0, start_node, tuple(stones), [], totalCost ))
    closed_list = set()
    directions = [(-1, 0, 'U', 'u'), (1, 0, 'D', 'd'), (0, -1, 'L', 'l'), (0, 1, 'R', 'r')] # đi đến 4 hướng

    while open_list:
        f, g, (ares_r, ares_c), stones_pos, path, totalCost = heapq.heappop()

        if ((ares_r, ares_c), stones_pos) in closed_list:
            continue

        closed_list.add((ares_r,ares_c), stones_pos)

        if all(grid[r,c] == '.' for r,c in stones_pos):
            return path, totalCost
        
        for dr, dc, push, move in directions:
            new_r, new_c = ares_r + dr, ares_c + dc

            if not is_valid(grid, new_r, new_c):
                continue

            cur_cost = totalCost
            cur_cost += 1
            new_stones = list(stones_pos)
            isPush = False

            if(new_r, new_c) in stones_pos: 
                stone_index = stones_pos.index((new_r, new_c))

                new_stone_r = new_r + dr
                new_stone_c = new_c + dc

                if not is_valid(grid, new_stone_r, new_stone_c) or (new_stone_r, new_stone_c) in stones_pos:
                    continue
                    
                


                             
