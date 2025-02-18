from BFS import *
from map_processor import *

file_name = "./data/input-02.txt"
grid, costs = GetMapFromFile(file_name)
print(grid)
print(costs)
ares_pos, stones = find_pos(grid)
print(stones)

if ares_pos and stones:
    path, totalCost = order_bfs(grid, ares_pos, stones, costs)
    if path:
        print("Path found:", ''.join(path))
        print("Total cost: ", totalCost)
    else:
        print("No valid path found.")
else:
    print("Invalid map: Missing Ares or stones.")
