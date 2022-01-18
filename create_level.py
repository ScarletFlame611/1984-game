import pygame
import sys
import time
import global_peremen
import particles

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
enemies = []  # группа для всех врагов
bar_x, bar_y = 10, 10
EVENTS = None
coins = pygame.sprite.Group()
level_name = None
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
        self.image = None
        self.runframes = []
        self.goframes = []
        self.fire = []
        self.start = []
        for i in range(1, 9):
            self.runframes.append(global_peremen.load_image(f"run{i}.png"))
        for i in range(1, 7):
            self.goframes.append(global_peremen.load_image(f"go{i}.png"))
        for i in range(1, 6):
            self.fire.append(global_peremen.load_image(f"fire{i}.png"))
        for i in range(1, 8):
            self.start.append(global_peremen.load_image(f"start{i}.png"))
        self.cur_frame = 0
        self.current_state = "right"  # текущее направление, куда смотрит игрок
        self.hp = 400
        self.score = 0
        self.keys = 0
        self.instruments = 0
        self.is_start = False

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
            if pygame.sprite.spritecollideany(self, wall_group):
                # если произошло столкновение со стеной - перемещаем обратно
                self.rect.move_ip([-i for i in coords])
        else:
            self.image = player_image if self.current_state == "right" else pygame.transform.flip(
                player_image, True, False)

    def attack(self, enemy, damage):
        enemy.hp -= damage

    def attack_update(self):
        amount_of_frames = 5
        self.cur_frame = int(
            (time.time() - start_frame) * frames_per_second % amount_of_frames)
        self.image = self.fire[self.cur_frame]

    def start_update(self):
        amount_of_frames = 7
        self.cur_frame = int(
            (time.time() - start_frame) * frames_per_second % amount_of_frames)
        self.image = self.start[self.cur_frame]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, distation=5, damage=10):
        super().__init__(enemies_group, all_sprites)
        self.image = global_peremen.load_image(f"enemy/idle1.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + 5)
        self.fire = []
        for i in range(1, 7):
            self.fire.append(global_peremen.load_image(f"enemy/fire{i}.png"))
        self.cur_frame = 0
        self.current_state = "right"  # текущее направление, куда смотрит игрок
        self.hp = 150
        self.in_fight = False
        self.max_hp = 150
        self.range = distation
        self.cords = (pos_x, pos_y)
        self.damage = damage

    # передаются координаты сдвига врага и направление движения
    # (0-вправо, 1 - влево, -1 - остановка)
    def update(self, x_player):
        is_hero = pygame.sprite.spritecollide(self, player_group, False)
        if is_hero:
            self.in_fight = True
            global_peremen.MOD = "fight_start"
        self.current_state = "right" if x_player > self.rect.x else "left"
        if self.current_state == "right":
            self.image = global_peremen.load_image(f"enemy/idle1.png")
        else:
            self.image = pygame.transform.flip(global_peremen.load_image(f"enemy/idle1.png"), True, False)

    def attack(self, player):
        player.hp -= self.damage

    def attack_update(self):
        amount_of_frames = 6
        self.cur_frame = int(
            (time.time() - start_frame) * frames_per_second % amount_of_frames)
        if self.current_state == "right":
            self.image = self.fire[self.cur_frame]
        else:
            self.image = pygame.transform.flip(self.fire[self.cur_frame], True, False)
        if self.hp <= 0:
            global_peremen.MOD = 'play'
            enemies_group.remove(self)
            all_sprites.remove(self)
            enemies.remove(self)
            self.kill()

    def motion(self, x, y):
        self.rect.x = x * tile_width + 10
        self.rect.y = y * tile_height + 5
        play_x = self.rect.x // tile_width
        play_y = self.rect.y // tile_height
        self.cords = (play_x, play_y)


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


class Level:
    def __init__(self, matrix_name, colorkey=0):
        self.level = self.load_level(matrix_name)
        self.mouse_x, self.mouse_y = None, None
        self.win_button = global_peremen.Button('WIN', global_peremen.WIDTH // 2, global_peremen.HIGH // 2, self.win())
        self.player_start_cd = 20

    def load_level(self, filename):
        global level_name
        level_name = filename
        self.name = filename
        with open("data/levels/" + filename + ".txt", 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def win(self):
        global_peremen.levels[self.name] = max([player.score for player in player_group])
        global_peremen.MOD = 'in_game_menu'

    def generate_level(self, number_of_level=0):
        player, x, y = None, None, None
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == '.':
                    Tile('empty', x, y)
                elif self.level[y][x] == '#':
                    Tile('wall', x, y)
                elif self.level[y][x] == '+':
                    Tile('empty', x, y)
                    HealTile(x, y)
                elif self.level[y][x] == '$':
                    Tile('empty', x, y)
                    Coin(x, y)
                elif self.level[y][x] == "&":
                    Tile('empty', x, y)
                    enemies.append(Enemy(x, y))
                elif self.level[y][x] == '@':
                    Tile('empty', x, y)
                    player = Player(x, y)
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
        self.x, self.y = x, y

    def play(self, events):
        global EVENTS
        if not [enemy for enemy in enemies]:
            self.win_button.render(events=global_peremen.screen, events)
        EVENTS = events
        if global_peremen.MOD == "fight_start":
            for enemy in enemies:
                if enemy.in_fight:
                    self.fight = Fight(self.player, enemy, self.level)
        self.player.iamge = None
        for event in events:
            if event.type == pygame.QUIT:
                sys.terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and global_peremen.MOD == "fight":
                if event.button == 1:
                    self.fight.motion(event.pos[0] // tile_width, event.pos[1] // tile_height)
            if event.type == pygame.KEYDOWN and global_peremen.MOD == "fight":
                if event.key == pygame.K_k:
                    self.fight.attack(5, 5, 1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ui.menu_esc()
        # движение игрока (передаются координаты сдвига и направление движения)
        if self.player_start_cd != 0:
            self.player.start_update()
            self.player_start_cd -= 1
        else:
            if global_peremen.MOD == "play":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.update([-v, 0], 1)
                    self.steps_particles(-10)
                elif keys[pygame.K_RIGHT]:
                    self.player.update([v, 0])
                    self.steps_particles(10)
                elif keys[pygame.K_UP]:
                    self.player.update([0, -v])
                    self.steps_particles(0)
                elif keys[pygame.K_DOWN]:
                    self.player.update([0, v], 2)
                    self.steps_particles(0)
                else:
                    self.player.update([0, 0], -1)
            else:
                self.player.update([0, 0], -1)
        for enemy in enemies_group:
            enemy.update(self.player.rect.x)

        global_peremen.screen.fill("black")

        tiles_group.draw(global_peremen.screen)
        particles.particles.draw(global_peremen.screen)
        particles.particles.update()
        if global_peremen.MOD == "play":
            for item in bonus_group:
                item.update()
            coins.draw(global_peremen.screen)
            bonus_group.draw(global_peremen.screen)
        if global_peremen.MOD == "fight":
            self.fight.update()
        enemies_group.draw(global_peremen.screen)
        player_group.draw(global_peremen.screen)
        borders_group.draw(global_peremen.screen)
        ui.draw_bar(global_peremen.screen, bar_x, bar_y, self.player.hp)
        ui.draw_score(self.player.score)

        pygame.display.flip()
        global_peremen.clock.tick(FPS)

    def steps_particles(self, direction):
        particles.create_particles(
            (self.player.rect.x + self.player.rect.width // 2 + direction,
             self.player.rect.y + self.player.rect.height - 5), ['particle.png'],
            [1, 3, 5],
            (self.player.rect.x, self.player.rect.y + self.player.rect.height,
             self.player.rect.width, self.player.rect.height // 10))


class Fight:
    def __init__(self, player, enemy, level):
        self.level = level
        self.player = player
        self.enemy = enemy
        x = global_peremen.WIDTH // tile_width
        y = global_peremen.HIGH // tile_height
        self.create_lab()
        self.w, self.h = len(self.level[0]), len(self.level)
        play_x = self.player.rect.x // tile_width
        play_y = self.player.rect.y // tile_height
        self.player_cords = (play_x, play_y)
        self.player.rect.x = play_x * tile_width + 10
        self.player.rect.y = play_y * tile_height + 5
        self.mod = "player"
        self.player_count = 5
        self.enemy_count = 5
        global_peremen.MOD = "fight"
        self.enemy_attack_cd = 0
        self.player_animation_cd = 0

    def draw_blocks(self):
        color = pygame.Color(70, 70, 70)
        x = global_peremen.WIDTH // tile_width
        y = global_peremen.HIGH // tile_height
        self.create_lab()
        path = self.has_path(self.player_cords[0], self.player_cords[1], 0, self.w, self.h, self.lab)
        for x1 in range(x):
            for y1 in range(y):
                color_light = pygame.Color(230, 230, 230)
                self.draw_block(color, x1, y1)
                if self.is_path(x1, y1, path):
                    pos = pygame.mouse.get_pos()
                    if pos[0] // tile_width == x1 and pos[1] // tile_height == y1:
                        color_light = pygame.Color(100, 250, 250)
                    self.draw_block(color_light, x1, y1, size=2)

    def create_lab(self):
        self.lab = []
        for y1 in self.level:
            row = []
            for x1 in y1:
                if x1 == "#":
                    row.append(-1)
                else:
                    row.append(0)
            self.lab.append(row)

    def motion(self, x, y):
        if self.mod == "player":
            path = self.has_path(self.player_cords[0], self.player_cords[1], 0, self.w, self.h, self.lab)
            if not (x == self.player.rect.x // tile_width and y == self.player.rect.y // tile_height):
                self.create_lab()
                if self.is_path(x, y, path) and not (self.enemy.rect.x // tile_width == x and
                                                     self.enemy.rect.y // tile_height == y):
                    self.player.rect.x = x * tile_width + 10
                    self.player.rect.y = y * tile_height + 5
                    self.player_count -= \
                        self.has_path(self.player_cords[0], self.player_cords[1], 0, self.w, self.h, self.lab)[y][x]
                    play_x = self.player.rect.x // tile_width
                    play_y = self.player.rect.y // tile_height
                    self.player_cords = (play_x, play_y)

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
        self.create_lab()
        path = self.has_path(self.enemy.cords[0], self.enemy.cords[1], 0, self.w,
                             self.h, self.lab)[self.player_cords[1]][self.player_cords[0]]
        if path <= self.enemy.range:
            if self.enemy_attack_cd == 0:
                self.enemy.attack(self.player)
                self.enemy_attack_cd = 10
                self.enemy_count -= 1
        else:
            new_lab = []
            self.create_lab()
            path = self.has_path(self.player_cords[0], self.player_cords[1], 0, self.w,
                                 self.h, self.lab)
            for y in range(self.h):
                row = []
                for x in range(self.w):
                    path_to_hero = path[y][x]
                    row.append(path_to_hero)
                new_lab.append(row)
            min = 1000
            right = None
            self.create_lab()
            path = self.has_path(self.enemy.cords[0], self.enemy.cords[1], 0, self.w,
                                 self.h, self.lab)
            for y, elem in enumerate(new_lab):
                for x, element in enumerate(elem):
                    path_to_enemy = path[y][x]
                    if path_to_enemy <= self.enemy_count and path_to_enemy > 0:
                        if new_lab[y][x] < min and new_lab[y][x] > 0:
                            min = new_lab[y][x]
                            right = (x, y)
                            min_path = path_to_enemy
            self.enemy.motion(right[0], right[1])
            self.enemy_count -= min_path
            self.create_lab()
        if self.enemy_count <= 0:
            self.player_count = 5
            self.mod = 'player'
            self.enemy_attack_cd = 0

    def update(self):
        if self.player_count <= 0:
            self.enemy_count = 5
            self.player_count = 5
            self.mod = 'enemy'
        if self.mod == "player":
            self.enemy_attack_cd = 0
            self.player_turn()
        else:
            self.player_animation_cd = 0
            self.enemy_turn()
        if self.player_animation_cd != 0:
            self.player.attack_update()
            self.player_animation_cd -= 1
        if self.enemy_attack_cd != 0:
            self.enemy.attack_update()
            self.enemy_attack_cd -= 1
        if self.player.hp <= 0:
            ui.game_over()
        ui.draw_bar_enemy(global_peremen.screen, self.enemy.hp, self.enemy.max_hp)
        turns = self.enemy_count if self.mod == "enemy" else self.player_count
        ui.draw_turns(self.mod, turns)

    def is_path(self, x, y, path):
        if x + 1 <= self.w and y + 1 <= self.h:
            path = path[y][x]
            if path <= self.player_count and path > 0:
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

    def attack(self, damage, radius, mana):
        if self.mod == "player":
            x, y = self.enemy.cords[0], self.enemy.cords[1]
            path = self.has_path(self.player_cords[0], self.player_cords[1], 0, self.w, self.h, self.lab)[y][x]
            if path <= radius:
                self.player.attack(self.enemy, damage)
                self.player_animation_cd = 5
                self.player_count -= mana


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
            v += 2
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
            v -= 2
            self.used = True


class UI:
    def __init__(self):
        self.pause = False

    def draw_skills(self):
        pass

    def draw_score(self, number_score):
        text = "score " + str(number_score)
        font = pygame.font.Font(None, 25)
        font = font.render(text, True, (100, 220, 220))
        global_peremen.screen.blit(font,
                                   (0 + bar_x, 0 + self.bar_height + bar_x + global_peremen.WIDTH // 100))

    def draw_bar(self, surf, x, y, player_hp):
        if player_hp < 0:
            player_hp = 0
        if player_hp > 150:
            player_hp = 150
        bar_width = 300
        self.bar_height = 10
        fill = (player_hp / 150) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, self.bar_height)
        fill_rect = pygame.Rect(x, y, fill, self.bar_height)
        pygame.draw.rect(surf, pygame.Color(100, 230, 230), fill_rect)
        pygame.draw.rect(surf, pygame.Color("white"), outline_rect, 2)

    def draw_bar_enemy(self, surf, enemy_hp, max_hp):
        if enemy_hp < 0:
            enemy_hp = 0
        if enemy_hp > max_hp:
            enemy_hp = max_hp
        bar_width = 300
        fill = (enemy_hp / 150) * bar_width
        x = global_peremen.WIDTH - bar_width - global_peremen.WIDTH // 100
        y = 0 + self.bar_height + global_peremen.HIGH // 100

        outline_rect = pygame.Rect(x, y, bar_width, self.bar_height)
        fill_rect = pygame.Rect(x, y, fill, self.bar_height)
        pygame.draw.rect(surf, pygame.Color(255, 100, 100), fill_rect)
        pygame.draw.rect(surf, pygame.Color("white"), outline_rect, 2)

    def draw_turns(self, turn, turns):
        text = str(turns)
        font = pygame.font.Font(None, 100)
        if turn == "player":
            font = font.render(text, True, (100, 230, 230))
        else:
            font = font.render(text, True, (255, 100, 100))
        global_peremen.screen.blit(font, (global_peremen.WIDTH // 2 - font.get_width() // 2,
                                          0 + global_peremen.WIDTH // 100))

    def delete_level(self):
        global all_sprites, tiles_group, player_group, wall_group, bonus_group, enemies_group
        for elem in bonus_group:
            elem.kill()
        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        wall_group = pygame.sprite.Group()  # группа для остановки игрока при столкновении с ее объектами
        bonus_group = pygame.sprite.Group()
        enemies_group = pygame.sprite.Group()

    def game_over(self):
        fon = pygame.transform.scale(global_peremen.load_image('bg.png'), (global_peremen.WIDTH, global_peremen.HIGH))
        global_peremen.screen.blit(fon, (0, 0))
        again = global_peremen.Button("Start over", global_peremen.WIDTH // 2,
                                      global_peremen.HIGH // 2 - global_peremen.HIGH // 10, self.again)

        back = global_peremen.Button("Back", global_peremen.WIDTH // 2,
                                     global_peremen.HIGH // 2 + global_peremen.HIGH // 10, self.back)
        btns = [again, back]
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if global_peremen.MOD == "in_game_menu" or "level" in global_peremen.MOD:
                    return
            for elem in btns:
                elem.render(global_peremen.screen, events=events)
            pygame.display.flip()
            global_peremen.clock.tick(FPS)

    def again(self):
        self.delete_level()
        global_peremen.MOD = level_name

    def back(self):
        global_peremen.in_game_menu.mod = 'menu'
        global_peremen.MOD = "in_game_menu"
        self.delete_level()

    def resume(self):
        self.pause = False

    def menu_esc(self):
        self.pause = True
        fon = pygame.transform.scale(global_peremen.load_image('bg.png'), (global_peremen.WIDTH, global_peremen.HIGH))
        global_peremen.screen.blit(fon, (0, 0))
        again = global_peremen.Button("Start over", global_peremen.WIDTH // 2,
                                      global_peremen.HIGH // 2 - global_peremen.HIGH // 6, self.again)
        contin = global_peremen.Button("Continue", global_peremen.WIDTH // 2,
                                       global_peremen.HIGH // 2, self.resume)

        back = global_peremen.Button("Back", global_peremen.WIDTH // 2,
                                     global_peremen.HIGH // 2 + global_peremen.HIGH // 6, self.back)
        btns = [again, contin, back]

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if global_peremen.MOD == "main_menu" or "level" in global_peremen.MOD:
                    return
                if not self.pause:
                    return
            for elem in btns:
                elem.render(global_peremen.screen, events=events)
            pygame.display.flip()
            global_peremen.clock.tick(FPS)


ui = UI()
