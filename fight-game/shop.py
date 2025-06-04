import pygame

class ShopItem(pygame.sprite.Sprite):
    def __init__(self, name, cost, pos, color=(200,200,0), radius=20):
        super().__init__()
        self.name = name            # e.g. "shotgun" or "heavy_punch"
        self.cost = cost
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        
        # render the first letter or icon
        font = pygame.font.Font(None, 24)
        text = font.render(name[0].upper(), True, (0,0,0))
        text_rect = text.get_rect(center=(radius, radius))
        self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect(center=pos)
