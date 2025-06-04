import pygame
import game_settings as gs
from shop import ShopItem
import json

with open("weapons.json") as f:
    weapons_data = json.load(f)
    
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(60 , 60, 60)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("png/flag.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 100))  # Resize if needed
        self.rect = self.image.get_rect(topleft=(x, y))


# Each level returns a list of platforms
def get_level_platforms(level):
    if level == 1:
        platforms = [
            Platform(0, 580, 1000, 20),
            Platform(300, 500, 100, 20),
            Platform(600, 420, 100, 20),
            Platform(900, 350, 100, 20),
            Platform(1200, 450, 150, 20),
            Platform(1450, 380, 150, 20),
            Platform(1700, 300, 100, 20),
            Platform(1900, 400, 150, 20),
            Platform(2150, 320, 100, 20),
            Platform(2400, 580, 1000, 20),
        ]
        flag_pos = (3350, 480)
        return platforms, flag_pos, pygame.sprite.Group()

    elif level == 2:
        platforms = [
            Platform(0, 580, 800, 20),
            Platform(400, 500, 100, 20),
            Platform(700, 400, 100, 20),
            Platform(1000, 300, 100, 20),
            Platform(1300, 200, 100, 20),
            Platform(1600, 300, 100, 20),
            Platform(1900, 400, 100, 20),
            Platform(2200, 500, 100, 20),
            Platform(2500, 580, 800, 20),
        ]
        flag_pos = (3350, 480)
        return platforms, flag_pos, pygame.sprite.Group()

    elif level == 3:
        platforms = [
            Platform(0, 580, 800, 20),
            Platform(350, 500, 100, 20),
            Platform(700, 420, 100, 20),
            Platform(1050, 340, 100, 20),
            Platform(1400, 260, 100, 20),
            Platform(1750, 340, 100, 20),
            Platform(2100, 420, 100, 20),
            Platform(2450, 500, 100, 20),
            Platform(2750, 580, 1000, 20),
        ]
        flag_pos = (3350, 480)
        return platforms, flag_pos, pygame.sprite.Group()
    elif level == 5:
        platforms = [
            Platform(0, 580, 600, 20),
            Platform(300, 480, 100, 20),
            Platform(600, 380, 100, 20),
            Platform(900, 280, 100, 20),
            Platform(1200, 380, 100, 20),
            Platform(1500, 480, 100, 20),
            Platform(1800, 380, 100, 20),
            Platform(2100, 280, 100, 20),
            Platform(2400, 580, 1000, 20),
        ]
        flag_pos = (3350, 480)
        return platforms, flag_pos, pygame.sprite.Group()

    elif level == 6:
        platforms = [
            Platform(0, 580, 800, 20),
            Platform(400, 500, 100, 20),
            Platform(800, 420, 100, 20),
            Platform(1200, 340, 100, 20),
            Platform(1600, 260, 100, 20),
            Platform(2000, 340, 100, 20),
            Platform(2400, 420, 100, 20),
            Platform(2800, 500, 100, 20),
            Platform(3100, 580, 800, 20),
        ]
        flag_pos = (3350, 480)
        return platforms, flag_pos, pygame.sprite.Group()

    elif level == 7:
        platforms = [
            Platform(0, 580, 1000, 20),
            Platform(1000, 380, 100, 20),
            Platform(1500, 430, 100, 20),
            Platform(1800, 280, 100, 20),
            Platform(2300, 280, 100, 20),
            Platform(2600, 380, 100, 20),
            Platform(2900, 580, 800, 20),
        ]
        flag_pos = (3350, 480)
        return platforms, flag_pos, pygame.sprite.Group()

    elif level == 4:
        platforms = [Platform(0, gs.HEIGHT - 20, 3000, 20)]
        shop_items = pygame.sprite.Group()
        spacing = 200
        x_start = 300
        y = gs.HEIGHT // 2
        i = 0

        # fists
        for fname, fdata in weapons_data["fists"].items():
            if fdata.get("cost", 0) > 0: 
                shop_items.add(ShopItem(fname, fdata["cost"], (x_start + i * spacing, y)))
                i += 1

        # guns
        for gname, gdata in weapons_data["guns"].items():
            if gdata.get("cost", 0) > 0:  
                shop_items.add(ShopItem(gname, gdata["cost"], (x_start + i * spacing, y)))
                i += 1

        # No flag in the shop
        return platforms, (1350, 480), shop_items
    else:
        return [], [], pygame.sprite.Group()
