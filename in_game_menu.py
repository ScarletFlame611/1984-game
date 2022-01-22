import global_peremen, pygame, saves


class In_game_menu:
    def __init__(self, bg_image_name, hero_image_name, map_image_name):
        self.bg = pygame.transform.scale(global_peremen.load_image(bg_image_name, colorkey=-1), global_peremen.SIZE)
        self.hero = global_peremen.Button('', global_peremen.WIDTH // 2 - (global_peremen.WIDTH // 14), global_peremen.HIGH // 2 - (global_peremen.HIGH // 6), self.dont_touch, name_image=hero_image_name, size=(global_peremen.WIDTH // 7, global_peremen.HIGH // 3))
        self.map = global_peremen.Button('', global_peremen.WIDTH - (global_peremen.WIDTH // 5), global_peremen.HIGH - (global_peremen.HIGH // 5), self.open_mup, name_image=map_image_name, size=(global_peremen.WIDTH // 5, global_peremen.HIGH // 5))
        self.names = ['1', '2', '3', '4']
        self.buttons = []
        for i in range(len(self.names)):
            clicable = True
            if i - 1 >= 0:
                if self.buttons[i - 1][0].split()[-1] == '0':
                    clicable = False
            if self.names[i] not in global_peremen.levels:
                global_peremen.levels[self.names[i]] = '0'
                if clicable:
                    self.buttons.append([self.names[i] + '. Score: ' + '0', self.open_level, map_image_name, (global_peremen.WIDTH // 5, global_peremen.HIGH // 5), int(self.names[i])])
                else:
                    self.buttons.append([self.names[i] + '. Score: ' + '0', self.open_level, map_image_name, (global_peremen.WIDTH // 5, global_peremen.HIGH // 5), int(self.names[i]), 'clicable'])
            else:
                if clicable:
                    self.buttons.append([self.names[i] + '. Score: ' + str(global_peremen.levels[self.names[i]]), self.open_level, map_image_name, (global_peremen.WIDTH // 5, global_peremen.HIGH // 5), int(self.names[i])])
                else:
                    self.buttons.append([self.names[i] + '. Score: ' + str(global_peremen.levels[self.names[i]]), self.open_level, map_image_name, (global_peremen.WIDTH // 5, global_peremen.HIGH // 5), int(self.names[i]), 'clicable'])
        self.scroll = global_peremen.Scroll(self.buttons, 0 + global_peremen.WIDTH // 40, global_peremen.HIGH // 2)
        self.save = global_peremen.Button('save', global_peremen.WIDTH, 0, saves.save)
        self.save.x = global_peremen.WIDTH - self.save.w
        self.close = global_peremen.Button('close', self.save.x, 0, self.close)
        self.close.x = self.save.x - self.close.w
        self.mod = 'menu'
        self.dont_touch_cd = 0
        text = "don't touch me!"
        self.font = global_peremen.font.render(text, True, (255, 255, 255))

    def close(self):
        if self.mod == 'menu':
            global_peremen.MOD = 'main_menu'
        elif self.mod == 'map':
            self.mod = 'menu'

    def update(self, events):
        if self.mod == 'menu':
            global_peremen.screen.blit(self.bg, (0, 0))
            self.hero.render(global_peremen.screen, events)
            self.map.render(global_peremen.screen, events)
            if self.dont_touch_cd:
                global_peremen.screen.blit(self.font, (self.hero.x + (self.font.get_width() // 2), self.hero.y + (self.font.get_height() // 2)))
                self.dont_touch_cd -= 1
            global_peremen.screen.blit(global_peremen.font.render(global_peremen.NAME, True, (100, 100, 100)), (0, 0))
        elif self.mod == 'map':
            self.scroll.update(events)
        self.save.render(global_peremen.screen, events)
        self.close.render(global_peremen.screen, events)

    def dont_touch(self):
        self.dont_touch_cd = 60

    def open_mup(self):
        self.mod = 'map'

    def open_level(self, num):
        global_peremen.MOD = "level" + str(num)
        self.mod = "menu"
