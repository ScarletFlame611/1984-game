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
bonus_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
coins = pygame.sprite.Group()
for_open = pygame.sprite.Group()
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
        self.runframes = []
        self.goframes = []
        for i in range(1, 9):
            self.runframes.append(global_peremen.load_image(f"run{i}.png"))
        for i in range(1, 7):
            self.goframes.append(global_peremen.load_image(f"go{i}.png"))
        self.cur_frame = 0
        self.current_state = "right"  # текущее направление, куда смотрит игрок
        self.hp = 150
        self.score = 0
        self.keys = 0
        self.instruments = 0

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
            hits = pygame.sprite.spritecollide(self, bonus_group, False)
            if hits:
                for sprite in hits:
                    if pygame.sprite.collide_rect(sprite, sprite):
                        sprite.buff(self)
            hits = pygame.sprite.spritecollide(self, for_open, False)
            if hits:
                for sprite in hits:
                    if pygame.sprite.collide_rect(sprite, sprite):
                        sprite.open(self)
            if pygame.sprite.spritecollideany(self, wall_group):
                # если произошло столкновение со стеной - перемещаем обратно
                self.rect.move_ip([-i for i in coords])
            enemy = pygame.sprite.spritecollide(self, enemies_group, False)
            if enemy:
                for sprite in enemy:
                    if pygame.sprite.collide_rect(sprite, sprite):
                        self.my_enemy = sprite
                global_peremen.MOD = "fight_start"

        else:
            self.image = player_image if self.current_state == "right" else pygame.transform.flip(
                player_image, True, False)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = global_peremen.load_image(f"enemy/idle1.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 5)
        self.cur_frame = 0
        self.current_state = "right"  # текущее направление, куда смотрит игрок
        self.hp = 150

    # передаются координаты сдвига врага и направление движения
    # (0-вправо, 1 - влево, -1 - остановка)
    def update(self, x_player):
        self.current_state = "right" if x_player > self.rect.x else "left"
        if self.current_state == "right":
            self.image = global_peremen.load_image(f"enemy/idle1.png")
        else:
            self.image = pygame.transform.flip(global_peremen.load_image(f"enemy/idle1.png"), True,
                                               False)


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
            self.add(borders_group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(wall_group)
            self.add(borders_group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class HealTile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.add(bonus_group)
        self.image = global_peremen.load_image('heal.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.used = False

    def buff(self, other):
        if not self.used and other.hp < 150:
            other.hp += 30
            self.used = True
            color = pygame.Color(100, 100, 100)
            colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
            colorImage.fill(color)
            self.image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bonus_group, all_sprites)
        self.frames = []
        self.add(coins)
        for i in range(1, 7):
            self.frames.append(global_peremen.load_image(f"coin{i}.png"))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 20, tile_height * pos_y + 15)
        self.used = False

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


class level:
    def __init__(self, matrix_name, colorkey=0):
        self.level = self.load_level(matrix_name)
        self.mouse_x, self.mouse_y = None, None

    def load_level(self, filename):
        with open("data/" + filename + ".txt", 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self, number_of_level=0):
        player, x, y = None, None, None
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == '.':
                    Tile('empty', x, y)
                elif self.level[y][x] == '#':
                    Tile('wall', x, y)
                elif self.level[y][x] == '@':
                    Tile('empty', x, y)
                    player = Player(x, y)
                elif self.level[y][x] == '+':
                    Tile('empty', x, y)
                    HealTile(x, y)
                elif self.level[y][x] == '$':
                    Tile('empty', x, y)
                    Coin(x, y)
                elif self.level[y][x] == "&":
                    Tile('empty', x, y)
                    Enemy(x, y)
                elif self.level[y][x] == ">":
                    Speed_Up(x, y)
                elif self.level[y][x] == "<":
                    Speed_Down(x, y)
                elif self.level[y][x] == "<":
                    Speed_Down(x, y)
                elif self.level[y][x] == "k":
                    Tile('empty', x, y)
                    Key(x, y)
                elif self.level[y][x] == "i":
                    Tile('empty', x, y)
                    Instrument(x, y)
                elif self.level[y][x] == "?":
                    Safe(x, y)
                elif self.level[y][x] == "!":
                    Panel(x, y)
                elif self.level[y][x] == "=":
                    Tile('empty', x, y)
                    Trap(x, y)
        self.player = player
        self.width = len(self.level[0]) * tile_width
        self.height = len(self.level) * tile_height
        self.x, self.y = x, y

    def play(self):
        ui = UI()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.terminate()
        # движение игрока (передаются координаты сдвига и направление движения)
        if global_peremen.MOD == "play":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.update([-v, 0], 1)
            elif keys[pygame.K_RIGHT]:
                self.player.update([v, 0])
            elif keys[pygame.K_UP]:
                self.player.update([0, -v])
            elif keys[pygame.K_DOWN]:
                self.player.update([0, v], 2)
            else:
                self.player.update([0, 0], -1)
        else:
            self.player.update([0, 0], -1)

        for enemy in enemies_group:
            enemy.update(self.player.rect.x)

        global_peremen.screen.fill("black")
        tiles_group.draw(global_peremen.screen)
        if global_peremen.MOD == "play":
            for item in bonus_group:
                item.update()
            coins.draw(global_peremen.screen)
            bonus_group.draw(global_peremen.screen)
        if global_peremen.MOD == "fight_start":
            fight = Fight(self.player)
            fight.update()
        enemies_group.draw(global_peremen.screen)
        player_group.draw(global_peremen.screen)
        borders_group.draw(global_peremen.screen)
        ui.draw_bar(global_peremen.screen, 10, 10, self.player.hp)
        ui.show_scores(global_peremen.screen, global_peremen.WIDTH - 150, 10, self.player.score)
        pygame.display.flip()
        global_peremen.clock.tick(FPS)


class Fight:
    def __init__(self, player):
        self.player = player
        self.lab = []
        x = global_peremen.WIDTH // tile_width
        y = global_peremen.HIGH // tile_height
        for y1 in range(y):
            row = []
            for x1 in range(x):
                for elem in wall_group:
                    if elem.rect.x // tile_width == x1 and elem.rect.y // tile_height == y1:
                        row.append(-1)
                        break
                else:
                    row.append(0)
            self.lab.append(row)
        self.w, self.h = x, y
        play_x = self.player.rect.x // tile_width
        play_y = self.player.rect.y // tile_height
        self.player_cords = (play_x, play_y)
        self.player.rect.x = play_x * tile_width + 10
        self.player.rect.y = play_y * tile_height + 5
        self.mod = "player"
        self.player_count = 5
        self.enemy_count = 5

    def draw_blocks(self):
        color = pygame.Color(70, 70, 70)
        x = global_peremen.WIDTH // tile_width
        y = global_peremen.HIGH // tile_height
        for x1 in range(x):
            for y1 in range(y):
                color_light = pygame.Color(230, 230, 230)
                self.draw_block(color, x1, y1)
                if self.is_path(x1, y1):
                    pos = pygame.mouse.get_pos()
                    if pos[0] // tile_width == x1 and pos[1] // tile_height == y1:
                        color_light = pygame.Color(100, 250, 250)
                    self.draw_block(color_light, x1, y1, size=2)

    # отрисовка блока x, y
    def draw_block(self, color, x, y, size=1):
        for elem in wall_group:
            if elem.rect.x // tile_width == x and elem.rect.y // tile_height == y:
                break
        else:
            pygame.draw.rect(global_peremen.screen, color, (tile_width * x, tile_height * y,
                                                            tile_width, tile_height), size)

    def highlighting(self, x, y):
        color = pygame.Color(200, 255, 255)
        self.draw_block(color, x, y, size=2)

    def player_turn(self):
        self.draw_blocks()

    def enemy_turn(self):
        pass

    def update(self):
        if self.mod == "player":
            self.player_turn()

    def is_path(self, x, y):
        if x + 1 <= self.w and y + 1 <= self.h:
            path = \
                self.has_path(self.player_cords[0], self.player_cords[1], 0, self.w, self.h,
                              self.lab)[
                    y][x]
            if path <= self.player_count:
                return True
        return False

    def has_path(self, x, y, cur, w, h, lab):
        lab[y][x] = cur
        if y + 1 < h:
            if lab[y + 1][x] == 0 or (lab[y + 1][x] != -1 and lab[y + 1][x] > cur):
                self.has_path(x, y + 1, cur + 1, w, h, lab)
        if x + 1 < w:
            if lab[y][x + 1] == 0 or (lab[y][x + 1] != -1 and lab[y][x + 1] > cur):
                self.has_path(x + 1, y, cur + 1, w, h, lab)
        if x - 1 >= 0:
            if lab[y][x - 1] == 0 or (lab[y][x - 1] != -1 and lab[y][x - 1] > cur):
                self.has_path(x - 1, y, cur + 1, w, h, lab)
        if y - 1 >= 0:
            if lab[y - 1][x] == 0 or (lab[y - 1][x] != -1 and lab[y - 1][x] > cur):
                self.has_path(x, y - 1, cur + 1, w, h, lab)
        return lab


class Trap(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bonus_group, all_sprites)
        self.image = global_peremen.load_image('trap.png')
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 1, tile_height * pos_y + 50)
        self.used = False

    def buff(self, other):
        if not self.used:
            other.hp -= 10
            self.image = global_peremen.load_image('trap2.png')
            self.rect = self.image.get_rect().move(
                tile_width * self.x + 10, tile_height * self.y + 30)
            self.used = True


class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bonus_group, all_sprites)
        self.image = global_peremen.load_image('key.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 20, tile_height * pos_y + 15)
        self.used = False

    def buff(self, other):
        if not self.used:
            other.keys += 1
            self.used = True
            self.remove(bonus_group)
            self.remove(all_sprites)


class Instrument(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bonus_group, all_sprites)
        self.image = global_peremen.load_image('key2.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 20, tile_height * pos_y + 15)
        self.used = False

    def buff(self, other):
        if not self.used:
            other.instruments += 1
            self.used = True
            self.remove(bonus_group)
            self.remove(all_sprites)


class Panel(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.add(for_open)
        self.image = global_peremen.load_image('broken_panel.jpg')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.used = False

    def open(self, other):
        if other.instruments > 0 and not self.used:
            self.used = True
            other.score += 100
            other.instruments -= 1
            self.image = global_peremen.load_image('panel.jpg')


class Safe(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.add(for_open)
        self.add(wall_group)
        self.image = global_peremen.load_image('Safe.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.used = False

    def open(self, other):
        if other.keys > 0 and not self.used:
            self.used = True
            other.score += 100
            other.keys -= 1
            self.image = global_peremen.load_image('Safe1.png')


class Speed_Up(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.add(bonus_group)
        self.image = global_peremen.load_image('fast.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.used = False

    def buff(self, other):
        global v
        if not self.used:
            v += 1
            self.used = True


class Speed_Down(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.add(bonus_group)
        self.image = global_peremen.load_image('slow.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.used = False

    def buff(self, other):
        global v
        if not self.used:
            v -= 1
            self.used = True


class UI:
    def draw_skills(self):
        pass

    def draw_bar(self, surf, x, y, player_hp):
        if player_hp < 0:
            player_hp = 0
        if player_hp > 150:
            player_hp = 150
        bar_width = 300
        bar_height = 10
        fill = (player_hp / 150) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surf, pygame.Color("green"), fill_rect)
        pygame.draw.rect(surf, pygame.Color("white"), outline_rect, 2)

    def show_scores(self, surf, x, y, score):
        pygame.font.init()
        f = pygame.font.Font(None, 36)
        text = f.render(f'Score: {score}', True,
                        (255, 255, 255))
        surf.blit(text, (x, y))
        pygame.display.update()
