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

        self.player = player
        self.w, self.h = screen_width, screen_height
        self.screen = screen
        self.tile = tile_size
        self.walls = wall_group
        self.enemy = enemy
        self.draw_blocks()

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

    def highlighting(self, x, y):
        color = pygame.Color(200, 255, 255)
        self.draw_block(color, x, y, size=2)


board = Board()
player_turns = 5
enemy_turns = 5


# функция боя
def fighting(screen_width, screen_height, tile_size, player, enemy, wall_group, mouse_pos, screen):
    global player_turns, enemy_turns
    board.start(screen_width, screen_height, tile_size, player, enemy, wall_group, screen)
    if enemy.hp > 0 and player.hp > 0:
        return True
    return False
