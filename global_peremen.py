import pygame, os
import sys, random

pygame.init()
clock = pygame.time.Clock()
fps = 60
MOD = 'main_menu'
SIZE = WIDTH, HIGH = 900, 500
screen = pygame.display.set_mode(SIZE)
font = pygame.font.Font(None, min(SIZE) // 10)
NAME = ''
enter_nam = None
choice_menu = None
in_game_menu = None


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button:
    def __init__(self, text, x, y, function, name_image=None, size=None, clicable=True, function_peremen=None):  # текст и координаты считывает
        self.text = text
        self.font_light = font.render(text, True, (100, 255, 255))
        self.font = font.render(text, True, (100, 100, 100))
        self.size = self.w, self.h = self.font.get_width() + 10, self.font.get_height() + 10
        self.cords = self.x, self.y = x - self.font.get_width() // 2, y
        self.function = function
        self.clicable = clicable
        self.cd = 30
        if name_image is not None:
            self.image = pygame.transform.scale(load_image(name_image, colorkey=-1), size)
            self.size = self.w, self.h = size[0], size[1]
        else:
            self.image = None
        self.function_peremen = function_peremen
        # а размер под текст настривает

    def render(self, screen, events):  # это, тип, обычные кнопочки
        if self.cd != 0:
            self.cd -= 1
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
        if self.clicable and not self.cd:
            if self.function_peremen is None:
                self.function()
            else:
                self.function(*self.function_peremen)

    def is_mouse_on(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h


class Scroll:
    def __init__(self, buttons, x, y):
        self.buttons = buttons
        self.x = x
        self.y = y
        self.step = WIDTH // 30
        self.v = WIDTH // 5
        past_x = 0
        self.buttons = []
        for char in buttons:
            if len(char) > 3:
                self.buttons.append(Button(char[0], x, y, char[1], name_image=char[2], size=char[3]))
            elif len(char) == 3:
                self.buttons.append(Button(char[0], x, y, char[1], function_peremen=[char[2]]))
            else:
                self.buttons.append(Button(char[0], x, y, char[1]))
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
                if max_ - self.v > WIDTH - self.v:
                    for i in range(len(self.buttons)):
                        self.buttons[i].x -= self.v
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                min_ = min([elem.x for elem in self.buttons])
                if min_ + self.v < self.v:
                    for i in range(len(self.buttons)):
                        self.buttons[i].x += self.v


class Name_input:
    def __init__(self, poz, size, random_name_button, max_count_symbols):
        print(poz)
        self.mod = 0
        self.x, self.y = poz[0], poz[1]
        self.text_input = Button('', *poz, None, clicable=False)
        self.text_input.size = self.text_input.w, self.text_input.h = size
        self.max_count_symbols = max_count_symbols
        self.min_size = size
        self.continue_button = Button('Continue', self.x, self.y + self.text_input.h, self.success)
        if random_name_button:
            self.random_name_button = Button('random_name', self.text_input.w + self.x + self.text_input.w, self.y + self.text_input.h, self.create_random_name)
            self.random_name_button.x = self.text_input.w + self.x - self.random_name_button.w
            self.continue_button.x = self.random_name_button.x - self.continue_button.w
        else:
            self.random_name_button = None
            self.continue_button.x = self.text_input.w + self.x - self.random_name_button.w

    def create_random_name(self, symbols='фбвгдеёжзийклмнопрстуфхцчшщъыьэюяabsdefghijklmnopqrstuvwxyz1234567890', counts=(5, 10)):
        name = ''
        for _ in range(random.randint(*counts)):
            name += random.choice(symbols)
        self.text_input.text = name
        self.text_input.font_light = font.render(self.text_input.text, True, (100, 255, 255))
        self.text_input.font = font.render(self.text_input.text, True, (100, 100, 100))
        self.text_input.size = self.text_input.w, self.text_input.h = self.text_input.font.get_width() + 10, self.text_input.font.get_height() + 10
        self.resize()

    def resize(self):
        if self.text_input.font.get_width() + 10 < self.min_size[0]:
            self.text_input.size = self.text_input.w, self.text_input.h = self.min_size
        self.random_name_button.x = self.text_input.w + self.x - self.random_name_button.w

    def update(self, events):
        self.text_input.render(screen, events)
        self.continue_button.render(screen, events)
        if self.random_name_button is not None:
            self.random_name_button.render(screen, events)

    def success(self):
        global NAME, enter_nam, MOD
        if self.text_input.text != '':
            NAME = self.text_input.text
            enter_nam = None
            MOD = 'in_game_menu'


def enter_name(poz, size, random_name_button=True, max_count_symbols=10):
    global enter_nam
    enter_nam = Name_input(poz, size, random_name_button, max_count_symbols)