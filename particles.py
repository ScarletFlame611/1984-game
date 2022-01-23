import pygame
import os
import sys
import random


class Particles_error(Exception):
    pass


try:
    # константы и группа спрайтов
    GRAVITY = 1
    particles = pygame.sprite.Group()
    screen_rect = None


    # класс частиц
    class Particle(pygame.sprite.Sprite):
        # инициализация
        def __init__(self, pos, dx, dy, fires, scales):
            super().__init__(particles)
            scale = random.choice(scales)
            self.image = pygame.transform.scale(random.choice(fires), (scale, scale))
            self.rect = self.image.get_rect()
            self.velocity = [dx, dy]
            self.rect.x, self.rect.y = pos
            self.gravity = GRAVITY

        # функция для передвижения частиц
        def update(self):
            self.velocity[1] += self.gravity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            if not self.rect.colliderect(screen_rect):
                self.kill()


    # подгружаем картинки
    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image
        return image


    # создание картинок
    def create_particles(position, fires, scales, scr_rect, particle_count=20):
        global screen_rect
        screen_rect = scr_rect
        numbers = range(-5, 6)
        fires = [load_image(elem, colorkey=-1) for elem in fires]
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers), fires, scales)
except:
    raise Particles_error()