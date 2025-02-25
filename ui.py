import pygame
from PIL import Image


pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

pygame.display.set_caption('Sokoban')
window_surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)


is_running = True

logo = pygame.image.load("assets/sokoban_logo.png")  
logo_width, logo_height = logo.get_size()
logo = pygame.transform.scale(logo, (logo_width * 1.2, logo_height * 1.2))
logo_width, logo_height = logo.get_size()
background_menu = pygame.image.load("assets/menu_background.png")  
background_menu = pygame.transform.scale(background_menu, (WIDTH, HEIGHT))



while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background_menu, (0, 0))
    window_surface.blit(logo, ((WIDTH - logo_width) / 2, HEIGHT / 10))

    pygame.display.update()