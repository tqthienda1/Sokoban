

def loadMap(file_name):
    map_data = []
    stone_costs = []
    
    with open(file_name, 'r') as file:
        stone_costs = list(map(int, file.readline().strip().split()))
        
        map_data = [line.rstrip() for line in file.readlines()]
    
    return map_data, stone_costs

def heuristicCalc(start, end):
    start_y, start_x = start
    end_y, end_x = end
    
    return abs(end_y - start_y) + abs(end_x - start_x)

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
 
def solve(map_data, stone_costs):
    directions = [[-1, 0, 'U', 'u', 0], [1, 0, 'D', 'd', 0], [0, -1, 'L', 'l', 0], [0, 1, 'R', 'r', 0]]
    ares_first_pos, stones_first_pos, switches_pos = findPos(map_data)
    frontier = [(ares_first_pos, stones_first_pos, [], 0)]
    explored = set()
    
    while(True):
        if frontier == []:
            return "No solution"
        
        ares_cur_pos, stones_cur_pos, path, cost = frontier.pop(0)
        ares_cur_pos_y, ares_cur_pos_x = ares_cur_pos
        
        if (ares_cur_pos, tuple(stones_cur_pos)) in explored:
            continue
        explored.add((ares_cur_pos, tuple(stones_cur_pos)))
        
        if goal(map_data, stones_cur_pos):
            return path, cost
        
        for index, (dy, dx, push, move, _) in enumerate(directions):
            next_pos_y, next_pos_x = dy + ares_cur_pos_y, dx + ares_cur_pos_x
            
            if (next_pos_y, next_pos_x) not in stones_cur_pos:
                for each_stone in stones_cur_pos:
                    directions[index][4] = heuristicCalc((next_pos_y, next_pos_x), each_stone)
            else:
                for each_switch in switches_pos:
                    directions[index][4] = heuristicCalc((next_pos_y, next_pos_x), each_switch)
        
        directions.sort(key=lambda x: x[-1])
        
        
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
                tmp_stones_cur_pos[num_stone_explored] = (new_stone_pos_y, new_stone_pos_x)
                is_pushed = True
                

            if is_pushed:
                frontier.append(((next_pos_y, next_pos_x), tmp_stones_cur_pos, path + [push], cost + 1 + stone_costs[num_stone_explored]))
            else:
                frontier.append(((next_pos_y, next_pos_x), tmp_stones_cur_pos, path + [move], cost + 1))
            
            
        
        

def main():
    map_data = []
    stone_costs = []
    file_name = "./Inputs/input-02.txt"
    
    map_data, stone_costs = loadMap(file_name)
    
    print(map_data, stone_costs)
    
    solution, total_cost = solve(map_data, stone_costs)
    
    print(solution, total_cost)
    
if __name__ == "__main__":
    main()
