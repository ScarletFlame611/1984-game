import pygame, os

pygame.init()
clock = pygame.time.Clock()
fps = 60
MOD = 'main_menu'
SIZE = WIDTH, HIGH = 900, 500
screen = pygame.display.set_mode(SIZE)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button:
    def __init__(self, text, x, y, function, name_image=None, size=None):  # текст и координаты считывает
        font = pygame.font.Font(None, 50)
        self.text = text
        self.font_light = font.render(text, True, (100, 255, 255))
        self.font = font.render(text, True, (100, 100, 100))
        self.size = self.w, self.h = self.font.get_width() + 10, self.font.get_height() + 10
        self.cords = self.x, self.y = x - self.font.get_width() // 2, y
        self.function = function
        if name_image is not None:
            self.image = pygame.transform.scale(load_image(name_image, colorkey=-1), size)
            self.size = self.w, self.h = size[0], size[1]
        else:
            self.image = None
        # а размер под текст настривает

    def render(self, screen, events):  # это, тип, обычные кнопочки
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.is_mouse_on(*event.pos):
                        self.click_on()
        if self.image is not None:
            screen.blit(self.image, (self.x, self.y))
        else:
            color = pygame.Color(100, 100, 100)
            pygame.draw.rect(screen, color, (self.x - 5, self.y - 5, self.w, self.h), 2)
        screen.blit(self.font, (self.x, self.y))
        if self.is_mouse_on(*pos):
            self.mouse_on(screen)

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
        self.function()

    def is_mouse_on(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h


class Scroll:
    def __init__(self, buttons, x, y):
        self.buttons = buttons
        self.x = x
        self.y = y
        self.step = WIDTH // 15
        self.v = WIDTH // 5
        past_x = 0
        for i in range(len(self.buttons)):
            self.buttons[i].x = past_x + self.step
            self.buttons[i].y = self.y
            past_x = self.buttons[i].x + self.buttons[i].w

    def update(self, events):
        for i in range(len(self.buttons)):
            if self.buttons[i].x <= WIDTH:
                self.buttons[i].render(screen, events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                max_ = max([elem.x + elem.h for elem in self.buttons])
                width = [elem.w for elem in self.buttons if elem.x + elem.h == max_][0]
                if max_ - self.v > WIDTH - width - self.v:
                    for i in range(len(self.buttons)):
                        self.buttons[i].x -= self.v
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                min_ = min([elem.x for elem in self.buttons])
                width = [elem.w for elem in self.buttons if elem.x == min_][0]
                if min_ + self.v < width + self.v:
                    for i in range(len(self.buttons)):
                        self.buttons[i].x += self.v