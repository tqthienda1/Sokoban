import pygame
import numpy as np
import time
import tracemalloc

from BFS import *
from gbfs import *
from helper import *
from UCS import *
from DFS import *
from A_star import *
from dijkstra import *

WALL = '#'
STONE = '$'
ARES = '@'
SWITCH = '.'
STONE_ON_SWITCH = '*'
ARES_ON_SWITCH = '+'
FLOOR = ' '

pygame.init()
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
CELL_SIZE = screen_height / 30

def load_images():
    return {
        WALL: pygame.image.load("assets/wall.png"),
        STONE: pygame.image.load("assets/box_not_on_switch.png"),
        ARES: pygame.image.load("assets/steve.png"),
        SWITCH: pygame.image.load("assets/switch.png"),
        STONE_ON_SWITCH: pygame.image.load("assets/box_on_switch.png"),
        ARES_ON_SWITCH: pygame.image.load("assets/herobrine.png"),
        FLOOR: pygame.image.load("assets/floor.png")
    }

def load_map(filename):
    game_map, weights = GetMapFromFile(filename)
    return game_map, weights

def draw_map(screen, game_map, images, screen_width, screen_height, square_size):
    rows, cols = game_map.shape

    center_x_start = (screen_width - square_size) / 2
    center_x_end = screen_width - center_x_start
    center_width = center_x_end - center_x_start

    map_width = cols * CELL_SIZE
    map_height = rows * CELL_SIZE

    offset_x = center_x_start + (center_width - map_width) // 2
    offset_y = (screen_height - map_height) // 2

    for y in range(rows):
        for x in range(cols):
            cell_type = game_map[y, x]
            if cell_type in images:
                image = pygame.transform.scale(images[cell_type], (CELL_SIZE, CELL_SIZE))
                screen.blit(image, (x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y))

            center_x_start = (screen_width - square_size) / 2

    return offset_x, offset_y 

def find_player(game_map):
    positions = np.where((game_map == ARES) | (game_map == ARES_ON_SWITCH))
    return positions[0][0], positions[1][0] if len(positions[0]) > 0 else None

def move_ares(game_map, path):
    direction_map = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1),
                     'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    
    for move in path:
        dx, dy = direction_map[move]
        px, py = find_player(game_map)
        nx, ny = px + dx, py + dy 
        nnx, nny = nx + dx, ny + dy 

        if game_map[nx, ny] in [STONE, STONE_ON_SWITCH]:
            if game_map[nnx, nny] in [' ', SWITCH]: 
                game_map[nnx, nny] = STONE_ON_SWITCH if game_map[nnx, nny] == SWITCH else STONE
                game_map[nx, ny] = ARES_ON_SWITCH if game_map[nx, ny] == STONE_ON_SWITCH else ARES
                game_map[px, py] = SWITCH if game_map[px, py] == ARES_ON_SWITCH else ' '
        elif game_map[nx, ny] in [' ', SWITCH]:
            game_map[nx, ny] = ARES_ON_SWITCH if game_map[nx, ny] == SWITCH else ARES
            game_map[px, py] = SWITCH if game_map[px, py] == ARES_ON_SWITCH else ' '

        time.sleep(0.3)
        yield game_map.copy()

def main(file_name):
    pygame.font.init()
    font = pygame.font.Font("assets\MinecraftRegular-Bmg3.otf", 25)
    screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
    square_size = min(screen_width, screen_height)
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)

    game_map, weights = load_map(file_name)
    images = load_images()
    border_tile = pygame.image.load("assets/floor.png")
    border_tile_side = pygame.image.load("assets/oakwood.png")
    border_width, border_height = border_tile.get_size()
    background_tile = pygame.image.load("assets/stoneC.png")
    background_width, background_height = background_tile.get_size()

    path, totalCost, node_counter = None, None, None
    elapsed_time, memory_used = 1, 1
    algorithm = ""

    start_button = pygame.image.load("assets/start.png")
    start_button_width, start_button_height = start_button.get_size()
    start_button = pygame.transform.scale(start_button, (start_button_width * 0.7, start_button_height * 0.7))
    start_button_width, start_button_height = start_button.get_size()
    BFS_button = pygame.image.load("assets/bfs_button.png")
    BFS_button_width, BFS_button_height = BFS_button.get_size()
    BFS_button = pygame.transform.scale(BFS_button, (BFS_button_width * 0.7, BFS_button_height * 0.7))
    BFS_button_width, BFS_button_height = BFS_button.get_size()
    GBFS_button = pygame.image.load("assets/gbfs_button.png")
    GBFS_button_width, GBFS_button_height = GBFS_button.get_size()
    GBFS_button = pygame.transform.scale(GBFS_button, (GBFS_button_width * 0.7, GBFS_button_height * 0.7))
    GBFS_button_width, GBFS_button_height = GBFS_button.get_size()
    UCS_button = pygame.image.load("assets/ucs_button.png")
    UCS_button_width, UCS_button_height = UCS_button.get_size()
    UCS_button = pygame.transform.scale(UCS_button, (UCS_button_width * 0.7, UCS_button_height * 0.7))
    UCS_button_width, UCS_button_height = UCS_button.get_size()
    DFS_button = pygame.image.load("assets/dfs_button.png")
    DFS_button_width, DFS_button_height = DFS_button.get_size()
    DFS_button = pygame.transform.scale(DFS_button, (DFS_button_width * 0.7, DFS_button_height * 0.7))
    DFS_button_width, DFS_button_height = DFS_button.get_size()
    AStar_button = pygame.image.load("assets/astar_button.png")
    AStar_button_width, AStar_button_height = AStar_button.get_size()
    AStar_button = pygame.transform.scale(AStar_button, (AStar_button_width * 0.7, AStar_button_height * 0.7))
    AStar_button_width, AStar_button_height = AStar_button.get_size()
    Dijsktra_button = pygame.image.load("assets/dijkstra_button.png")
    Dijsktra_button_width, Dijsktra_button_height = Dijsktra_button.get_size()
    Dijsktra_button = pygame.transform.scale(Dijsktra_button, (Dijsktra_button_width * 0.7, Dijsktra_button_height * 0.7))
    Dijsktra_button_width, Dijsktra_button_height = Dijsktra_button.get_size()

    start = False
    running = True
    while running:
        screen.fill((255, 255, 255))

        center_x_start = (screen_width - game_map.shape[1] * CELL_SIZE) // 2
        center_x_end = center_x_start + game_map.shape[1] * CELL_SIZE

        center_y_start = (screen_height - game_map.shape[0] * CELL_SIZE) // 2
        center_y_end = center_y_start + game_map.shape[0] * CELL_SIZE

        for x in range(0, screen_width, background_width):
            for y in range(0, screen_height, background_height):
                screen.blit(background_tile, (x, y))

        center_x_start = (screen_width - square_size) / 2
        center_x_end = screen_width - center_x_start 
        center_width = screen_width - 2 * center_x_start

        x = center_x_start
        while x < center_x_end:
            screen.blit(border_tile, (x, 0))
            screen.blit(border_tile, (x, screen_height - border_height))
            x += border_width

        y = 0
        while y < screen_height:
            screen.blit(border_tile, (center_x_start, y))
            screen.blit(border_tile, (center_x_start + center_width - border_width + CELL_SIZE / 8, y))
            y += border_height
        
        x = 0
        y = 0
        while x < center_x_start:
            y = 0
            while y < screen_height:
                screen.blit(border_tile_side, (x - CELL_SIZE / 2, y))
                screen.blit(border_tile_side, (x + center_x_start + center_width + CELL_SIZE / 8, y))
                y += border_height
            x += border_width

        y = screen_height / 7
        screen.blit(BFS_button, (screen_width - square_size - center_x_start - BFS_button_width, y))
        BFS_button_rect = BFS_button.get_rect()
        BFS_button_rect.topleft = ((screen_width - square_size - center_x_start - GBFS_button_width, y))
        y += 100
        screen.blit(GBFS_button, (screen_width - square_size - center_x_start - GBFS_button_width, y))
        GBFS_button_rect = GBFS_button.get_rect()
        GBFS_button_rect.topleft = ((screen_width - square_size - center_x_start - BFS_button_width, y))
        y += 100
        screen.blit(UCS_button, (screen_width - square_size - center_x_start - UCS_button_width, y))
        UCS_button_rect = UCS_button.get_rect()
        UCS_button_rect.topleft = ((screen_width - square_size - center_x_start - BFS_button_width, y))
        y += 100
        screen.blit(DFS_button, (screen_width - square_size - center_x_start - DFS_button_width, y))
        DFS_button_rect = DFS_button.get_rect()
        DFS_button_rect.topleft = ((screen_width - square_size - center_x_start - BFS_button_width, y))
        y += 100
        screen.blit(AStar_button, (screen_width - square_size - center_x_start - AStar_button_width, y))
        AStar_button_rect = AStar_button.get_rect()
        AStar_button_rect.topleft = ((screen_width - square_size - center_x_start - BFS_button_width, y))
        y += 100
        screen.blit(Dijsktra_button, (screen_width - square_size - center_x_start - Dijsktra_button_width, y))
        Dijsktra_button_rect = Dijsktra_button.get_rect()
        Dijsktra_button_rect.topleft = ((screen_width - square_size - center_x_start - BFS_button_width, y))
        y += 250
        screen.blit(start_button, (screen_width - square_size - center_x_start - start_button_width, y))
        start_button_rect = start_button.get_rect()
        start_button_rect.topleft = ((screen_width - square_size - center_x_start - BFS_button_width, y))


        for event in pygame.event.get():
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if (start_button_rect.collidepoint(event.pos)):
                    start = True
                elif (BFS_button_rect.collidepoint(event.pos)):
                    algorithm = "Breadth-First Search"
                    ares_pos, stones, switches = find_pos(game_map)
                    tracemalloc.start()
                    start_time = time.time()
                    path, totalCost, node_counter = order_bfs(game_map, ares_pos, stones, weights)
                    elapsed_time = time.time() - start_time
                    memory_used = tracemalloc.get_traced_memory()[1] / 1024**2
                    tracemalloc.stop()

                    clock = pygame.time.Clock()
                    path_gen = move_ares(game_map, path)
                elif (GBFS_button_rect.collidepoint(event.pos)):
                    algorithm = "Greedy Best-First Search"
                    ares_pos, stones, switches = find_pos(game_map)
                    tracemalloc.start()
                    start_time = time.time()
                    path, totalCost, node_counter = launch(file_name)
                    elapsed_time = time.time() - start_time
                    memory_used = tracemalloc.get_traced_memory()[1] / 1024**2
                    tracemalloc.stop()

                    clock = pygame.time.Clock()
                    path_gen = move_ares(game_map, path)
                elif (UCS_button_rect.collidepoint(event.pos)):
                    algorithm = "Uniform-Cost Search"
                    ares_pos, stones, switches = find_pos(game_map)
                    tracemalloc.start()
                    start_time = time.time()
                    path, totalCost, node_counter = launchUCS(file_name)
                    elapsed_time = time.time() - start_time
                    memory_used = tracemalloc.get_traced_memory()[1] / 1024**2
                    tracemalloc.stop()

                    clock = pygame.time.Clock()
                    path_gen = move_ares(game_map, path)
                elif (DFS_button_rect.collidepoint(event.pos)):
                    algorithm = "Depth-First Search"
                    ares_pos, stones, switches = find_pos(game_map)
                    tracemalloc.start()
                    start_time = time.time()
                    path, totalCost, node_counter = launchDFS(file_name)
                    elapsed_time = time.time() - start_time
                    memory_used = tracemalloc.get_traced_memory()[1] / 1024**2
                    tracemalloc.stop()

                    clock = pygame.time.Clock()
                    path_gen = move_ares(game_map, path)
                elif (AStar_button_rect.collidepoint(event.pos)):
                    algorithm = "A* Search"
                    ares_pos, stones, switches = find_pos(game_map)
                    tracemalloc.start()
                    start_time = time.time()
                    path, totalCost, node_counter = order_A_star(game_map, ares_pos, stones, weights, switches)
                    elapsed_time = time.time() - start_time
                    memory_used = tracemalloc.get_traced_memory()[1] / 1024**2
                    tracemalloc.stop()

                    clock = pygame.time.Clock()
                    path_gen = move_ares(game_map, path)
                elif (Dijsktra_button_rect.collidepoint(event.pos)):
                    algorithm = "Dijsktra Search"
                    ares_pos, stones, switches = find_pos(game_map)
                    tracemalloc.start()
                    start_time = time.time()
                    path, totalCost, node_counter = launchDijkstra(file_name)
                    path, totalCost, node_counter = order_A_star(game_map, ares_pos, stones, weights, switches)
                    elapsed_time = time.time() - start_time
                    memory_used = tracemalloc.get_traced_memory()[1] / 1024**2
                    tracemalloc.stop()

                    clock = pygame.time.Clock()
                    path_gen = move_ares(game_map, path)

        y = (screen_height / 4) - 200
        text_surface = font.render(algorithm, True, (255, 255, 255))
        screen.blit(text_surface, (center_x_start + center_width + CELL_SIZE, y))

        info_text = [
            f"Steps: {len(path) if path is not None else 0}",
            f"Weight: {totalCost}",
            f"Node: {node_counter}",
            f"Time(ms): {round(elapsed_time * 1000, 3)}",
            f"Memory(MB): {memory_used:.2f}"
        ]

        clock = pygame.time.Clock()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        
        offset_x, offset_y = draw_map(screen, game_map, images, screen_width, screen_height, square_size)

        if(start == True):      
                try:
                    game_map = next(path_gen)
                except StopIteration:
                    y = screen_height / 4 
                    for line in info_text:
                        text_surface = font.render(line, True, (255, 255, 255))
                        screen.blit(text_surface, (center_x_start + center_width + 64, y))
                        y += 100 
                        
                    pass

        pygame.display.flip()
        clock.tick(5)
    pygame.quit()

