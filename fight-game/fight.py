import pygame
import math
import random
 
from weapons import WeaponSystem
from platforms import get_level_platforms,Flag
from entities import Player, Enemy, Projectile


import game_settings as gs
import json

with open("weapons.json") as f:
    weapons_data = json.load(f)

def respawn_enemy_on_platform(platforms, player, enemy, min_dist=200):
    """
    Pick a random platform and a random x‐coordinate on it, but ensure 
    that the chosen x is at least min_dist pixels from the player's center.
    """
    while True:
        plat = random.choice(platforms)
        x = random.randint(plat.rect.left, plat.rect.right)
        if abs(x - player.rect.centerx) >= min_dist:
            enemy.rect.midbottom = (x, plat.rect.top)
            break

    # reset health, alive flag, re‐add if needed:
    enemy.health = 100
    return

def draw_main_menu(screen):
    screen.fill(gs.WHITE)
    
    font = pygame.font.Font(None, 72)
    title_text = font.render("Box Fight", True, (0, 0, 0))
    screen.blit(title_text, (gs.WIDTH // 2 - title_text.get_width() // 2, 150))
    
    button_font = pygame.font.Font(None, 48)
    button_text = button_font.render("Start", True, (255, 255, 255))
    button_rect = pygame.Rect(gs.WIDTH // 2 - 100, 300, 200, 60)
    pygame.draw.rect(screen, (0, 128, 0), button_rect)
    screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                              button_rect.centery - button_text.get_height() // 2))
    
    return button_rect


def show_menu():
    in_menu = True
    while in_menu:
        button_rect = draw_main_menu(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    in_menu = False


# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((gs.WIDTH, gs.HEIGHT))
pygame.display.set_caption("Box Fight")
camera_offset_x = 0

# Initialize player and enemy
player = Player()
enemy = Enemy()
enemy_dead = False  

# Platform
current_level = 1

platforms, flag_pos, shop_items = get_level_platforms(current_level)
flag = Flag(*flag_pos)


background_img = pygame.image.load("png/bg.png").convert()
background_img = pygame.transform.scale(background_img, (gs.WIDTH, gs.HEIGHT))

# Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, *platforms,flag) 
all_sprites.add(shop_items)

projectiles = pygame.sprite.Group()

# Setup weapons
weapon_system = WeaponSystem(weapons_data, player, enemy, all_sprites, projectiles)


# Main game loop
running = True
clock = pygame.time.Clock()

just_pressed_r = just_q = just_e = just_z = just_x = just_l = False
messages = []



show_menu()
  
while running:
    screen.fill(gs.WHITE)
    now = pygame.time.get_ticks()
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.blit(background_img, (0, 0))

    # Handle key presses
    keys = pygame.key.get_pressed()
    player.update(keys, platforms)  
    
    

    # ----------------------------------------#
    #                                         #
    #       Levels - TODO: Make them          #
    #                                         #
    # ----------------------------------------#

  
    # On level switch
    if keys[pygame.K_l] or player.rect.colliderect(flag.rect):
        if not just_l:
            just_l = True
            current_level = (current_level % 7) + 1

            # clear out old platforms, flag, shop items, and enemy
            for sprite in platforms:
                all_sprites.remove(sprite)
            if flag:
                all_sprites.remove(flag)
            all_sprites.remove(*shop_items.sprites())

            if enemy in all_sprites:
                all_sprites.remove(enemy)

            # load new platforms, flag, shop_items
            platforms, flag_pos, shop_items = get_level_platforms(current_level)
            if flag_pos is not None:
                flag = Flag(*flag_pos)
                all_sprites.add(flag)
            else:
                flag = None

            # Always add player
            all_sprites.add(player)

            # Add enemy only if NOT shop (level 4)
            if current_level != 4:
                all_sprites.add(enemy)
                # respawn enemy on a platform
                respawn_enemy_on_platform(platforms, player, enemy)
                enemy_dead = False
            else:
                enemy_dead = True  # mark enemy dead in shop (or inactive)

            # Add platforms and shop items
            all_sprites.add(*platforms, *shop_items)

            # Reset player position and camera
            player.rect.center = (100, 500)
            camera_offset_x = 0
    else:
        just_l = False

            
    # SHOP PURCHASES 
    if current_level == 4:
        hits = pygame.sprite.spritecollide(player, shop_items, dokill=False)
        for item in hits:
            if player.coins >= item.cost:
                player.coins -= item.cost
                weapon_system.unlock(item.name)
                # immediately equip what you just bought
                if item.name in weapons_data["guns"]:
                    weapon_system.set_current_gun(item.name)
                else:
                    weapon_system.set_current_fist(item.name)
                item.kill()
                messages.append((f"Bought {item.name} for {item.cost}c", now))
            else:
                messages.append(("Not enough coins!", now))

        # keep only the last five messages
        messages = messages[-5:]


    
    # ----------------------------------------#
    #                                         #
    #             Attack handling             #
    #                                         #
    # ----------------------------------------#
    
    # ——— GUN CYCLE ———
    if keys[pygame.K_q]:
        if not just_q:
            weapon_system.cycle_gun(-1)
            just_q = True
    else:
        just_q = False

    if keys[pygame.K_e]:
        if not just_e:
            weapon_system.cycle_gun(1)
            just_e = True
    else:
        just_e = False

    # ——— FIST CYCLE ———
    if keys[pygame.K_z]:
        if not just_z:
            weapon_system.cycle_fist(-1)
            just_z = True
    else:
        just_z = False

    if keys[pygame.K_x]:
        if not just_x:
            weapon_system.cycle_fist(1)
            just_x = True
    else:
        just_x = False


    # Update weapon 
    weapon_system.handle_gun_fire(now, keys[pygame.K_w])
    
    #Reload
    weapon_system.update_reload(now)
    
    if keys[pygame.K_r]:
        if not just_pressed_r and not weapon_system.is_reloading and weapon_system.ammo < weapon_system.max_ammo:
            weapon_system.start_reload()
        just_pressed_r = True
    else:
        just_pressed_r = False


    if keys[pygame.K_s]:
        weapon_system.fist_attack(screen, gs, camera_offset_x)
    else:
        weapon_system.fist_attacking = False
        weapon_system.fist_dmg_applied = False
    
   

    # Update all projectiles
    projectiles.update()

    # Check for projectile collisions with enemy
    for projectile in projectiles:
        if projectile.rect.colliderect(enemy.rect):
            enemy.health -= projectile.dmg
            projectile.kill()  # Remove the projectile when it hits the enemy

    
   

   
    # ----------------------------------------#
    #                                         #
    #                  DEATH                  #
    #                                         #
    # ----------------------------------------#
    
    # Enemy death
    enemy.update(player)
    
    if enemy.health <= 0 and not enemy_dead:
        # Reward player with random coins 
        coin_reward = random.randint(5, 8)
        player.coins += coin_reward
        print(f"Enemy defeated! You earned {coin_reward} coins.")

        # Remove enemy
        all_sprites.remove(enemy)
        enemy.kill() #Remove to spawn enemies after
        enemy_dead = True
    
    # Player death
    # Check if player fell below the bottom boundary 
    if player.rect.top > gs.HEIGHT or (not enemy_dead and enemy.rect.colliderect(player.rect)):
        font = pygame.font.Font(None, 72)
        message = font.render("Died :/", True, (255, 0, 0))
        screen.fill(gs.WHITE)
        screen.blit(message, (gs.WIDTH // 2 - message.get_width() // 2, gs.HEIGHT // 2 - message.get_height() // 2))
        pygame.display.flip()

        # Pause and wait for any key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

        # Reset player and enemy positions
        player.rect.center = (100, 500)
        if player.coins >= 2:
            player.coins -=2 

        # Reset enemy position on a random platform
        respawn_enemy_on_platform(platforms, player, enemy)
        enemy_dead = False
        
        if enemy not in all_sprites:
             all_sprites.add(enemy)

        # Also reset any other state as needed (ammo, coins, etc.)
        weapon_system.ammo = weapon_system.max_ammo
        weapon_system.is_reloading = False
        weapon_system.reload_start = 0

        # Reset projectiles
        for proj in projectiles:
            proj.kill()

   
   
    # ----------------------------------------#
    #                                         #
    #                 DISPLAY                 #
    #                                         #
    # ----------------------------------------#
     
    
    # Camera FOLLOW logic 
    camera_offset_x = player.rect.centerx - gs.WIDTH // 2
    if camera_offset_x < 0:
        camera_offset_x = 0

    # Draw everything
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_offset_x, sprite.rect.y))

    # Also draw projectiles manually
    for proj in projectiles:
        screen.blit(proj.image, (proj.rect.x - camera_offset_x, proj.rect.y))
    
    
    font = pygame.font.Font(None, 36)
    player_health_text = font.render(f"Player HP: {player.health}", True, (0, 0, 0))
    screen.blit(player_health_text, (10, 10))
    # enemy_health_text = font.render(f"Enemy HP: {enemy.health}", True, (0, 0, 0))
    # screen.blit(enemy_health_text, (gs.WIDTH - 200, 10))
    
    gun_text = font.render(f"{weapon_system.current_gun.title()} | Ammo: {weapon_system.ammo}/{weapon_system.max_ammo}", True, (0,0,0))
    screen.blit(gun_text, (10, 50))
    if weapon_system.is_reloading:
        elapsed = now - weapon_system.reload_start
        pct = min(elapsed / weapon_system.reload_duration, 1.0)
        pygame.draw.rect(screen, gs.RED, (10, 80, 100, 10), 2)
        pygame.draw.rect(screen, gs.GREEN, (10, 80, 100 * pct, 10))
    
    coin_text = font.render(f"Coins: {player.coins}", True, (0, 0, 0))
    screen.blit(coin_text, (10, 90))

    # Draw enemy health bar 
    if not enemy_dead:
        bar_width = 50
        bar_height = 6
        bar_x = enemy.rect.centerx - bar_width // 2 - camera_offset_x
        bar_y = enemy.rect.top - 10

        health_pct = max(enemy.health / 100, 0)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Background red
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_pct, bar_height))  # Green health
        
    # DRAW SHOP UI if in shop
    if current_level == 4:
        font = pygame.font.Font(None, 36)
        instr = font.render("Touch orbs to buy. Press L to leave shop.", True, (0,0,0))
        screen.blit(instr, (gs.WIDTH//2 - instr.get_width()//2, 20))

        for orb in shop_items:
            cost_txt = font.render(str(orb.cost), True, (0,0,0))
            screen.blit(cost_txt, (orb.rect.centerx - cost_txt.get_width()/2 - camera_offset_x,
                                orb.rect.bottom + 5))

    # DRAW messages
    # Remove messages older than 3 seconds
    messages = [(msg, ts) for msg, ts in messages if now - ts < 3000]

    for idx, (msg, ts) in enumerate(messages):
        color = (255, 0, 0) if msg.startswith("Not enough") else (0, 128, 0)
        txt_surf = font.render(msg, True, color)
        screen.blit(txt_surf, (10, gs.HEIGHT - 20 * (len(messages) - idx)))



    # Show equipped fists as well
    fist_text = font.render(
        f"Fist: {weapon_system.current_fist.replace('_',' ').title()}",
        True, (0, 0, 0)
    )
    screen.blit(fist_text, (10, 130))
    
    # Ammo / gun
    gun_text = font.render(
        f"{weapon_system.current_gun.title()} | Ammo: {weapon_system.ammo}/{weapon_system.max_ammo}",
        True, (0,0,0)
    )
    screen.blit(gun_text, (10, 50))

    # Coins
    coin_text = font.render(f"Coins: {player.coins}", True, (0, 0, 0))
    screen.blit(coin_text, (10, 90))

    # Currently equipped fist
    fist_text = font.render(
        f"Fist: {weapon_system.current_fist.replace('_',' ').title()}",
        True, (0, 0, 0)
    )
    screen.blit(fist_text, (10, 130))


    # Update the screen
    pygame.display.flip()

    # Frame rate control
    clock.tick(gs.FPS)

pygame.quit()
