import pygame


def start(screen):
    screen.fill((10, 10, 10))
    font = pygame.font.Font(None, 50)
    font = font.render("Тут как бы игра начинается", True, (100, 100, 100))
    screen.blit(font, (150, 180))