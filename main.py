import time
import psutil
import os

from BFS import *
from gbfs import *
from helper import *
from UCS import *
from DFS import *
from A_star import *


def main():
    file_name = "./Inputs/input-01.txt"
    grid, costs = GetMapFromFile(file_name)
    print(grid)
    print(costs)
    ares_pos, stones, switches = find_pos(grid)
    print(stones)
    print(switches)

    if ares_pos and stones:
        
        path, totalCost, algorithm, node_counter = None, None, None, None
        

        
        process = psutil.Process(os.getpid())  
        memory_used = process.memory_info().rss / 1024**2 
        
        file_output = "./Outputs/" + file_name.split('/')[2].replace("in", "out")
        with open(file_output, 'w') as file:
            file.write("Map: " + file_name.split('/')[2] + "\n\n")
            for choice in range(1, 6):
                start_time = time.time()
    
                if choice == 1:
                    algorithm = "BFS"
                    
                    path, totalCost, node_counter = order_bfs(grid, ares_pos, stones, costs)
                elif choice == 2:
                    algorithm = "GBFS"
                    
                    path, totalCost, node_counter = launch(file_name)
                elif choice == 3:
                    algorithm = "UCS"
                    
                    path, totalCost, node_counter = launchUCS(file_name)
                elif choice == 4:
                    algorithm = "DFS"
                    
                    path, totalCost, node_counter = launchDFS(file_name)
                elif choice == 5:
                    algorithm = "A*"
                    
                    path, totalCost, node_counter = order_A_star(grid, ares_pos, stones, costs, switches)
                    
                elapsed_time = time.time() - start_time
                
                if path:
                    file.write(algorithm + '\n')
                    file.write(f"Steps: {len(path)}, Weight: {totalCost}, Node: {node_counter}, Time(ms): {round(elapsed_time * 1000, 3)}, Memory(MB) {memory_used:.2f}\n\n")
                else:
                    file.write("No solution")
                    break
                
                
                
            


            

    else:
        print("\nInvalid map: Missing Ares or stones.")
        


if __name__ == "__main__":
    main()