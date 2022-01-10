import global_peremen, pygame

class In_game_menu:
    def __init__(self, bg_image_name, hero_image_name, map_image_name):
        self.bg = pygame.transform.scale(global_peremen.load_image(bg_image_name, colorkey=-1), global_peremen.SIZE)
        self.hero = global_peremen.Button('', global_peremen.WIDTH // 2 - (global_peremen.WIDTH // 14), global_peremen.HIGH // 2 - (global_peremen.HIGH // 6), self.dont_touch, name_image=hero_image_name, size=(global_peremen.WIDTH // 7, global_peremen.HIGH // 3))
        self.map = global_peremen.Button('', global_peremen.WIDTH - (global_peremen.WIDTH // 5), global_peremen.HIGH - (global_peremen.HIGH // 5), self.open_mup, name_image=map_image_name, size=(global_peremen.WIDTH // 5, global_peremen.HIGH // 5))
        self.mod = 'menu'
        self.dont_touch_cd = 0

    def update(self, events):
        if self.mod == 'menu':
            global_peremen.screen.blit(self.bg, (0, 0))
            self.hero.render(global_peremen.screen, events)
            self.map.render(global_peremen.screen, events)
            if self.dont_touch_cd:
                text = "don't touch me!"
                font = pygame.font.Font(None, 50)
                font = font.render(text, True, (255, 255, 255))
                global_peremen.screen.blit(font, (self.hero.x + (font.get_width() // 2), self.hero.y + (font.get_height() // 2)))
                self.dont_touch_cd -= 1

        elif self.mod == 'map':
            print('here')

    def dont_touch(self):
        self.dont_touch_cd = 60


    def open_mup(self):
        self.mod = 'map'

in_game_menu = In_game_menu('bg.png', 'player.png', 'map.png')