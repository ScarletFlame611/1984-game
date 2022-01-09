import pygame
import os
import sys
import time
import global_peremen

pygame.init()
pygame.display.set_caption('Обучение')
FPS = 60
v = 4  # скорость игрока
start_frame = time.time()
amount_of_frames = 8
frames_per_second = 8  # обновление кадров для анимации бега
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # группа для остановки игрока при столкновении с ее объектами


# загрузка изображения


tile_images = {
    'wall': global_peremen.load_image('box.png'),
    'empty': global_peremen.load_image('floor.png')
}
player_image = global_peremen.load_image('player.png')

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
            self.frames.append(global_peremen.load_image(f"run{i}.png"))
        self.cur_frame = 0
        self.current_state = "right"  # текущее направление, куда смотрит игрок

    # передаются координаты сдвига игрока и направление движения
    # (0-вправо, 1 - влево, -1 - остановка)
    def update(self, coords, direction=0):
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


class level:
    def __init__(self, matrix_name, image_name, colorkey=0):
        self.image = global_peremen.load_image(image_name, colorkey=colorkey)
        self.level = self.load_level(matrix_name)

    def load_level(self, filename):
        with open("data/" + filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self):
        new_player, x, y = None, None, None
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        self.player = new_player
        self.x, self.y = x, y

    def play(self):
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
            player.update([0, -v])
        elif keys[pygame.K_DOWN]:
            player.update([0, v])
        else:
            player.update([0, 0], -1)
        screen.fill("black")
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)