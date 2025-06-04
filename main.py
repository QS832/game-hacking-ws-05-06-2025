import pygame
import sys
import ctypes

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stat Tracker")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Stats class using mutable int values
class Stats:
    def __init__(self):
        self.health = ctypes.c_int(23761)
        self.coins  = ctypes.c_int(0)
        self.power  = ctypes.c_int(10)

    def modify(self, key):
        if key == pygame.K_h:
            self.health.value += 1
            print("Health Address:", hex(ctypes.addressof(self.health)))
        elif key == pygame.K_j:
            self.health.value -= 1
            print("Health Address:", hex(ctypes.addressof(self.health)))
        elif key == pygame.K_c:
            self.coins.value += 4
        elif key == pygame.K_v:
            self.coins.value -= 2
        elif key == pygame.K_p:
            self.power.value += 1
        elif key == pygame.K_l:
            self.power.value -= 1

    def display(self, surface):
        stats_text = [
            f"Health: {self.health.value}",
            f"Coins:  {self.coins.value}",
            f"Power:  {self.power.value}",
        ]
        for i, text in enumerate(stats_text):
            rendered = font.render(text, True, BLACK)
            surface.blit(rendered, (20, 30 + i * 40))

# Create the stats object
stats = Stats()

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            stats.modify(event.key)

    # Draw the stats
    stats.display(screen)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
