import create_level
import menu
import sys
import global_peremen
import in_game_menu
import pygame
import fight


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
        if "level" in global_peremen.MOD:
            number = global_peremen.MOD[-1]
            name_level = "level" + number
            now_level = create_level.level(name_level)
            now_level.generate_level()
            now_level.play()
            global_peremen.MOD = "play"
        if global_peremen.MOD == 'play' or global_peremen.MOD == 'fight_start':
            now_level.play()

        global_peremen.clock.tick(global_peremen.fps)
        pygame.display.update()

