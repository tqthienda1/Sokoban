from collections import deque
from queue import PriorityQueue
from helper import *

def loadMap(file_name):
    map_data = []
    stone_costs = []
    
    with open(file_name, 'r') as file:
        stone_costs = list(map(int, file.readline().strip().split()))
        
        map_data = [line.rstrip() for line in file.readlines()]
    
    file.close()
    
    return map_data, stone_costs

def findPos(map_data):
    ares_pos = None
    stones_pos = []
    switches_pos = []
    
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            if map_data[row][col] == '@':
                ares_pos = (row, col)
            if map_data[row][col] == '$':
                stones_pos.append((row, col))
            if map_data[row][col] == '.':
                switches_pos.append((row, col))
    
    return ares_pos, stones_pos, switches_pos
                
def goal(map_data, stone_cur_pos):
    for pos_stone_y, pos_stone_x in stone_cur_pos:
        if map_data[pos_stone_y][pos_stone_x] != '.':
            return False
            
    return True

def isDeadlock(new_stone_pos_x, new_stone_pos_y, map_data, stones_cur_pos):
    if map_data[new_stone_pos_y][new_stone_pos_x] == '.':
        return False
    
    return  (map_data[new_stone_pos_y - 1][new_stone_pos_x] == '#' and map_data[new_stone_pos_y][new_stone_pos_x - 1] == '#') or \
            (map_data[new_stone_pos_y - 1][new_stone_pos_x] == '#' and map_data[new_stone_pos_y][new_stone_pos_x + 1] == '#') or \
            (map_data[new_stone_pos_y + 1][new_stone_pos_x] == '#' and map_data[new_stone_pos_y][new_stone_pos_x - 1] == '#') or \
            (map_data[new_stone_pos_y + 1][new_stone_pos_x] == '#' and map_data[new_stone_pos_y][new_stone_pos_x + 1] == '#')

           
 
def solve(map_data, stone_costs):
    node_counter = 0
    directions = [[-1, 0, 'U', 'u', 0], [1, 0, 'D', 'd', 0], [0, -1, 'L', 'l', 0], [0, 1, 'R', 'r', 0]]
    ares_first_pos, stones_first_pos, switches_pos = findPos(map_data)
    frontier = PriorityQueue()
    frontier.put((heuristic(stones_first_pos, switches_pos) , ares_first_pos, stones_first_pos, [], 0))
    explored = set()
    
    while(not frontier.empty()):
        
        heuristic_value, ares_cur_pos, stones_cur_pos, path, cost = frontier.get()
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
                frontier.put((heuristic(stones_cur_pos, switches_pos), (next_pos_y, next_pos_x), tmp_stones_cur_pos, path + [push], cost + stone_costs[num_stone_explored]))
            else:
                frontier.put((heuristic(stones_cur_pos, switches_pos), (next_pos_y, next_pos_x), tmp_stones_cur_pos, path + [move], cost))
            node_counter += 1
    
    return None, None, None
            
            
            
        
def launch(file_name):
    map_data = []
    stone_costs = []
    
    map_data, stone_costs = loadMap(file_name)
    
    
    solution, total_cost, node_counter = solve(map_data, stone_costs)
    
    
    return solution, total_cost, node_counter
