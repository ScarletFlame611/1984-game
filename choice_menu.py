import global_peremen, saves, in_game_menu


class Choice_menu_error(Exception):
    pass


try:
    class Choice_menu:
        def __init__(self, delete_mod=False):
            buttons = []
            saves_ = saves.all_saves()
            id = 1
            self.delete_mod = delete_mod
            self.close = global_peremen.Button('close', global_peremen.WIDTH, 0, self.close)
            self.close.x = self.close.x - self.close.w
            self.delete = global_peremen.Button('delete_mod', self.close.x, 0, self.set_delete_mod)
            self.delete.x -= self.delete.w
            for save in saves_:
                save = save.split(',')
                buttons.append((save[-1][:-2] + '-' + str(id), self.load, id))
                id += 1
            if buttons:
                self.scroll = global_peremen.Scroll(buttons, global_peremen.WIDTH // 2, global_peremen.HIGH // 2)
            else:
                self.scroll = None
            self.font = self.font = global_peremen.font.render('DELETE_MOD_ON!', True, (255, 255, 255))

        def set_delete_mod(self):
            if self.delete_mod:
                self.delete_mod = False
            else:
                self.delete_mod = True

        def update(self, events):
            self.close.render(global_peremen.screen, events)
            if self.delete_mod:
                global_peremen.screen.blit(self.font, (global_peremen.WIDTH // 2 - self.font.get_width() // 2, global_peremen.HIGH // 4))
            self.delete.render(global_peremen.screen, events)
            if self.scroll is not None:
                self.scroll.update(events)
            else:
                global_peremen.MOD = 'main_menu'

        def close(self):
            global_peremen.MOD = 'main_menu'
            global_peremen.choice_menu = None

        def load(self, id):
            if self.delete_mod:
                saves.delete(id)
                global_peremen.choice_menu = Choice_menu(delete_mod=True)
            else:
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
except Exception:
    raise Choice_menu_error()
