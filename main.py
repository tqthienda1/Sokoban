import time
import tracemalloc
import textwrap

from BFS import *
from gbfs import *
from helper import *
from UCS import *
from DFS import *
from A_star import *
from dijkstra import *


def main():
    choose_map = int(input("Choose map from 1-10: "))
    num = "10"
    
    if choose_map == 1:
        num = "01"
    elif choose_map == 2:
        num = "02"
        
    elif choose_map == 3:
        num = "03"
    
    elif choose_map == 4:
        num = "04"
        
    elif choose_map == 5:
        num = "05"
    
    elif choose_map == 6:
        num = "06"
        
    elif choose_map == 7:
        num = "07"
        
    elif choose_map == 8:
        num = "08"
    
    elif choose_map == 9:
        num = "09"
    
    else:
        pass
    file_name = f"./Inputs/input-{num}.txt"
    grid, costs = GetMapFromFile(file_name)
    print(f"Map was chosen: input-{num}.txt")
    print(grid)
    ares_pos, stones, switches = find_pos(grid)

    if ares_pos and stones:
        
        path, totalCost, algorithm, node_counter = None, None, None, None
        
        file_output = "./Outputs/" + file_name.split('/')[2].replace("in", "out")
        with open(file_output, 'w') as file:
            file.write("Map: " + file_name.split('/')[2] + "\n\n")
            for choice in range(1, 7):
                tracemalloc.start()
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
                elif choice == 6:
                    algorithm = "Dijkstra"
                    
                    path, totalCost, node_counter = launchDijkstra(file_name)
                    
                elapsed_time = time.time() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                memory_used = peak / 1024**2
                
                file.write(algorithm + '\n')
                
                if path:
                    file.write(f"Steps: {len(path)}, Weight: {totalCost}, Node: {node_counter}, Time(ms): {round(elapsed_time * 1000, 3)}, Memory(MB) {memory_used:.2f}\n")
                    file.write(textwrap.fill("".join(path), width=100) + "\n\n")
                else:
                    file.write("No solution\n\n")
                
                
                
            


            

    else:
        print("\nInvalid map: Missing Ares or stones.")
        


if __name__ == "__main__":
    main()