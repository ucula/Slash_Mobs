import random
from spritesheet import SpriteSheet
import pygame as pg
from config import Configs
from ui import AllUI
import math

class Monster_TMP:
    monster1 = ['SLIME', 'GOBLIN', 'DARK']
    monster2 = ['SCORPION', 'BLUE', 'PURPLE']
    monster3 = ['MINOTAUR1', 'MINOTAUR2', 'MINOTAUR3']
    monster4 = ['VAMPIRE1', 'VAMPIRE2', 'VAMPIRE3']

    def __init__(self, screen, x_off=0, y_off=0, x=0, y=0, name="", health=0, damage=0, level=0, evasion=0,
                steps=0, size=0, pixel=0, exp=0, coin=0):
        self.ui = AllUI(screen)
        self.font = pg.font.Font(None, 30)
        self.prep_size = 0
        self.screen = screen
        self.name = name
        self.x_offset = x_off
        self.y_offset = y_off
        self.encounter_dist = 25
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.level = level
        self.evasion = evasion
        self.exp = exp
        self.coin = coin
        self.attack_skill = True    
        
        # For animating
        self.animation = []
        self.animation_steps = steps
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0
        self.size = size
        self.pixel = pixel

    def roll_evasion(self):
        return random.choices([False, True], [1-self.evasion,self.evasion])[0]

    # Show mob info and ready for start fight trigger
    # รอใส่ข้อมูลมอน
    def draw_monster(self):
        sprite_sheet_image = pg.image.load(Configs.monster(self.name)).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation):
                self.frame = 0
        for i in range(self.animation_steps):
            self.animation.append(sprite_sheet.get_monster((0, 0), i, self.pixel, self.pixel, self.size, Configs.get('BLACK')))
    
    def draw_mob_info(self, name):
        pg.draw.rect(self.screen, Configs.get('BLACK'), (250, 180, self.prep_size, self.prep_size), width=5, border_radius=10)
        pg.draw.rect(self.screen, Configs.get('CREAMY'), (255, 185, self.prep_size-10, self.prep_size-10))
        if self.prep_size != 300:
            self.prep_size += 50
        if self.prep_size == 300:
            text1 = self.font.render("Monster info: bla bla", True, Configs.get("BLACK"))
            text1_rect = text1.get_rect(center=(400, 300))

            text2 = self.font.render("Press SPACE to fight", True, Configs.get("BLACK"))
            text2_rect = text1.get_rect(center=(400, 350))

            self.screen.blit(text1, text1_rect)
            self.screen.blit(text2, text2_rect)

    def in_range(self, player, monster):
        distance = self.calculate_dist(player)
        if distance < self.encounter_dist:
            self.draw_mob_info(monster.name)
            # print("in range")
            return True
        else:
            self.prep_size = 0

    # Calculate dist player from mobs
    def calculate_dist(self, player):
        a = player.x - (self.x + self.x_offset)
        b = player.y - (self.y + self.y_offset)
        distance = math.hypot(a, b)
        return distance 

class Slime(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="SLIME", health=15, damage=1, level=1, evasion=0.1,
                 steps=6, size=1, pixel=128, exp=2, coin=2):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin) 
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee}
        self.attack_rate = 0.95
        self.run_rate = 0.05
        self.skill_chances = [self.attack_rate, self.run_rate]

class Goblin(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="GOBLIN", health=50, damage=5, level=2, evasion=0.1,
                 steps=3, size=1, pixel=300, exp=10, coin=5, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
           
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Dark_Goblin(Goblin):
    def __init__(self, screen, x_off, y_off, x, y, name="DARK", health=50, damage=2, level=2, evasion=0.3,
                 steps=3, size=3, pixel=64, exp=15, coin=20):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate = 0.5 # 0.1
        self.run_rate = 0 # 0.7
        self.hunter_instinct_rate = 0.5 #0.2
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]

class Vampire1(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE1", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Vampire2(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE2", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Vampire3(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE3", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Minotaur1(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR1", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Minotaur2(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR2", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Minotaur3(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR3", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Scorpion(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="SCORPION", health=200, damage=30, level=10, evasion=0.4,
                 steps=3, size=1, pixel=64, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Blue_worm(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="BLUE", health=200, damage=30, level=10, evasion=0.4,
                 steps=9, size=2, pixel=90, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)

class Purple_worm(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="PURPLE", health=200, damage=30, level=10, evasion=0.4,
                 steps=9, size=2, pixel=90, exp=100, coin=50, a=0, b=1):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.ui.draw_monster_attack,
                       'RUN': self.ui.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate =  0.7 #0.55
        self.run_rate = 0.05 # 0.05
        self.hunter_instinct_rate = 0.25 # 0.4
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]
        
    def hunter_instinct(self):
        self.attack_skill = False
        self.damage *= 1.5
        self.damage = round(self.damage)