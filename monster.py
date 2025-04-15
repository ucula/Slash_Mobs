import random
from spritesheet import SpriteSheet
import pygame as pg
from config import Configs
import math

class Monster_TMP:
    def __init__(self, name, health, damage, level, evasion):
        self.name = name
        self.health = health
        self.damage = damage
        self.level = level
        self.evasion = evasion

        # Encounter
        self.x_offset = 28
        self.y_offset = 25 
        self.encounter_dist = 25

        # For animating
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0

    # Check if player is close. If so, show Fight UI
    def check_distance(self, player):
        a = player.x - (self.x + self.x_offset)
        b = player.y - (self.y + self.y_offset)
        distance = math.hypot(a, b)

        if distance < self.encounter_dist:
            # กันไว้ใส่ UI
            # print("encounter")
            pass
        
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
    def __init__(self, x=0, y=0, name='slime', health=10, damage=1, level=1, evasion=0.1):
        self.x = x
        self.y = y
        self.animation = []
        self.animation_steps = 3
        super().__init__(name, health, damage, level, evasion)
        
    def draw_slime(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/Slime1_Idle_body.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        return sprite_sheet.get_slime((0, 0), 0, 128, 128, 1, Configs.get('BLACK'))

        # current_time = pg.time.get_ticks()
        # if current_time - self.last_up >= self.cool_down:
        #     self.frame += 1
        #     self.last_up = current_time
        #     if self.frame >= len(self.animation):
        #         self.frame = 0

        # for i in range(self.animation_steps):
        #     self.animation.append(sprite_sheet.get_slime((0, 0), i, 128, 128, 1, Configs.get('BLACK')))

    
class Goblin(Monster_TMP):
    def __init__(self):
        super().__init__(name="goblin", health=10, evasion=0.1)
        self.hunter_instinct_rate = 0.14
    
    def hunter_instinct(self):
        self.damage *= 1.2

class Hop_Goblin(Goblin):
    def __init__(self):
        super().__init__(name="hop_goblin", health=20, evasion=0.15)
        self.potion_rate = 0.15

    def potion(self):
        if self.health == 20:
            random.choice[self.attack(), self.hunter_instinct()]
        else:
            self.health += 5
