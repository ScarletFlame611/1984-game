import pygame
from game import *
from menu import *


if __name__ == '__main__':
    pygame.init()
    playing = False
    running = True
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("1984 - Menu")
    while running:
        if not playing:
            result = menu(screen)
            if not result:
                running = False
            else:
                if type(result) != bool:
                    clicked_button = result
                    if clicked_button == "New game":
                        playing = True
                    elif clicked_button == "Continue game":
                        while btn_continue(screen):
                            pass
        else:
            start(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()