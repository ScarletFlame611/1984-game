import pygame
import global_peremen
import sys


class Menu:
    def __init__(self):
        self.start = global_peremen.Button("New game", global_peremen.WIDTH // 2, global_peremen.HIGH // 3, self.new_game)
        self.cont = global_peremen.Button("Continue game", global_peremen.WIDTH // 2, global_peremen.HIGH // 2, self.continuee)
        self.close = global_peremen.Button("Close", global_peremen.WIDTH // 2, global_peremen.HIGH // 1.5, self.close)
        self.btns_menu = (self.start, self.cont, self.close)

    def update(self, events):
        for btn in self.btns_menu:
            btn.render(global_peremen.screen, events)

    def new_game(self):
        global_peremen.MOD = 'in_game_menu'

    def close(self):
        pygame.quit()
        sys.exit()

    def continuee(self):
        pass
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