import time
import psutil
import os

from BFS import *
from gbfs import *
from helper import *
from A_star import *
from UCS import *

def main():
    file_name = "./Inputs/myfile.txt"
    grid, costs = GetMapFromFile(file_name)
    print(grid)
    print(costs)
    ares_pos, stones, switches = find_pos(grid)
    print(stones)
    print(switches)

    if ares_pos and stones:
        print("1. Breadth First Search")
        print("2. Greedy Best First Search")
        print("3. A*")
        print("4. UCS")
        choice = int(input("Choose algorithm you want to use: "))
        
        path, totalCost = None, None
        
        start_time = time.time()
        
        if choice == 1:
            path, totalCost = order_bfs(grid, ares_pos, stones, costs)
        elif choice == 2:
            path, totalCost = launch(file_name)
        elif choice == 3:
            path, totalCost = order_A_star(grid, ares_pos, stones, costs, switches)
        elif choice == 4:
            path, totalCost = sokoban_ucs(grid, costs)
        elapsed_time = time.time() - start_time
        
        if path:
            print("\nPath found:", ''.join(path))
            print("Total cost: ", totalCost)
        else:
            print("\nNo valid path found.")
            
        process = psutil.Process(os.getpid())  
        memory_used = process.memory_info().rss / 1024**2 

        print(f"Time exceeded: {round(elapsed_time, 3)}")
        print(f"Memory: {memory_used:.2f} MB")
            

    else:
        print("\nInvalid map: Missing Ares or stones.")
        


if __name__ == "__main__":
    main()