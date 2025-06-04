import math
import pygame
from entities import Projectile
import numpy as np

class WeaponSystem:
    def __init__(self, weapons_data, player, enemy, all_sprites, projectiles):
        self.weapons_data = weapons_data
        self.player = player
        self.enemy = enemy
        self.all_sprites = all_sprites
        self.projectiles = projectiles

        # --- UNLOCK TRACKING ---
        # start with only the basic weapons unlocked
        self.unlocked_fists = {"basic_punch"}
        self.unlocked_guns   = {"pistol"}

        # current selection
        self.current_fist = "basic_punch"
        self.current_gun   = "pistol"
        self.set_current_gun(self.current_gun)
        
        # fist state
        self.fist_attacking    = False      
        self.fist_start_time   = 0         
        self.fist_dmg_applied  = False    

        # reload / fire state
        self.is_reloading      = False
        self.reload_start      = 0
        self.last_shot_time    = 0
        self.just_pressed_w    = False

    # -------------------------------
    #   EQUIP / UNLOCK FUNCTIONALITY
    # -------------------------------
    def unlock(self, name):
        """Call this when the player buys a weapon orb in the shop."""
        if name in self.weapons_data["fists"]:
            self.unlocked_fists.add(name)
        elif name in self.weapons_data["guns"]:
            self.unlocked_guns.add(name)
        else:
            print(f"[WeaponSystem] Cannot unlock unknown weapon '{name}'")

    def set_current_fist(self, fist_name):
        """Switch to a punch—only if it’s been unlocked."""
        if fist_name in self.unlocked_fists:
            self.current_fist = fist_name
        else:
            print(f"[WeaponSystem] Fist '{fist_name}' is locked!")

    def set_current_gun(self, gun_name):
        """Switch to a gun—only if it’s been unlocked."""
        if gun_name not in self.unlocked_guns:
            print(f"[WeaponSystem] Gun '{gun_name}' is locked!")
            return

        self.current_gun = gun_name
        stats = self.weapons_data["guns"][gun_name]
        self.max_ammo        = stats["ammo"]
        self.ammo            = self.max_ammo
        self.reload_duration = stats["reload_speed"] * 1000  # ms
        self.is_reloading    = False
        self.reload_start    = 0
        self.last_shot_time  = 0
        self.gun_mode        = stats["mode"]

    # -------------------------------
    #   RELOADING / FIRING
    # -------------------------------
    def start_reload(self):
        self.is_reloading = True
        self.reload_start = pygame.time.get_ticks()

    def update_reload(self, now):
        if self.is_reloading and now - self.reload_start >= self.reload_duration:
            self.ammo = self.max_ammo
            self.is_reloading = False

    def handle_gun_fire(self, now, key_pressed):
        if key_pressed:
            if not self.just_pressed_w:
                self.just_pressed_w = True
                if self.gun_mode == "manual":
                    self.fire_gun(now)
            elif self.gun_mode == "auto":
                self.fire_gun(now)
        else:
            self.just_pressed_w = False

    def fire_gun(self, now):
        if self.is_reloading or self.ammo <= 0:
            return

        stats = self.weapons_data["guns"][self.current_gun]
        fire_interval = stats["firerate"] * 1000
        if now - self.last_shot_time < fire_interval:
            return
        
        # aim at living enemy, or straight right if dead
        if self.enemy.health > 0:
            dx = self.enemy.rect.centerx - self.player.rect.centerx
            dy = self.enemy.rect.centery  - self.player.rect.centery
            angle = math.atan2(dy, dx)
        else:
            angle = 0
            
        proj = Projectile(self.player.rect.center, angle, stats["dmg"])
        self.projectiles.add(proj)
        self.all_sprites.add(proj)

        self.ammo           -= 1
        self.last_shot_time = now

        if self.ammo == 0:
            self.start_reload()

    # -------------------------------
    #     FIST (MELEE) ATTACK
    # -------------------------------
    def fist_attack(self, screen, gs, camera_offset_x):
        # guard locked
        if self.current_fist not in self.unlocked_fists:
            return

        stats   = self.weapons_data["fists"][self.current_fist]
        dmg     = stats["dmg"]
        range_  = stats["range"]
        size    = stats["size"]
        duration= stats["duration"]

        now     = pygame.time.get_ticks() / 1000  # seconds

        if not self.fist_attacking:
            self.fist_attacking   = True
            self.fist_start_time  = now
            self.fist_dmg_applied = False

        elapsed = now - self.fist_start_time

        if elapsed <= duration:
            dx    = self.enemy.rect.centerx - self.player.rect.centerx
            dy    = self.enemy.rect.centery  - self.player.rect.centery
            angle = math.atan2(dy, dx)

            end_x = self.player.rect.centerx + math.cos(angle) * range_
            end_y = self.player.rect.centery  + math.sin(angle) * range_

            fist_rect = pygame.Rect(
                end_x - size[0]/2, end_y - size[1]/2,
                size[0], size[1]
            )

            # draw
            adj = fist_rect.copy()
            adj.x -= camera_offset_x
            pygame.draw.rect(screen, gs.BLUE, adj)

            # apply damage once per swing
            if (not self.fist_dmg_applied
                and self.enemy.rect.colliderect(fist_rect)
            ):
                self.enemy.health -= dmg
                self.fist_dmg_applied = True
        else:
            # finished
            self.fist_attacking   = False
            self.fist_dmg_applied = False
    
    def cycle_gun(self, direction):
        guns = sorted(self.unlocked_guns)
        idx = guns.index(self.current_gun)
        self.set_current_gun(guns[(idx + direction) % len(guns)])

    def cycle_fist(self, direction):
        fists = sorted(self.unlocked_fists)
        idx = fists.index(self.current_fist)
        self.set_current_fist(fists[(idx + direction) % len(fists)])

