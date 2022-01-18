import pygame
import global_peremen
import sys
import saves
import in_game_menu


class Menu:
    def __init__(self):
        y = global_peremen.HIGH // 5
        self.start = global_peremen.Button("New game", global_peremen.WIDTH // 2, y, self.new_game)
        self.cont = global_peremen.Button("Continue game", global_peremen.WIDTH // 2, self.start.y + self.start.h * 1.5, self.continuee)
        self.settings = global_peremen.Button("Settings", global_peremen.WIDTH // 2, self.cont.y + self.cont.h * 1.5, self.settings)
        self.close = global_peremen.Button("Close", global_peremen.WIDTH // 2, self.settings.y + self.settings.h * 1.5, self.close)
        self.btns_menu = (self.start, self.cont, self.settings, self.close)

    def update(self, events):
        for btn in self.btns_menu:
            btn.render(global_peremen.screen, events)

    def new_game(self):
        global_peremen.choice_menu = None
        global_peremen.MOD = 'name_input'
        global_peremen.in_game_menu = in_game_menu.In_game_menu('bg.png', 'player.png', 'map.png')
        for name in global_peremen.in_game_menu.names:
            global_peremen.levels[name] = 0

    def close(self):
        pygame.quit()
        sys.exit()

    def continuee(self):
        global_peremen.MOD = 'choice_menu'

    def settings(self):
        global_peremen.MOD = 'settings'

'''
    def btn_continue(self, screen):
        global x, y
        screen.fill((10, 10, 10))
        some = Button("Something", 300, 100)
        some.render(screen)
        some1 = Button("Something too", 250, 175)
        some1.render(screen)
        back = Button("Back", 10, 300)
        back.render(screen)
        btns_continue = (some, some1, back)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for btn in btns_continue:
                    if btn.is_mouse_on(x, y):
                        if btn.click_on() == "Back":
                            return False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
        if x and y:
            for btn in btns_continue:
                if btn.is_mouse_on(x, y):
                    btn.mouse_on(screen)
'''
menu = Menu()