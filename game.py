import create_level
import menu
import sys
import global_peremen
import in_game_menu
import pygame
import fight
import saves
import choice_menu
import settings


def play():
    global_peremen.run = True
    pygame.display.set_caption('жмых')
    global_peremen.in_game_menu = in_game_menu.In_game_menu('bg.png', 'player.png', 'map.png')
    while global_peremen.run:
        global_peremen.screen.fill(pygame.Color(0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                if global_peremen.MOD == 'in_game_menu' or global_peremen.MOD in ('play', 'fight_start', 'fight'):
                    saves.save()
                pygame.quit()
                sys.exit()
        if global_peremen.MOD == 'main_menu':
            menu.menu.update(events)
        if global_peremen.MOD == 'in_game_menu':
            global_peremen.in_game_menu.update(events)
        if "level" in global_peremen.MOD:
            now_level = create_level.Level(global_peremen.MOD)
            now_level.generate_level()
            now_level.play(events)
            global_peremen.MOD = "play"
        if global_peremen.MOD in ('play', 'fight_start', 'fight'):
            now_level.play(events)
        if global_peremen.MOD == 'name_input':
            if global_peremen.enter_nam is None:
                global_peremen.enter_name(((global_peremen.WIDTH // 2) - (global_peremen.WIDTH // 4),
                                           global_peremen.HIGH // 2 - global_peremen.HIGH // 20),
                                          (global_peremen.WIDTH // 2, global_peremen.HIGH // 10))
            global_peremen.enter_nam.update(events)
        if global_peremen.MOD == 'choice_menu':
            if global_peremen.choice_menu is None:
                global_peremen.choice_menu = choice_menu.Choice_menu()
            global_peremen.choice_menu.update(events)
        if global_peremen.MOD == 'settings':
            settings.settings.update(events)
        global_peremen.clock.tick(global_peremen.fps)
        pygame.display.update()


if __name__ == '__main__':
    while global_peremen.new_game:
        global_peremen.new_game = False
        menu.menu = menu.Menu()
        settings.settings = settings.Settings()
        play()
