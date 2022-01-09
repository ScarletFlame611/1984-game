import global_peremen, pygame

class In_game_menu:
    def __init__(self, bg_image_name, hero_image_name, map_image_name):
        self.bg = pygame.transform.scale(global_peremen.load_image(bg_image_name, colorkey=-1), global_peremen.SIZE)
        self.hero = pygame.transform.scale(global_peremen.load_image(hero_image_name, colorkey=-1), (global_peremen.WIDTH // 7, global_peremen.HIGH // 3))
        self.map = pygame.transform.scale(global_peremen.load_image(map_image_name, colorkey=-1), (global_peremen.WIDTH // 7, global_peremen.HIGH // 5))

    def update(self):
        global_peremen.screen.blit(self.bg, (0, 0))
        global_peremen.screen.blit(self.hero, (global_peremen.WIDTH // 2 - (self.hero.get_width() // 2), global_peremen.HIGH // 2- (self.hero.get_height() // 2)))
        global_peremen.screen.blit(self.map, (global_peremen.WIDTH - self.map.get_width(), global_peremen.HIGH - self.map.get_height()))

in_game_menu = In_game_menu('box.png', 'player.png', 'floor.png')