import random
from spritesheet import SpriteSheet
import pygame as pg
from config import Configs
import math

class Monster_TMP:
    monster = ["slime", "goblin"]
    def __init__(self, x, y, health, damage, level, evasion):
        self.health = health
        self.damage = damage
        self.level = level
        self.evasion = evasion
        self.x = x
        self.y = y

        # For animating
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0
        
    def reduce_hp(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        pass

    def attack(self):
        pass

    def dodge(self):
        pass


class Slime(Monster_TMP):
    def __init__(self, x, y, health=10, damage=1, level=1, evasion=0.1):
        # For Encounter
        self.x_offset = 28
        self.y_offset = 25 
        self.encounter_dist = 25
        super().__init__(x, y, health, damage, level, evasion)
        
    def draw_mon(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/slime.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        return sprite_sheet.get_monster((0, 0), 0, 128, 128, 1, Configs.get('BLACK'))
    
    # Check if player is close. If so, show Fight UI
    def check_distance(self, player):
        a = player.x - (self.x + self.x_offset)
        b = player.y - (self.y + self.y_offset)
        distance = math.hypot(a, b)

        if distance < self.encounter_dist:
            # กันไว้ใส่ UI
            print("encounter")
            pass
   
class Goblin(Monster_TMP):
    def __init__(self, x, y, health=30, damage=5, level=2, evasion=0.2):
        # For Encounter
        self.x_offset = 117
        self.y_offset = 133
        self.encounter_dist = 25

        # Skill rate
        self.hunter_instinct_rate = 0.14
        super().__init__(x, y, health, damage, level, evasion)
        
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

        if distance < self.encounter_dist:
            # กันไว้ใส่ UI
            print("encounter")
            pass

class Hop_Goblin(Goblin):
    def __init__(self):
        super().__init__(health=20, evasion=0.15)
        self.potion_rate = 0.15

    def potion(self):
        if self.health == 20:
            random.choice[self.attack(), self.hunter_instinct()]
        else:
            self.health += 5
