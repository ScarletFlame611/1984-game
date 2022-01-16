import os, sys, pygame


class Animation:
    def __init__(self, names_files, cd_images, screen, width_screen, height_screen, sounds, colorkey=None, music=None):
        self.images = []
        for elem in names_files:
            self.images.append(pygame.transform.scale(self.load_image(elem, colorkey=colorkey), (width_screen, height_screen)))
        self.images_cd = cd_images
        self.common_cd = 5
        self.screen = screen
        self.music = music
        self.sounds = sounds

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def play(self):
        if self.images != []:
            number = 0
            fps = 10
            clock = pygame.time.Clock()
            running = True
            cd = self.set_cd(number) * fps
            pygame.mixer.music.load(self.music)
            while running:
                screen.fill((0, 0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                if cd == 0:
                    print('here')
                    number += 1
                    if number < len(self.images):
                        cd = self.set_cd(number) * fps
                    else:
                        return True
                cd -= 1
                screen.blit(self.images[number], (0, 0))
                clock.tick(fps)
                pygame.display.update()
        else:
            print('в этой анимвции нету изображений')

    def set_cd(self, number):
        if 0 <= number < len(self.images_cd):
            return self.images_cd[number]
        return self.common_cd


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('свой курсор мыши')
    size = width, height = 300, 450
    screen = pygame.display.set_mode(size)
    animation = Animation(['third.png', 'first.jpg', 'second.jpg'], [], screen, width, height, colorkey=-1)
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    animation.play()
        pygame.display.update()