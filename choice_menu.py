import global_peremen, saves


class Choice_menu:
    def __init__(self):
        buttons = []
        saves_ = saves.all_saves()
        id = 1
        for save in saves_:
            save = save.split('/')
            print(save[-1][:-1] + '-' + str(id))
            buttons.append((save[-1][:-1] + '-' + str(id), self.load, id))
            id += 1
        if buttons:
            self.scroll = global_peremen.Scroll(buttons, global_peremen.WIDTH // 2, global_peremen.HIGH // 2)
        else:
            self.scroll = None

    def update(self, events):
        if self.scroll is not None:
            self.scroll.update(events)
        else:
            global_peremen.MOD = 'main_menu'

    def load(self, id):
        sav = saves.load(id)
        if sav is not None:
            sav = sav.split('/')
            global_peremen.NAME = sav[-1][:-1]
            global_peremen.WIDTH, global_peremen.HIGH = int(sav[0]), int(sav[1])
            global_peremen.MOD = 'in_game_menu'
        else:
            print('нету такого сохранения')


choice_menu = Choice_menu()