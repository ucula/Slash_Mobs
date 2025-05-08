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
        
        self.screen = screen
        # Mob's coords in every scenarios ex. combat, normal
        self.x = x
        self.y = y
        self.x_offset = x_off
        self.y_offset = y_off
        self.m_pos = None
        self.mstate = "forward"

        # Mob's stats
        self.name = name
        self.level = level
        self.health = health
        self.damage = damage
        self.evasion = evasion
        self.exp = exp
        self.coin = coin

        # Check attack (could be made better)
        self.attack_skill = True  

        # Display info
        self.ui = AllUI(screen)
        self.font = pg.font.Font(None, 30)
        self.prep_size = 0
        self.text_offset = 25
        self.encounter_dist = 25
        
        # For animating
        self.animation = []
        self.animation_steps = steps
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0
        self.size = size
        self.pixel = pixel
        self.speed = 20

    # Done
    def draw_monster_attack(self, player):
        if self.m_pos is None:
            self.m_pos = self.x
            self.mstate = "forward"

        if self.mstate == "forward":
            self.x += self.speed
            if self.x >= player.x - 150:
                self.mstate = "backward"

        elif self.mstate == "backward":
            self.x -= self.speed
            if self.x <= self.m_pos:
                self.x = self.m_pos
                self.mstate = "idle"
                self.m_pos = None
                return False
        return True
    
    # Done
    def draw_monster_flee(self, a):
        if self.x > -50:
            self.x -= 10
            return True
        return False
    
    def roll_evasion(self):
        return random.choices([False, True], [1-self.evasion,self.evasion])[0]

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
    
    def draw_mob_info(self):
        pg.draw.rect(self.screen, Configs.get('BLACK'), (250, 180, self.prep_size, self.prep_size), width=5, border_radius=10)
        pg.draw.rect(self.screen, Configs.get('CREAMY'), (255, 185, self.prep_size-10, self.prep_size-10))
        if self.prep_size != 300:
            self.prep_size += 50
        if self.prep_size == 300:
            name = self.font.render(f"Name: {self.name}", True, Configs.get("BLACK"))
            name_rect = name.get_rect(topleft=(270, 200))

            lvl = self.font.render(f"Level: {self.level}", True, Configs.get("BLACK"))
            lvl_rect = lvl.get_rect(topleft=(270, 200+(1*self.text_offset)))

            health = self.font.render(f"Health: {self.health}", True, Configs.get("BLACK"))
            health_rect = health.get_rect(topleft=(270, 200+(2*self.text_offset)))

            dmg = self.font.render(f"Damage: {self.damage}", True, Configs.get("BLACK"))
            dmg_rect = dmg.get_rect(topleft=(270, 200+(3*self.text_offset)))

            eva = self.font.render(f"Evasion: {self.evasion*100}%", True, Configs.get("BLACK"))
            eva_rect = eva.get_rect(topleft=(270, 200+(4*self.text_offset)))

            exp = self.font.render(f"Exp drop: {self.exp}", True, Configs.get("BLACK"))
            exp_rect = exp.get_rect(topleft=(270, 200+(5*self.text_offset)))

            coin = self.font.render(f"Coin drop: {self.coin}", True, Configs.get("BLACK"))
            coin_rect = coin.get_rect(topleft=(270, 200+(6*self.text_offset)))

            help = self.font.render("Press \"SPACE\" to fight", True, Configs.get("BLACK"))
            help_rect = help.get_rect(topleft=(270, 200+(7*self.text_offset)))

            self.screen.blit(name, name_rect)
            self.screen.blit(lvl, lvl_rect)
            self.screen.blit(health, health_rect)
            self.screen.blit(dmg, dmg_rect)
            self.screen.blit(eva, eva_rect)
            self.screen.blit(exp, exp_rect)
            self.screen.blit(coin, coin_rect)
            self.screen.blit(help, help_rect)

    def in_range(self, player, monster):
        distance = self.calculate_dist(player)
        if distance < self.encounter_dist:
            self.draw_mob_info()
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
    def __init__(self, screen, x_off, y_off, x, y, name="SLIME", health=8, damage=1, level=1, evasion=0.1,
                 steps=6, size=1, pixel=128, exp=2, coin=2):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin) 
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate = 0.95
        self.run_rate = 0.05
        self.skill_chances = [self.attack_rate, self.run_rate]

class Goblin(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="GOBLIN", health=20, damage=7, level=2, evasion=0.1,
                 steps=3, size=1, pixel=300, exp=10, coin=5):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
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
    def __init__(self, screen, x_off, y_off, x, y, name="DARK", health=30, damage=2, level=2, evasion=0.3,
                 steps=3, size=3, pixel=64, exp=15, coin=8):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'INSTINCT': self.ui.draw_instinct}
        self.attack_rate = 0.4 # 0.1
        self.run_rate = 0 # 0.7
        self.hunter_instinct_rate = 0.6 #0.2
        self.skill_chances = [self.attack_rate, self.run_rate, self.hunter_instinct_rate]

class Scorpion(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="SCORPION", health=55, damage=10, level=4, evasion=0.3,
                 steps=3, size=1, pixel=64, exp=25, coin=15):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate =  0.9 #0.55
        self.run_rate = 0.1 # 0.05
        self.skill_chances = [self.attack_rate, self.run_rate]

class Blue_worm(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="BLUE", health=200, damage=8, level=5, evasion=0.4,
                 steps=9, size=2, pixel=90, exp=30, coin=15):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'CRUNCH': self.draw_crunch,
                       'FIRE': self.draw_fire}
        self.attack_rate =  0.7 
        self.run_rate = 0.05 
        self.crunch_rate = 0
        self.fire_rate = 0
        self.skill_chances = [self.attack_rate, self.run_rate]
    
    def draw_crunch(self):
        pass

    def draw_fire(self):
        pass

class Purple_worm(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="PURPLE", health=200, damage=50, level=5, evasion=0.2,
                 steps=9, size=2, pixel=90, exp=30, coin=10):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate =  0.7 
        self.run_rate = 0.05 
        self.skill_chances = [self.attack_rate, self.run_rate]


class Vampire1(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE1", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate =  0.7 
        self.run_rate = 0.05 
        self.skill_chances = [self.attack_rate, self.run_rate]

class Vampire2(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE2", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate =  0.7
        self.run_rate = 0.05 
        self.skill_chances = [self.attack_rate, self.run_rate]

class Vampire3(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE3", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate =  0.7 
        self.run_rate = 0.05 
        self.skill_chances = [self.attack_rate, self.run_rate]

class Minotaur1(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR1", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate =  0.7 
        self.run_rate = 0.05 
        self.skill_chances = [self.attack_rate, self.run_rate]

class Minotaur2(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR2", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate =  0.7 
        self.run_rate = 0.05 
        self.skill_chances = [self.attack_rate, self.run_rate]

class Minotaur3(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR3", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        self.attack_rate =  0.7 
        self.run_rate = 0.05 
        self.skill_chances = [self.attack_rate, self.run_rate]
