import pygame
import numpy as np
import time
import tracemalloc
from DFS import *  # Sử dụng thuật toán DFS
from UCS import *
from BFS import *

# Định nghĩa các ký hiệu trên bản đồ
WALL = '#'
STONE = '$'
ARES = '@'
SWITCH = '.'
STONE_ON_SWITCH = '*'
ARES_ON_SWITCH = '+'
FLOOR = ' '

# Màu sắc tương ứng

CELL_SIZE = 64

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

    # Xác định phần giữa màn hình
    center_x_start = (screen_width - square_size) / 2
    center_x_end = screen_width - center_x_start
    center_width = center_x_end - center_x_start

    # Căn giữa game map trong phần giữa
    map_width = cols * CELL_SIZE
    map_height = rows * CELL_SIZE

    offset_x = center_x_start + (center_width - map_width) // 2
    offset_y = (screen_height - map_height) // 2  # Căn giữa theo chiều dọc

    # Vẽ bản đồ game
    for y in range(rows):
        for x in range(cols):
            cell_type = game_map[y, x]
            if cell_type in images:
                image = pygame.transform.scale(images[cell_type], (CELL_SIZE, CELL_SIZE))
                screen.blit(image, (x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y))

            center_x_start = (screen_width - square_size) / 2

    return offset_x, offset_y  # Trả về vị trí căn chỉnh để dùng trong di chuyển

def find_player(game_map):
    positions = np.where((game_map == ARES) | (game_map == ARES_ON_SWITCH))
    return positions[0][0], positions[1][0] if len(positions[0]) > 0 else None

def move_ares(game_map, path):
    direction_map = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1),
                     'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    
    for move in path:
        dx, dy = direction_map[move]
        px, py = find_player(game_map)
        nx, ny = px + dx, py + dy  # Vị trí tiếp theo của Ares
        nnx, nny = nx + dx, ny + dy  # Ô tiếp theo của viên đá nếu bị đẩy

        if game_map[nx, ny] in [STONE, STONE_ON_SWITCH]:  # Nếu Ares gặp đá
            if game_map[nnx, nny] in [' ', SWITCH]:  # Kiểm tra xem có thể đẩy đá không
                # Di chuyển viên đá
                game_map[nnx, nny] = STONE_ON_SWITCH if game_map[nnx, nny] == SWITCH else STONE
                game_map[nx, ny] = ARES_ON_SWITCH if game_map[nx, ny] == STONE_ON_SWITCH else ARES
                game_map[px, py] = SWITCH if game_map[px, py] == ARES_ON_SWITCH else ' '
        elif game_map[nx, ny] in [' ', SWITCH]:  # Nếu Ares có thể đi tới
            game_map[nx, ny] = ARES_ON_SWITCH if game_map[nx, ny] == SWITCH else ARES
            game_map[px, py] = SWITCH if game_map[px, py] == ARES_ON_SWITCH else ' '

        time.sleep(0.3)  # Hiệu ứng di chuyển chậm lại
        yield game_map.copy()

def main(file_name):
    pygame.init()
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

    tracemalloc.start()
    start_time = time.time()
    solution, total_cost, node_counter = launchUCS(file_name)  # Gọi thuật toán DFS
    elapsed_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    memory_used = peak / 1024**2

    clock = pygame.time.Clock()
    offset_x, offset_y = 0, 0  # Giá trị mặc định

    path_gen = move_ares(game_map, solution)
    start_button = pygame.image.load("assets/start.png")
    start_width, start_height = start_button.get_size()
    start_button_rect = start_button.get_rect()
    start = False
    running = True
    while running:
        screen.fill((255, 255, 255))  # Màu nền

        # Xác định phạm vi trung tâm màn hình
        center_x_start = (screen_width - game_map.shape[1] * CELL_SIZE) // 2
        center_x_end = center_x_start + game_map.shape[1] * CELL_SIZE

        center_y_start = (screen_height - game_map.shape[0] * CELL_SIZE) // 2
        center_y_end = center_y_start + game_map.shape[0] * CELL_SIZE

        # Lót nền trong phạm vi màn hình nhưng không tràn vào vùng bản đồ
        for x in range(0, screen_width, background_width):
            for y in range(0, screen_height, background_height):
                screen.blit(background_tile, (x, y))

        center_x_start = (screen_width - square_size) / 2
        center_x_end = screen_width - center_x_start 
        center_width = screen_width - 2 * center_x_start

        # Tạo viền trên
        x = center_x_start
        while x < center_x_end:
            screen.blit(border_tile, (x, 0))
            screen.blit(border_tile, (x, screen_height - border_height))
            x += border_width

        y = 0
        while y < screen_height:
            screen.blit(border_tile, (center_x_start, y))
            screen.blit(border_tile, (center_x_start + center_width - border_width + 8, y))
            y += border_height
        
        #tạo viền 2 khung 2 bên
        x = 0
        while x < center_x_start:
            screen.blit(border_tile_side, (x - 32, 0))
            screen.blit(border_tile_side, (x - 32, screen_height - border_height))
            screen.blit(border_tile_side, (x + center_x_start + center_width + 8, 0))
            screen.blit(border_tile_side, (x + center_x_start + center_width + 8, screen_height - border_height))
            x += border_width

        y = 0
        while y < screen_height:
            screen.blit(border_tile_side, (0, y))
            screen.blit(border_tile_side, (center_x_start - border_width, y))
            screen.blit(border_tile_side, (center_x_start + center_width + 8, y))
            screen.blit(border_tile_side, (2 * center_x_start + center_width - border_width, y))
            y += border_height
    
        info_text = [
            f"Steps: {len(solution)}",
            f"Weight: {total_cost}",
            f"Node: {node_counter}",
            f"Time(ms): {round(elapsed_time * 1000, 3)}",
            f"Memory(MB): {memory_used:.2f}"
        ]

        screen.blit(start_button, (84, 104))
        start_button_rect.topleft = ((84, 104))
        
        y_offset = screen_height / 4  # Khoảng cách từ trên xuống
        for line in info_text:
            text_surface = font.render(line, True, (255, 255, 255))  # Màu đen
            screen.blit(text_surface, (center_x_start + center_width + 92, y_offset))
            y_offset += 100  # Tăng vị trí xuống mỗi dòng
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Nhấn ESC để thoát toàn màn hình

        
        offset_x, offset_y = draw_map(screen, game_map, images, screen_width, screen_height, square_size)

        if (event.type == pygame.MOUSEBUTTONDOWN):
            if(start_button_rect.collidepoint(event.pos)):
                start = True

        if(start == True) :      
            try:
                game_map = next(path_gen)
            except StopIteration:
                pass  # Kết thúc di chuyển

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

