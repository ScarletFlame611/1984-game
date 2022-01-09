import pygame
import global_peremen
import sys


# Это класс кнопочки:
class Button:
    def __init__(self, text, x, y):  # текст и координаты считывает
        font = pygame.font.Font(None, 50)
        self.text = text
        self.font_light = font.render(text, True, (100, 255, 255))
        self.font = font.render(text, True, (100, 100, 100))
        self.size = self.w, self.h = self.font.get_width() + 10, self.font.get_height() + 10
        self.cords = self.x, self.y = x - self.font.get_width() // 2, y
        # а размер под текст настривает

    def render(self, screen):  # это, тип, обычные кнопочки
        color = pygame.Color(100, 100, 100)
        pygame.draw.rect(screen, color, (self.x - 5, self.y - 5, self.w, self.h), 2)
        screen.blit(self.font, (self.x, self.y))

    def mouse_on(self, screen):  # а это, мол, выделенные кнопочки рендерит
        color = pygame.Color(200, 255, 255)
        shadow_surface = pygame.Surface((self.w + 100, self.h + 100), pygame.SRCALPHA)
        light_surface = pygame.Surface((self.w + 100, self.h + 100), pygame.SRCALPHA)
        shadow = pygame.Color(0, 150, 200, 100)
        light = pygame.Color(0, 150, 200, 200)
        ###
        pygame.draw.rect(shadow_surface, shadow, (0, 0, self.w + 4, self.h + 4), 10)
        screen.blit(shadow_surface, (self.x - 8, self.y - 8))
        pygame.draw.rect(light_surface, light, (0, 0, self.w + 1, self.h + 1), 6)
        screen.blit(light_surface, (self.x - 6, self.y - 6))
        pygame.draw.rect(screen, color, (self.x - 5, self.y - 5, self.w, self.h), 2)
        screen.blit(self.font_light, (self.x, self.y))

    def click_on(self):  # это на случай, если мы тыкнем на кнопочку ._.
        return self.text

    def is_mouse_on(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h


class Menu:
    def __init__(self):
        self.start = Button("New game", global_peremen.WIDTH // 2, global_peremen.HIGH // 3)
        self.start.render(global_peremen.screen)
        self.cont = Button("Continue game", global_peremen.WIDTH // 2, global_peremen.HIGH // 2)
        self.cont.render(global_peremen.screen)
        self.close = Button("Close", global_peremen.WIDTH // 2, global_peremen.HIGH // 1.5)
        self.close.render(global_peremen.screen)
        self.btns_menu = (self.start, self.cont, self.close)

    def update(self, events):
        for btn in self.btns_menu:
            btn.render(global_peremen.screen)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.btns_menu:
                    if btn.is_mouse_on(*event.pos):
                        clicked_button = btn.click_on()
                        if clicked_button == "Close":
                            pygame.quit()
                            sys.exit()
                        elif clicked_button == 'New game':
                            global_peremen.MOD = 'in_game_menu'
        pos = pygame.mouse.get_pos()
        for btn in self.btns_menu:
            if btn.is_mouse_on(*pos):
                btn.mouse_on(global_peremen.screen)
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