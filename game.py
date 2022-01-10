import pygame
import create_level
import menu
import sys
import global_peremen
import in_game_menu


if __name__ == '__main__':
    pygame.display.set_caption('project')
    while True:
        global_peremen.screen.fill(pygame.Color(0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if global_peremen.MOD == 'main_menu':
            menu.menu.update(events)
        if global_peremen.MOD == 'in_game_menu':
            in_game_menu.in_game_menu.update(events)
        global_peremen.clock.tick(global_peremen.fps)
        pygame.display.update()