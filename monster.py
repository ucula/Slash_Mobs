import random
from spritesheet import SpriteSheet
import pygame as pg
from config import Configs
from ui import AllUI
import math


class Monster_TMP:
    monster = ["slime", "goblin", "hop"]
    def __init__(self, screen, x=0, y=0, health=0, damage=0, level=0, evasion=0):
        self.ui = AllUI(screen)
        self.health = health
        self.damage = damage
        self.level = level
        self.evasion = evasion
        self.x = x
        self.y = y

        self.ready = False

        # For animating
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0
    
    def reduce_hp(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def show_info(self, distance):
        if distance < self.encounter_dist:
            self.ui.draw_prepare_fight()
            self.ready = True
        else:
            self.ui.prep_size = 0
            self.ready = False

    def die(self):
        pass

    def attack(self):
        pass

    def dodge(self):
        pass


class Slime(Monster_TMP):
    def __init__(self, screen, x, y, health=10, damage=1, level=1, evasion=0.1):
        # For Encounter
        self.x_offset = 28
        self.y_offset = 25 
        self.encounter_dist = 25
        super().__init__(screen, x, y, health, damage, level, evasion)
        
    def draw_mon(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/slime.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        return sprite_sheet.get_monster((0, 0), 0, 128, 128, 1, Configs.get('BLACK'))
    
    # Check if player is close. If so, show Fight UI
    def check_distance(self, player):
        a = player.x - (self.x + self.x_offset)
        b = player.y - (self.y + self.y_offset)
        distance = math.hypot(a, b)

        self.show_info(distance)
        # self.check_start()
   
class Goblin(Monster_TMP):
    def __init__(self, screen, x, y, health=30, damage=5, level=2, evasion=0.2):
        # For Encounter
        self.x_offset = 117
        self.y_offset = 133
        self.encounter_dist = 25

        # Skill rate
        self.hunter_instinct_rate = 0.14
        super().__init__(screen, x, y, health, damage, level, evasion)
        
    def hunter_instinct(self):
        self.damage *= 1.2

    def draw_mon(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/goblin.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        return sprite_sheet.get_monster((0, 0), 0, 300, 300, 1, Configs.get('BLACK'))

    # Check if player is close. If so, show Fight UI
    def check_distance(self, player):
        a = player.x - (self.x + self.x_offset)
        b = player.y - (self.y + self.y_offset)
        distance = math.hypot(a, b)
        # print(f"gob=({self.x},{self.y}), char=({player.x},{player.y}), dist={distance}")

        self.show_info(distance)

class Dark_Goblin(Goblin):
    def __init__(self, screen, x, y, health=30, damage=10, level=5, evasion=0.4):
        self.potion_rate = 0.15
        super().__init__(screen, x, y, health, damage, level, evasion)
        self.x_offset = 57
        self.y_offset = 72
    
    def potion(self):
        if self.health == 20:
            random.choice[self.attack(), self.hunter_instinct()]
        else:
            self.health += 5

    def draw_mon(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/dark.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        return sprite_sheet.get_monster((0, 0), 0, 64, 64, 3, Configs.get('BLACK'))
    
    def check_distance(self, player):
        a = player.x - (self.x + self.x_offset)
        b = player.y - (self.y + self.y_offset)
        distance = math.hypot(a, b)
        # print(f"gob=({self.x},{self.y}), char=({player.x},{player.y}), dist={distance}")

        self.show_info(distance)

    
