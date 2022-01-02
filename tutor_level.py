import pygame
import os
import sys
import time
from fight import *

size = width, height = 770, 420
pygame.init()

cd_step = 0  # кд шага(чтобы не спамило)
CD_STEP = 30  # для того чтобы не менять кд в коде сделаем константу
FPS = 60
v = 4  # скорость игрока
start_frame = time.time()
amount_of_frames = 8
frames_per_second = 8  # обновление кадров для анимации бега
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # группа для остановки игрока при столкновении с ее объектами
enemies_group = pygame.sprite.Group()  # группа для всех врагов на уровне
step = pygame.mixer.Sound('data\step.mp3')  # звук шага
pygame.mixer.music.load("data/level_music.mp3")  # музыка
FIGHT = False


# генерация уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == "&":
                Enemy(x, y)
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
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('floor.png')
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
        self.frames = []
        for i in range(1, 9):
            self.frames.append(load_image(f"run{i}.png"))
        self.cur_frame = 0
        self.current_state = "right"  # текущее направление, куда смотрит игрок
        self.hp = 100

    # передаются координаты сдвига игрока и направление движения
    # (0-вправо, 1 - влево, -1 - остановка)
    def update(self, coords, direction=0):
        global FIGHT
        if direction != -1:
            self.rect.move_ip(coords)
            self.cur_frame = int((time.time() - start_frame) * frames_per_second % amount_of_frames)
            self.current_state = "right" if direction != 1 else "left"
            # если изменилось направление движения - меняем текущее направление, куда смотрит игрок
            self.image = self.frames[self.cur_frame] if direction == 0 else pygame.transform.flip(
                self.frames[self.cur_frame], True, False)
            if pygame.sprite.spritecollideany(self, wall_group):
                # если произошло столкновение со стеной - перемещаем обратно
                self.rect.move_ip([-i for i in coords])
            if pygame.sprite.spritecollideany(self, enemies_group):
                FIGHT = True
                pygame.mixer.music.load("data/fight.mp3")
                pygame.mixer.music.play(-1)
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


# класс  врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.add(enemies_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 5)
        self.frames = []
        for i in range(1, 9):
            self.frames.append(load_image(f"run{i}.png"))
        self.image = self.frames[0]
        self.hp = 100

    def update(self):
        pass


def fight():
    def update():
        print(0)


def terminate():
    pygame.quit()
    sys.exit()


def show_groupes(screen):
    tiles_group.draw(screen)
    player_group.draw(screen)
    enemies_group.draw(screen)


def game():
    global FIGHT, cd_step
    pygame.display.set_caption('Обучение')
    screen = pygame.display.set_mode((width, height))
    player, level_x, level_y = generate_level(load_level('level0.txt'))
    Border(0, 0, width, 0)
    Border(0, height, width, height)
    Border(0, 0, 0, height)
    Border(width, 0, width, height)
    enemy1 = Enemy(100, 50)
    x_pos, y_pos = 0, 0
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    while True:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                x_pos, y_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN and FIGHT:
                if event.button == 1:
                    if board.turn == "Player":
                        board.walk(event.pos[0] // tile_width, event.pos[1] // tile_height)
        # НЕ режим боя
        if not FIGHT:
            # движение игрока (передаются координаты сдвига и направление движения)
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]) and not cd_step:
                cd_step = CD_STEP
                step.play()
            elif cd_step:
                cd_step -= 1
            if keys[pygame.K_LEFT]:
                player.update([-v, 0], 1)
            elif keys[pygame.K_RIGHT]:
                player.update([v, 0])
            elif keys[pygame.K_UP]:
                player.update([0, -v])
            elif keys[pygame.K_DOWN]:
                player.update([0, v])
            else:
                player.update([0, 0], -1)
            show_groupes(screen)
        # режим боя
        else:
            player.image = player_image
            show_groupes(screen)
            fighting(width, height, tile_height, player, enemy1, wall_group, (x_pos, y_pos), screen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_k]:
                if board.attack_for_K():  # одна из атак на букву K
                    pass
                else:
                    # попытки выйти из боя и удалить врага
                    FIGHT = False
                    pygame.mixer.music.load("data/level_music.mp3")
                    pygame.mixer.music.play(-1)
                    enemy1.kill()

        enemy1.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    game()
