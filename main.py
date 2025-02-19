from BFS import *
from map_processor import *
from A_star import *

file_name = "./data/myfile.txt"
grid, costs = GetMapFromFile(file_name)
print(grid)
print(costs)
ares_pos, stones = find_pos(grid)
print(stones)
switches = find_switches(grid)
print(switches)

if ares_pos and stones:
    #path, totalCost = order_bfs(grid, ares_pos, stones, costs)
    path, totalCost = order_A_star(grid, ares_pos, stones, costs, switches)
    if path:
        print("Path found:", ''.join(path))
        print("Total cost: ", totalCost)
    else:
        print("No valid path found.")
else:
    print("Invalid map: Missing Ares or stones.")
