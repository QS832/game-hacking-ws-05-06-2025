import pygame
import math
import game_settings as gs


# Define colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def add_outline(image, outline_color=(0, 0, 0), thickness=2):
    mask = pygame.mask.from_surface(image)
    outline_surface = pygame.Surface(
        (image.get_width() + thickness * 2, image.get_height() + thickness * 2),
        pygame.SRCALPHA
    )

    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx == 0 and dy == 0:
                continue
            offset = (thickness + dx, thickness + dy)
            mask.to_surface(outline_surface, setcolor=outline_color, unsetcolor=(0, 0, 0, 0), dest=offset)

    outline_surface.blit(image, (thickness, thickness))
    return outline_surface



# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("png/studsec.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.health = 100
        self.velocity_y = 0
        self.on_ground = False
        self.coins = 0

    def update(self, keys, platforms):
        speed = 6
        dx = 0

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            dx = -speed
        if keys[pygame.K_RIGHT]:
            dx = speed

        # Apply horizontal movement and check horizontal collisions
        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:  # Moving right; hit the left side of platform
                    self.rect.right = platform.rect.left
                elif dx < 0:  # Moving left; hit the right side of platform
                    self.rect.left = platform.rect.right

        # Apply gravity
        if not self.on_ground:
            self.velocity_y += 0.5
        else:
            self.velocity_y = 0

        # Jumping mechanic
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = -15

        # Apply vertical movement
        self.rect.y += self.velocity_y

        # Reset on_ground flag before checking
        self.on_ground = False

        # Vertical collision check
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Falling down; hit the top of platform
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity_y = 0
                elif self.velocity_y < 0:  # Moving up; hit the bottom of platform
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0



# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("png/job-appl.webp").convert_alpha()
        original_image = pygame.transform.scale(original_image, (130, 130))
        
        self.image = add_outline(original_image, outline_color=(0, 0, 0), thickness=2)
        
        self.rect = self.image.get_rect()
        self.rect.center = (267, 200)  # Initial position
        self.health = 100
        
    def update(self, player):
        # Only chase the player if they are close enough
        chase_distance = 400  # pixel range

        # Calculate the distance between player and enemy
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance < chase_distance:
            # Move towards the player
            angle = math.atan2(dy, dx)
            self.rect.x += math.cos(angle) * 2
            self.rect.y += math.sin(angle) * 2
       


class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, angle, dmg):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=position)
        self.velocity = 10
        self.dx = math.cos(angle) * self.velocity
        self.dy = math.sin(angle) * self.velocity
        self.dmg = dmg 

        
        # Velocity based on the angle
        self.velocity = [math.cos(angle) * 10, math.sin(angle) * 10]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if (self.rect.right < 0 or self.rect.left >gs.WORLD_HEIGHT or
            self.rect.bottom < 0 or self.rect.top > gs.WORLD_WIDTH):
            self.kill()

