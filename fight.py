import pygame
import os
import sys
import time


# класс для графического интерфейса
class UI:
    def show(self):
        pass


# класс для доски из клеток во время боя
class Board:
    # самое начало боя
    def start(self, screen_width, screen_height, tile_size, player, enemy, wall_group, screen):
        self.x = screen_width // tile_size
        self.y = screen_height // tile_size
        self.player = player
        self.w, self.h = screen_width, screen_height
        self.screen = screen
        self.tile = tile_size
        self.walls = wall_group
        self.enemy = enemy
        self.draw_blocks()
        self.turn = None

    # отрисовка всех блоков серым цветом
    def draw_blocks(self):
        color = pygame.Color(100, 100, 100)
        play_x = self.player.rect.x // self.tile
        play_y = self.player.rect.y // self.tile
        self.player.rect.x = play_x * self.tile + 10
        self.player.rect.y = play_y * self.tile + 5
        for x in range(self.x):
            for y in range(self.y):
                self.draw_block(color, x, y)

    # отрисовка блока x, y
    def draw_block(self, color, x, y, size=1):
        for elem in self.walls:
            if elem.rect.x // self.tile == x and elem.rect.y // self.tile == y:
                break
        else:
            pygame.draw.rect(self.screen, color, (self.tile * x, self.tile * y, self.tile, self.tile), size)

    # очередь хода игрока
    def player_turn(self, screen, turns, wall_group, mouse_pos):
        self.turn = "Player"
        color = pygame.Color(200, 200, 200)
        self.draw_blocks()
        x1, y1 = self.player.rect.x // self.tile, self.player.rect.y // self.tile
        for x2 in range(self.x):
            for y2 in range(self.y):
                if abs(x2 - x1) + abs(y2 - y1) <= turns:
                    self.draw_block(color, x2, y2)
                    if mouse_pos[0] // self.tile == x2 and mouse_pos[1] // self.tile == y2:
                        self.highlighting(x2, y2)
        if player_turns <= 0:
            return False
        return True

    # очередь хода врага
    def enemy_turn(self, screen, turns, wall_group, mouse_pos):
        self.turn = "Enemy"
        color = pygame.Color(200, 200, 200)
        self.draw_blocks()
        x1, y1 = self.enemy.rect.x // self.tile, self.enemy.rect.y // self.tile
        for x2 in range(self.x):
            for y2 in range(self.y):
                if abs(x2 - x1) + abs(y2 - y1) <= turns:
                    self.draw_block(color, x2, y2)
                    if mouse_pos[0] // self.tile == x2 and mouse_pos[1] // self.tile == y2:
                        self.highlighting(x2, y2)

    # выделение клетки x, y
    def highlighting(self, x, y):
        color = pygame.Color(200, 255, 255)
        self.draw_block(color, x, y, size=2)

    # перемещение игрока на клетку x, y
    def move_player(self, x, y):
        global player_turns
        player_turns -= abs(x - self.player.rect.x // self.tile + y - self.player.rect.y // self.tile)
        for elem in self.walls:
            if elem.rect.x // self.tile == x and elem.rect.y // self.tile == y:
                break
        else:
            print(player_turns)
            if player_turns >= 0:
                self.player.rect.x = x * self.tile
                self.player.rect.y = y * self.tile
                self.player.update((x, y))
            else:
                return False

    # передвежение игрока по щелчку мыши
    def walk(self, x_end, y_end):
        x_start, y_start = self.player.rect.x // self.tile, self.player.rect.y // self.tile
        x = True if abs(x_end - x_start) > 0 else False
        y = True if abs(y_end - y_start) > 0 else False
        if y and x:
            y_step = (y_end - y_start) // abs(y_end - y_start)
            x_step = (x_end - x_start) // abs(x_end - x_start)
            for i in range(y_start + y_step, y_end + y_step, y_step):
                for j in range(x_start + x_step, x_end + x_step, x_step):
                    self.move_player(j, i)
        elif x:
            x_step = (x_end - x_start) // abs(x_end - x_start)
            for j in range(x_start + x_step, x_end + x_step, x_step):
                self.move_player(j, y_end)
        elif y:
            y_step = (y_end - y_start) // abs(y_end - y_start)
            for i in range(y_start + y_step, y_end + y_step, y_step):
                self.move_player(x_end, i)
        else:
            pass

    # атака на букву K
    def attack_for_K(self):
        self.enemy.hp -= 5
        if self.enemy.hp <= 0:
            return False
        return True


board = Board()
player_turns = 5
enemy_turns = 5


# функция боя
def fighting(screen_width, screen_height, tile_size, player, enemy, wall_group, mouse_pos, screen):
    global player_turns, enemy_turns
    board.start(screen_width, screen_height, tile_size, player, enemy, wall_group, screen)
    player_turn = board.player_turn(screen, player_turns, wall_group, mouse_pos)
    if not player_turn:
        board.enemy_turn(screen, player_turns, wall_group, mouse_pos)

    if enemy.hp > 0 and player.hp > 0:
        return True
    return False
