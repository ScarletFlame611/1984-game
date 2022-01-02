import pygame


# Это класс кнопочки:
class Button:
    def __init__(self, text, x, y):  # текст и координаты считывает
        self.cords = self.x, self.y = x, y
        font = pygame.font.Font(None, 50)
        self.text = text
        self.font_light = font.render(text, True, (100, 255, 255))
        self.font = font.render(text, True, (100, 100, 100))
        self.size = self.w, self.h = self.font.get_width() + 10, self.font.get_height() + 10
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
        return x > self.x and x < self.x + self.w and y > self.y and y < self.y + self.h


x, y = None, None


# Эта функция меню вызывает:
def menu(screen):
    global btns
    global x, y
    screen.fill((10, 10, 10))
    start = Button("New game", 300, 100)
    start.render(screen)
    cont = Button("Continue game", 250, 175)
    cont.render(screen)
    close = Button("Close", 336, 250)
    close.render(screen)
    btns_menu = (start, cont, close)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for btn in btns_menu:
                if btn.is_mouse_on(x, y):
                    clicked_button = btn.click_on()
                    if clicked_button == "Close":
                        return False
                    else:
                        return clicked_button
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
    if x and y:
        for btn in btns_menu:
            if btn.is_mouse_on(x, y):
                btn.mouse_on(screen)
    return True


def btn_continue(screen):
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
    pygame.display.flip()
    return True