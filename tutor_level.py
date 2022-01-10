import pygame
import os
import sys
import time
import random

size = width, height = 770, 420
pygame.init()
pygame.display.set_caption('Обучение')
screen = pygame.display.set_mode((width, height))
FPS = 60
v = 4  # скорость игрока
start_frame = time.time()
amount_of_frames = 8
frames_per_second = 8  # обновление кадров для анимации бега
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # группа для остановки игрока при столкновении с ее объектами
bonus_group = pygame.sprite.Group()
coins = pygame.sprite.Group()


# генерация уровня
def generate_level(level, number_of_level=0):
    new_player, x, y = None, None, None
    tiles_types = ['empty', 'wall']
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(tiles_types[0], x, y)
            elif level[y][x] == '#':
                Tile(tiles_types[1], x, y)
            elif level[y][x] == '+':
                HealTile(x, y)
            elif level[y][x] == '$':
                Tile(tiles_types[0], x, y)
                Coin(x, y)
            elif level[y][x] == '@':
                Tile(tiles_types[0], x, y)
                new_player = Player(x, y)
    return new_player, x, y


# загрузка уровня
def load_level(filename):
    filename = "data/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('floor.png'),
    'metal1': load_image('metal1.png')
}
player_image = load_image('player.png')

tile_width = tile_height = 70


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 5)
        self.runframes = []
        self.goframes = []
        for i in range(1, 9):
            self.runframes.append(load_image(f"run{i}.png"))
        for i in range(1, 7):
            self.goframes.append(load_image(f"go{i}.png"))
        self.cur_frame = 0
        self.current_state = "right"  # текущее направление, куда смотрит игрок
        self.hp = 150
        self.score = 0

    # передаются координаты сдвига игрока и направление движения
    # (0-вправо, 1 - влево, -1 - остановка)
    def update(self, coords, direction=0):
        global amount_of_frames
        if direction != -1:
            self.rect.move_ip(coords)
            if direction in (0, 1):
                amount_of_frames = 8
                self.cur_frame = int(
                    (time.time() - start_frame) * frames_per_second % amount_of_frames)
                self.current_state = "right" if direction != 1 else "left"
                # если изменилось направление движения - меняем текущее направление,
                # куда смотрит игрок
                self.image = self.runframes[
                    self.cur_frame] if direction == 0 else pygame.transform.flip(
                    self.runframes[self.cur_frame], True, False)
            else:
                amount_of_frames = 6
                self.cur_frame = int(
                    (time.time() - start_frame) * frames_per_second % amount_of_frames)
                self.image = self.goframes[
                    self.cur_frame]
            if pygame.sprite.spritecollideany(self, wall_group):
                # если произошло столкновение со стеной - перемещаем обратно
                self.rect.move_ip([-i for i in coords])
            hits = pygame.sprite.spritecollide(self, bonus_group, False)
            if hits:
                for sprite in hits:
                    if pygame.sprite.collide_rect(sprite, sprite):
                        sprite.buff(self)

        else:
            self.image = player_image if self.current_state == "right" else pygame.transform.flip(
                player_image, True, False)


# класс плиток
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == "wall":
            self.add(wall_group)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# границы карты
class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(wall_group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(wall_group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class HealTile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = load_image('heal.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.add(bonus_group)
        self.used = False

    def buff(self, other):
        if not self.used:
            other.hp += 300
            self.used = True


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bonus_group, all_sprites)
        self.frames = []
        self.add(coins)
        for i in range(1, 7):
            self.frames.append(load_image(f"coin{i}.png"))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 20, tile_height * pos_y + 15)

    def update(self):
        amount_of_frames = 6
        self.cur_frame = int(
            (time.time() - start_frame) * frames_per_second % amount_of_frames)
        self.image = self.frames[self.cur_frame]
        self.used = False

    def buff(self, other):
        if not self.used:
            other.score += 300
            self.used = True
            self.remove(coins)
            self.remove(bonus_group)


def draw_bar(surf, x, y, player_hp):
    if player_hp < 0:
        player_hp = 0
    bar_width = 300
    bar_height = 10
    fill = (player_hp / 1500) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, pygame.Color("green"), fill_rect)
    pygame.draw.rect(surf, pygame.Color("white"), outline_rect, 2)


def terminate():
    pygame.quit()
    sys.exit()


def game():
    player, level_x, level_y = generate_level(load_level('level0.txt'))
    Border(0, 0, width, 0)
    Border(0, height, width, height)
    Border(0, 0, 0, height)
    Border(width, 0, width, height)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        # движение игрока (передаются координаты сдвига и направление движения)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.update([-v, 0], 1)
        elif keys[pygame.K_RIGHT]:
            player.update([v, 0])
        elif keys[pygame.K_UP]:
            player.update([0, -v], 3)
        elif keys[pygame.K_DOWN]:
            player.update([0, v], 2)
        else:
            player.update([0, 0], -1)
        screen.fill("black")
        tiles_group.draw(screen)
        bonus_group.draw(screen)
        coins.update()
        draw_bar(screen, 230, 5, player.hp)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    clock = pygame.time.Clock()
    game()
