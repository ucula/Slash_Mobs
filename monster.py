import random
from spritesheet import SpriteSheet
import pygame as pg
from config import Configs
from ui import AllUI
import math


class Monster_TMP:
    monster = ["slime", "goblin", "hop"]
    def __init__(self, screen, x_off=0, y_off=0, x=0, y=0, health=0, damage=0, level=0, evasion=0):
        self.ui = AllUI(screen)
        self.x_offset = x_off
        self.y_offset = y_off
        self.encounter_dist = 25
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.level = level
        self.evasion = evasion

        self.ready = False
        
        # For animating
        self.animation = []
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0

    def reduce_hp(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    # Show mob info and ready for start fight trigger
    def show_info(self):
        self.ui.draw_mob_info()
        self.ready = True
        # print(self.ready)    

    # Calculate dist player from mobs
    def calculate_dist(self, player):
        a = player.x - (self.x + self.x_offset)
        b = player.y - (self.y + self.y_offset)
        distance = math.hypot(a, b)
        return distance 

    def die(self):
        pass

    def attack(self):
        pass

    def dodge(self):
        pass

class Slime(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, health=10, damage=1, level=1, evasion=0.1):
        super().__init__(screen, x_off, y_off, x, y, health, damage, level, evasion)
        self.animation_steps = 6
        self.size = 1
    
    def draw_mon(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/slime.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation):
                self.frame = 0

        for i in range(self.animation_steps):
            self.animation.append(sprite_sheet.get_monster((0, 0), i, 128, 128, self.size, Configs.get('BLACK')))
    
    # Check if player is close. If so, show Fight UI
    def check_distance(self, player):
        distance = self.calculate_dist(player)
        if distance < self.encounter_dist:
            self.show_info()
        else:
            self.ui.prep_size = 0
            self.ready = False
   
class Goblin(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, health=30, damage=5, level=2, evasion=0.2):
        super().__init__(screen, x_off, y_off, x, y, health, damage, level, evasion)
        self.animation_steps = 3
        self.size = 1
        # Skill rate
        self.hunter_instinct_rate = 0.14

    def draw_mon(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/goblin.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation):
                self.frame = 0

        for i in range(self.animation_steps):
            self.animation.append(sprite_sheet.get_monster((0, 0), i, 300, 300, self.size, Configs.get('BLACK')))
    
    def hunter_instinct(self):
        self.damage += 2

    # Check if player is close. If so, show Fight UI
    def check_distance(self, player):
        distance = self.calculate_dist(player)
        if distance < self.encounter_dist:
            self.show_info()
        else:
            self.ui.prep_size = 0
            self.ready = False

class Dark_Goblin(Goblin):
    def __init__(self, screen, x_off, y_off, x, y, health=30, damage=10, level=5, evasion=0.7):
        super().__init__(screen, x_off, y_off, x, y, health, damage, level, evasion)
        self.animation_steps = 3
        self.size = 3

    def draw_mon(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/dark.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        
        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation):
                self.frame = 0

        for i in range(self.animation_steps):
            self.animation.append(sprite_sheet.get_monster((0, 0), i, 64, 64, self.size, Configs.get('BLACK')))
    
    def check_distance(self, player):
        distance = self.calculate_dist(player)
        if distance < self.encounter_dist:
            self.show_info()
        else:
            self.ui.prep_size = 0
            self.ready = False
