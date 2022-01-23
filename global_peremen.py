import pygame, os
import sys, random


class Global_peremen_error(Exception):
    pass


try:
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    MOD = 'main_menu'
    SIZE = WIDTH, HIGH = 900, 500
    screen = pygame.display.set_mode(SIZE)
    font = pygame.font.Font(None, min(SIZE) // 10)
    big_font = pygame.font.Font(None, min(SIZE) // 5)
    NAME = ''
    enter_nam = None
    choice_menu = None
    in_game_menu = None
    eng_symbols='0123456789qwertyuiop  asdfghjkl  zxcvbnm  '
    ru_symbols = '0123456789йцукенгшщзхъфывапролджэячсмитьбю'
    indexes = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 122, 120, 99, 118, 98, 110, 109, 44, 46]
    run = True
    new_game = True
    levels = {}
    index = None
    music = None
    music_now = 'data\MENU.mp3'
    volume = 0.03


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
                if size[0] < self.font.get_width():
                    size = self.font.get_width(), size[1]
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
                            result = self.click_on()
                            if result:
                                return result
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
                    return self.function()
                else:
                    return self.function(*self.function_peremen)

        def is_mouse_on(self, x, y):
            return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h


    class Scroll:
        def __init__(self, buttons, x, y, mod='horizontal'):
            self.buttons = buttons
            self.x = x
            self.y = y
            self.step = WIDTH // 30
            self.v = WIDTH // 10
            self.buttons = []
            past_x = 0
            past_y = 0
            for char in buttons:
                clicable=True
                if char[-1] == 'clicable':
                    clicable = False
                    char = char[:-1]
                if len(char) == 4:
                    self.buttons.append(Button(char[0], x, y, char[1], name_image=char[2], size=char[3], clicable=clicable))
                elif len(char) == 3:
                    self.buttons.append(Button(char[0], x, y, char[1], function_peremen=[char[2]], clicable=clicable))
                elif len(char) == 5:
                    self.buttons.append(Button(char[0], x, y, char[1], name_image=char[2], size=char[3], function_peremen=[char[4]], clicable=clicable))
                else:
                    self.buttons.append(Button(char[0], x, y, char[1], clicable=clicable))
            for i in range(len(self.buttons)):
                if mod == 'horizontal':
                    self.buttons[i].x = past_x + self.step
                    past_x = self.buttons[i].x + self.buttons[i].w
                elif mod == 'vertical':
                    self.buttons[i].y = past_y + self.step
                    past_y = self.buttons[i].y + self.buttons[i].h
            self.mod = mod

        def update(self, events):
            for i in range(len(self.buttons)):
                if (0 <= self.buttons[i].x <= WIDTH or 0 <= self.buttons[i].x + self.buttons[i].w <= WIDTH) and (0 <= self.buttons[i].y <= HIGH or 0 <= self.buttons[i].y + self.buttons[i].h <= HIGH):
                    self.buttons[i].render(screen, events)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    if self.mod == 'horizontal':
                        max_ = max([elem.x + elem.w for elem in self.buttons])
                        if max_ - self.v > WIDTH - self.v:
                            for i in range(len(self.buttons)):
                                self.buttons[i].x -= self.v
                    elif self.mod == 'vertical':
                        max_ = max([elem.y + elem.h for elem in self.buttons])
                        if max_ - self.v > HIGH - self.v:
                            for i in range(len(self.buttons)):
                                self.buttons[i].y -= self.v
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    if self.mod == 'horizontal':
                        min_ = min([elem.x for elem in self.buttons])
                        if min_ + self.v < self.v:
                            for i in range(len(self.buttons)):
                                self.buttons[i].x += self.v
                    elif self.mod == 'vertical':
                        min_ = min([elem.y for elem in self.buttons])
                        if min_ + self.v < self.v:
                            for i in range(len(self.buttons)):
                                self.buttons[i].y += self.v


    class Name_input:
        def __init__(self, poz, size, random_name_button, max_count_symbols):
            self.mod = 0
            self.actual_symbols = ru_symbols
            self.x, self.y = poz[0], poz[1]
            self.text_input = Button('', *poz, self.set_mod)
            self.text_input.size = self.text_input.w, self.text_input.h = size
            self.max_count_symbols = max_count_symbols
            self.min_size = size
            self.continue_button = Button('Continue', self.x, self.y + self.text_input.h, self.success)
            self.lenguage = Button('RU', self.x + self.text_input.w, self.y, self.set_symbols)
            self.lenguage.x, self.lenguage.y = self.lenguage.x - self.lenguage.w, self.lenguage.y - self.lenguage.h
            if random_name_button:
                self.random_name_button = Button('random_name', self.text_input.w + self.x + self.text_input.w, self.y + self.text_input.h, self.create_random_name)
                self.random_name_button.x = self.text_input.w + self.x - self.random_name_button.w
                self.continue_button.x = self.random_name_button.x - self.continue_button.w
            else:
                self.random_name_button = None
                self.continue_button.x = self.text_input.w + self.x - self.random_name_button.w
            self.close = Button('close', WIDTH, 0, self.close)
            self.close.x = self.close.x - self.close.w

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

        def close(self):
            global MOD
            MOD = 'main_menu'

        def update(self, events):
            self.close.render(screen, events)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in indexes and self.mod and self.actual_symbols[indexes.index(event.key)] != ' ':
                        if len(self.text_input.text + self.actual_symbols[indexes.index(event.key)]) <= self.max_count_symbols:
                            self.text_input.text += self.actual_symbols[indexes.index(event.key)]
                            self.text_input.font_light = font.render(self.text_input.text, True, (100, 255, 255))
                            self.text_input.font = font.render(self.text_input.text, True, (100, 100, 100))
                            self.text_input.size = self.text_input.w, self.text_input.h = self.text_input.font.get_width() + 10, self.text_input.font.get_height() + 10
                            self.resize()
                    if event.key == pygame.K_BACKSPACE and self.mod and self.text_input.text != '':
                        self.text_input.text = self.text_input.text[:-1]
                        self.text_input.font_light = font.render(self.text_input.text, True, (100, 255, 255))
                        self.text_input.font = font.render(self.text_input.text, True, (100, 100, 100))
                        self.text_input.size = self.text_input.w, self.text_input.h = self.text_input.font.get_width() + 10, self.text_input.font.get_height() + 10
                        self.resize()
            self.text_input.render(screen, events)
            self.continue_button.render(screen, events)
            self.lenguage.render(screen, events)
            if self.random_name_button is not None:
                self.random_name_button.render(screen, events)

        def success(self):
            global NAME, enter_nam, MOD
            if self.text_input.text != '':
                NAME = self.text_input.text
                enter_nam = None
                MOD = 'in_game_menu'

        def set_mod(self):
            if self.mod:
                self.mod = 0
            else:
                self.mod = 1

        def set_symbols(self):
            if self.actual_symbols == ru_symbols:
                self.actual_symbols = eng_symbols
                self.lenguage.text = 'EN'
            else:
                self.actual_symbols = ru_symbols
                self.lenguage.text = 'RU'
            self.lenguage.font_light = font.render(self.lenguage.text, True, (100, 255, 255))
            self.lenguage.font = font.render(self.lenguage.text, True, (100, 100, 100))
            self.lenguage.size = self.lenguage.w, self.lenguage.h = self.lenguage.font.get_width() + 10, self.lenguage.font.get_height() + 10

    class Input_set:
        def __init__(self, poz, size, symbols, indexess, max_count_symbols=10):
            self.mod = 0
            self.actual_symbols = symbols
            self.x, self.y = poz[0], poz[1]
            self.text_input = Button('', *poz, self.set_mod)
            self.text_input.size = self.text_input.w, self.text_input.h = size
            self.max_count_symbols = max_count_symbols
            self.min_size = size
            self.indexes = indexess
            self.continue_button = Button('Continue', self.x, self.y + self.text_input.h, self.success)
            self.text_input.size = self.text_input.w, self.text_input.h = size
            self.continue_button.x = self.text_input.x + self.text_input.w - self.continue_button.w

        def resize(self):
            if self.text_input.font.get_width() + 10 < self.min_size[0]:
                self.text_input.size = self.text_input.w, self.text_input.h = self.min_size

        def update(self, events):
            self.text_input.render(screen, events)
            result = self.continue_button.render(screen, events)
            if result:
                return result
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in self.indexes and self.mod:
                        if len(self.text_input.text + self.actual_symbols[self.indexes.index(event.key)]) <= self.max_count_symbols:
                            self.text_input.text += self.actual_symbols[self.indexes.index(event.key)]
                            self.text_input.font_light = font.render(self.text_input.text, True, (100, 255, 255))
                            self.text_input.font = font.render(self.text_input.text, True, (100, 100, 100))
                            self.text_input.size = self.text_input.w, self.text_input.h = self.text_input.font.get_width() + 10, self.text_input.font.get_height() + 10
                            self.resize()
                    if event.key == pygame.K_BACKSPACE and self.mod and self.text_input.text != '':
                        self.text_input.text = self.text_input.text[:-1]
                        self.text_input.font_light = font.render(self.text_input.text, True, (100, 255, 255))
                        self.text_input.font = font.render(self.text_input.text, True, (100, 100, 100))
                        self.text_input.size = self.text_input.w, self.text_input.h = self.text_input.font.get_width() + 10, self.text_input.font.get_height() + 10
                        self.resize()

        def success(self):
            global NAME, enter_nam, MOD
            if self.text_input.text != '':
                return self.text_input.text

        def set_mod(self):
            if self.mod:
                self.mod = 0
            else:
                self.mod = 1




    def enter_name(poz, size, random_name_button=True, max_count_symbols=10):
        global enter_nam
        enter_nam = Name_input(poz, size, random_name_button, max_count_symbols)
except:
    raise Global_peremen_error()