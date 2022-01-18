import global_peremen, saves, in_game_menu


class Choice_menu:
    def __init__(self):
        buttons = []
        saves_ = saves.all_saves()
        id = 1
        self.close = global_peremen.Button('close', global_peremen.WIDTH, 0, self.close)
        self.close.x = self.close.x - self.close.w
        for save in saves_:
            save = save.split(',')
            buttons.append((save[-1][:-1] + '-' + str(id), self.load, id))
            id += 1
        if buttons:
            self.scroll = global_peremen.Scroll(buttons, global_peremen.WIDTH // 2, global_peremen.HIGH // 2)
        else:
            self.scroll = None

    def update(self, events):
        self.close.render(global_peremen.screen, events)
        if self.scroll is not None:
            self.scroll.update(events)
        else:
            global_peremen.MOD = 'main_menu'

    def close(self):
        global_peremen.MOD = 'main_menu'

    def load(self, id):
        sav = saves.load(id)
        global_peremen.index = id
        if sav is not None:
            sav = sav.split(',')
            for level in sav[:-1]:
                global_peremen.levels[level.split(':')[0]] = level.split(':')[1]
            global_peremen.NAME = sav[-1][:-1]
            global_peremen.MOD = 'in_game_menu'
            global_peremen.choice_menu = None
            global_peremen.in_game_menu = in_game_menu.In_game_menu('bg.png', 'player.png', 'map.png')
        else:
            print('нету такого сохранения')
