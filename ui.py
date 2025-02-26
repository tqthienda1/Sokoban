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
left_arrow = pygame.image.load("assets/left_arrow.png")
right_arrow = pygame.image.load("assets/right_arrow.png")
left_arrow_width, left_arrow_height = left_arrow.get_size()
right_arrow_width, right_arrow_height = right_arrow.get_size()
left_arrow = pygame.transform.scale(left_arrow, (left_arrow_width * 0.5, left_arrow_height * 0.5))
right_arrow = pygame.transform.scale(right_arrow, (right_arrow_width * 0.5, right_arrow_height * 0.5))
left_arrow_width, left_arrow_height = left_arrow.get_size()
right_arrow_width, right_arrow_height = right_arrow.get_size()
level1 = pygame.image.load("assets/level1.png")
level1_width, level1_height = level1.get_size()
level_button1 = pygame.image.load("assets/lv1_button.png")
level_button1_width, level_button1_height = level_button1.get_size()
level_button1 = pygame.transform.scale(level_button1, (level_button1_width * 0.7, level_button1_height * 0.7))
level_button1_width, level_button1_height = level_button1.get_size()
level2 = pygame.image.load("assets/level2.png")
level2_width, level2_height = level2.get_size()
level_button2 = pygame.image.load("assets/lv2_button.png")
level_button2_width, level_button2_height = level_button2.get_size()
level_button2 = pygame.transform.scale(level_button2, (level_button2_width * 0.7, level_button2_height * 0.7))
level_button2_width, level_button2_height = level_button2.get_size()
level3 = pygame.image.load("assets/level3.png")
level3 = pygame.transform.scale(level3, (level1_width, level1_height))
level3_width, level3_height = level3.get_size()
level_button3 = pygame.image.load("assets/lv3_button.png")
level_button3_width, level_button3_height = level_button3.get_size()
level_button3 = pygame.transform.scale(level_button3, (level_button3_width * 0.7, level_button3_height * 0.7))
level_button3_width, level_button3_height = level_button3.get_size()
level4 = pygame.image.load("assets/level4.png")
level4_width, level4_height = level4.get_size()
level_button4 = pygame.image.load("assets/lv4_button.png")
level_button4_width, level_button4_height = level_button4.get_size()
level_button4 = pygame.transform.scale(level_button4, (level_button4_width * 0.7, level_button4_height * 0.7))
level_button4_width, level_button4_height = level_button4.get_size()
level5 = pygame.image.load("assets/level5.png")
level5_width, level5_height = level5.get_size()
level_button5 = pygame.image.load("assets/lv5_button.png")
level_button5_width, level_button5_height = level_button5.get_size()
level_button5 = pygame.transform.scale(level_button5, (level_button5_width * 0.7, level_button5_height * 0.7))
level_button5_width, level_button5_height = level_button5.get_size()
level6 = pygame.image.load("assets/level6.png")
level6 = pygame.transform.scale(level6, (level1_width, level1_height))
level6_width, level6_height = level6.get_size()
level_button6 = pygame.image.load("assets/lv6_button.png")
level_button6_width, level_button6_height = level_button6.get_size()
level_button6 = pygame.transform.scale(level_button6, (level_button6_width * 0.7, level_button6_height * 0.7))
level_button6_width, level_button6_height = level_button6.get_size()
level7 = pygame.image.load("assets/level7.png")
level7_width, level7_height = level7.get_size()
level_button7 = pygame.image.load("assets/lv7_button.png")
level_button7_width, level_button7_height = level_button7.get_size()
level_button7 = pygame.transform.scale(level_button7, (level_button7_width * 0.7, level_button7_height * 0.7))
level_button7_width, level_button7_height = level_button7.get_size()
level8 = pygame.image.load("assets/level8.png")
level8_width, level8_height = level8.get_size()
level_button8 = pygame.image.load("assets/lv8_button.png")
level_button8_width, level_button8_height = level_button8.get_size()
level_button8 = pygame.transform.scale(level_button8, (level_button8_width * 0.7, level_button8_height * 0.7))
level_button8_width, level_button8_height = level_button8.get_size()
level9 = pygame.image.load("assets/level9.png")
level9 = pygame.transform.scale(level9, (level1_width, level1_height))
level9_width, level9_height = level9.get_size()
level_button9 = pygame.image.load("assets/lv9_button.png")
level_button9_width, level_button9_height = level_button9.get_size()
level_button9 = pygame.transform.scale(level_button9, (level_button9_width * 0.7, level_button9_height * 0.7))
level_button9_width, level_button9_height = level_button9.get_size()
level10 = pygame.image.load("assets/level10.png")
level10 = pygame.transform.scale(level10, (level1_width, level1_height))
level10_width, level10_height = level10.get_size()
level_button10 = pygame.image.load("assets/lv10_button.png")
level_button10_width, level_button10_height = level_button10.get_size()
level_button10 = pygame.transform.scale(level_button10, (level_button10_width * 0.7, level_button10_height * 0.7))
level_button10_width, level_button10_height = level_button10.get_size()

left_arrow_rect = left_arrow.get_rect()
left_arrow_rect.topleft = ((WIDTH - left_arrow_rect.width) * 0.25, (HEIGHT - left_arrow_rect.height) / 2)
right_arrow_rect = right_arrow.get_rect()
right_arrow_rect.topleft = ((WIDTH - right_arrow_rect.width) * 0.75, (HEIGHT - right_arrow_rect.height) / 2)

level = 1

while is_running:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if left_arrow_rect.collidepoint(event.pos):
                if level == 1:
                    level = 10
                else:
                    level -= 1
            elif right_arrow_rect.collidepoint(event.pos):
                if level == 10:
                    level = 1
                else:
                    level += 1
                

    window_surface.blit(background_menu, (0, 0))
    window_surface.blit(logo, ((WIDTH - logo_width) / 2, HEIGHT / 10))
    if level == 1:
        window_surface.blit(level1, ((WIDTH - level1_width) / 2, (HEIGHT - level1_height) / 2))
        window_surface.blit(level_button1, ((WIDTH - level_button1_width) / 2, HEIGHT * 0.8))
    elif level == 2:
        window_surface.blit(level2, ((WIDTH - level2_width) / 2, (HEIGHT - level2_height) / 2))
        window_surface.blit(level_button2, ((WIDTH - level_button2_width) / 2, HEIGHT * 0.8))
    elif level == 3:
        window_surface.blit(level3, ((WIDTH - level3_width) / 2, (HEIGHT - level3_height) / 2))
        window_surface.blit(level_button3, ((WIDTH - level_button3_width) / 2, HEIGHT * 0.8))
    elif level == 4:
        window_surface.blit(level4, ((WIDTH - level4_width) / 2, (HEIGHT - level4_height) / 2))
        window_surface.blit(level_button4, ((WIDTH - level_button3_width) / 2, HEIGHT * 0.8))
    elif level == 5:
        window_surface.blit(level5, ((WIDTH - level5_width) / 2, (HEIGHT - level5_height) / 2))
        window_surface.blit(level_button5, ((WIDTH - level_button5_width) / 2, HEIGHT * 0.8))
    elif level == 6:
        window_surface.blit(level6, ((WIDTH - level6_width) / 2, (HEIGHT - level6_height) / 2))
        window_surface.blit(level_button6, ((WIDTH - level_button6_width) / 2, HEIGHT * 0.8))
    elif level == 7:
        window_surface.blit(level7, ((WIDTH - level7_width) / 2, (HEIGHT - level7_height) / 2))
        window_surface.blit(level_button7, ((WIDTH - level_button7_width) / 2, HEIGHT * 0.8))
    elif level == 8:
        window_surface.blit(level8, ((WIDTH - level8_width) / 2, (HEIGHT - level8_height) / 2))
        window_surface.blit(level_button8, ((WIDTH - level_button8_width) / 2, HEIGHT * 0.8))
    elif level == 9:
        window_surface.blit(level9, ((WIDTH - level9_width) / 2, (HEIGHT - level9_height) / 2))
        window_surface.blit(level_button9, ((WIDTH - level_button9_width) / 2, HEIGHT * 0.8))
    elif level == 10:
        window_surface.blit(level10, ((WIDTH - level10_width) / 2, (HEIGHT - level10_height) / 2))
        window_surface.blit(level_button10, ((WIDTH - level_button10_width) / 2, HEIGHT * 0.8))
        
    window_surface.blit(left_arrow, ((WIDTH - left_arrow_width) * 0.25, (HEIGHT - left_arrow_height) / 2))
    window_surface.blit(right_arrow, ((WIDTH - right_arrow_width) * 0.75, (HEIGHT - right_arrow_height) / 2))
    

    pygame.display.update()