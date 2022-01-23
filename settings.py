import global_peremen, pygame


class Setting_error(Exception):
    pass


try:
    class Settings:
        def __init__(self):
            self.scroll = global_peremen.Scroll([('screen_size', self.set_size), ('Fps', self.change_fps), ('Volume', self.change_volume)], global_peremen.WIDTH // 2, 20, mod='vertical')
            self.input = global_peremen.Input_set((10, 10), (global_peremen.WIDTH // 4, global_peremen.HIGH // 10), '0123456789 ', [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 32])
            self.mod = ''
            self.close = global_peremen.Button('close', global_peremen.WIDTH, 0, self.close)
            self.close.x = self.close.x - self.close.w

        def set_size(self):
            self.mod = 'Size'

        def change_fps(self):
            self.mod = 'fps'

        def update(self, events):
            self.scroll.update(events)
            self.close.render(global_peremen.screen, events)
            result = self.input.update(events)
            if result:
                if self.mod == 'Size':
                    if len(result.split()) == 2 and result.split()[0].isdigit() and result.split()[1].isdigit():
                        global_peremen.SIZE = global_peremen.WIDTH, global_peremen.HIGH = int(result.split()[0]), int(result.split()[1])
                        global_peremen.screen = pygame.display.set_mode(global_peremen.SIZE)
                        global_peremen.MOD = 'main_menu'
                        global_peremen.font = pygame.font.Font(None, min(global_peremen.SIZE) // 10)
                elif self.mod == 'fps':
                    if len(result.strip().split()) == 1 and result.strip().split()[0].isdigit():
                        global_peremen.fps = int(result.strip().split()[0])
                        global_peremen.MOD = 'main_menu'
                elif self.mod == 'volume':
                    if len(result.strip().split()) == 1 and result.strip().split()[0].isdigit() and int(result.strip().split()[0]) <= 100:
                        pygame.mixer.music.set_volume(int(result.strip().split()[0]) / 100)
                        global_peremen.MOD = 'main_menu'
                        global_peremen.volume = int(result.strip().split()[0]) / 100
                global_peremen.NAME = ''
                global_peremen.enter_nam = None
                global_peremen.choice_menu = None
                global_peremen.in_game_menu = None
                global_peremen.run = False
                global_peremen.new_game = True


        def close(self):
            global_peremen.MOD = 'main_menu'

        def change_volume(self):
            self.mod = 'volume'


    settings = Settings()
except:
    raise Setting_error()