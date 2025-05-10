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
        self.mstate = "idle"

        # Mob's stats
        self.name = name
        self.level = level
        self.health = health
        self.damage = damage
        self.evasion = evasion
        self.exp = exp
        self.coin = coin
        self.state = None
        self.action_count = 0
        self.turn_count = 0

        # Skill rate
        self.attack_rate = 0
        self.run_rate = 0
        self.hunter_instinct_rate = 0
        self.crunch_rate = 0
        self.fire_rate = 0
        self.thunder_rate = 0
        self.gravity_rate = 0
        self.doom_rate = 0
        self.save_stats = {}

        # Check attack (could be made better)
        self.is_damage = False
        self.atk_tmp = 0
        self.bool_tmp = False
        self.already_boost = False
        self.already_save = False

        # Display info
        self.ui = AllUI(screen)
        self.font = pg.font.Font(None, 30)
        self.prep_size = 0
        self.text_offset = 25
        self.encounter_dist = 25
        
        # For animating
        self.animating = None
        self.effects = []
        self.animation = []
        self.animation_steps = steps
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.time_lock = False
        self.start = 0
        self.frame = 0
        self.frame2 = 0
        self.size = size
        self.pixel = pixel
        self.speed = 20
    
    # Drawing series
    def draw_monster_attack(self, player):
        self.atk_tmp = self.damage
        self.is_damage = True
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
    
    def draw_skill_attack(self, player, lim):
        self.atk_tmp = self.damage
        if self.m_pos is None:
            self.m_pos = self.x
            self.mstate = "forward"

        if self.mstate == "forward":
            self.x += self.speed
            if self.x >= player.x - 150:
                self.speed = 0
                self.bool_tmp = True
                self.animating = self.draw_skill_animation(lim)
                if not self.animating:
                    self.mstate = "backward"

        if self.mstate == "backward":
            self.bool_tmp = False
            self.speed = 20
            self.x -= self.speed
            if self.x <= self.m_pos:
                self.x = self.m_pos
                self.mstate = "idle"
                self.m_pos = None
                return False
        # print(self.x, self.y)
        return True

    def draw_skill_animation(self, lim):
        current_time = pg.time.get_ticks()
        if not self.time_lock:
            self.start = current_time
            self.time_lock = True
        if current_time - self.start >= lim:
            self.frame2 += 1
            self.time_lock = False
        if self.frame2 >= len(self.effects):
            self.frame2 = 0
            self.effects.clear()
            return False
        x = Configs.monster_combat(self.name)[0]
        y = Configs.monster_combat(self.name)[0]
        offsetx = Configs.effect_offset(self.name)[0]
        offsety = Configs.effect_offset(self.name)[1]
        self.screen.blit(self.effects[self.frame2], 
                        (x+offsetx, y+offsety))
        return True

    def draw_monster_flee(self, a):
        if self.x > -50:
            self.x -= 10
            return True
        return False
    
    def draw_effects(self, eff, lim, target=None):
        current_time = pg.time.get_ticks()
        if not self.time_lock:
            self.start = current_time
            self.time_lock = True
        if current_time - self.start >= lim:
            self.frame2 += 1
            self.time_lock = False
        if self.frame2 >= len(self.effects):
            self.frame2 = 0
            self.effects.clear()
            return False
        
        if target is None:
            offsetx = Configs.effect_offset(self.name)[0]
            offsety = Configs.effect_offset(self.name)[1]
            self.screen.blit(self.effects[self.frame2], 
                            (self.x+offsetx, self.y+offsety))
            
        elif target is not None:
            offsetx = Configs.effect_offset(eff)[0]
            offsety = Configs.effect_offset(eff)[1]
            self.screen.blit(self.effects[self.frame2], 
                            (target.x+offsetx, target.y+offsety))
        return True
    
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
            self.animation.append(sprite_sheet.get_monster((0, 0), i, self.pixel, self.pixel, self.size, Configs.get('TRANSPARENT')))
    
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

    # Create skill series
    def create_aura(self):
        sprite_sheet_image = pg.image.load(Configs.effects("AURA")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for _ in range(2):
                for i in range(5):
                    self.effects.append(sprite_sheet.get_effects((0, 0), i, 30, 30, 3, Configs.get('BLACK')))

    def create_fire(self):
        sprite_sheet_image = pg.image.load(Configs.effects("FIRE")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for j in range(4):
                for i in range(4):
                    self.effects.append(sprite_sheet.get_effects((0, 0), i, 96, 96, 2, Configs.get('BLACK'), j))

    def create_thunder(self):
        sprite_sheet_image = pg.image.load(Configs.effects("THUNDER")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for i in range(10):
                self.effects.append(sprite_sheet.get_effects((0, 0), i, 64, 128, 2.5, Configs.get('BLACK')))

    def create_gravity(self):
        sprite_sheet_image = pg.image.load(Configs.effects("GRAVITY")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for j in range(5):
                for i in range(4):
                    self.effects.append(sprite_sheet.get_effects((0, 0), i, 96, 80, 2, Configs.get('BLACK'), j))

    def create_doom(self):
        sprite_sheet_image = pg.image.load(Configs.effects("DOOM")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for j in range(4):
                for i in range(4):
                    self.effects.append(sprite_sheet.get_effects((0, 0), i, 144, 144, 2, Configs.get('BLACK'), j))

    def create_crunch(self):
        sprite_sheet_image1 = pg.image.load(Configs.effects(self.name)).convert_alpha()
        sprite_sheet1 = SpriteSheet(sprite_sheet_image1)
        sprite_sheet_image2 = pg.image.load(Configs.monster(self.name)).convert_alpha()
        sprite_sheet2 = SpriteSheet(sprite_sheet_image2)

        if len(self.effects) <= 0:
            for i in range(16):
                self.effects.append(sprite_sheet1.get_effects((0, 0), i, 90, 90, 2, Configs.get('BLACK')))
            for i in range(3):
                self.effects.append(sprite_sheet2.get_effects((0, 0), i, 90, 90, 2, Configs.get('BLACK')))

    def create_haste(self):
        pass

    def create_slash(self):
        sprite_sheet_image1 = pg.image.load(Configs.effects(self.name)).convert_alpha()
        sprite_sheet1 = SpriteSheet(sprite_sheet_image1)
        sprite_sheet_image2 = pg.image.load(Configs.monster(self.name)).convert_alpha()
        sprite_sheet2 = SpriteSheet(sprite_sheet_image2)

        if len(self.effects) <= 0:
            for i in range(5):
                self.effects.append(sprite_sheet1.get_effects((0, 0), i, 128, 128, 1, Configs.get('BLACK')))
            for i in range(3):
                self.effects.append(sprite_sheet2.get_effects((0, 0), i, 128, 128, 1, Configs.get('BLACK')))

    def create_evil(self):
        sprite_sheet_image = pg.image.load(Configs.effects("EVIL")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for j in range(5):
                for i in range(6):
                    self.effects.append(sprite_sheet.get_effects((0, 0), i, 256, 256, 1, Configs.get('BLACK'), j))

    # Skill series          
    def hunter_instinct(self, a):
        self.create_aura()
        self.ui.draw_skill_display(f"{self.name}'s damage increased by 1.5x!")
        dmg = 0
        self.is_damage = False
        if not self.already_boost:
            self.damage *= 1.5
            self.damage = round(self.damage)
            self.already_boost = True
        self.atk_tmp = dmg
        if not self.draw_effects('AURA', lim=150):
            self.effects.clear()
            self.already_boost = False
            return False
        return True
            
    def fire(self, player):
        self.create_fire()
        self.is_damage = True
        dmg = player.max_health*0.1
        self.atk_tmp = dmg
        if not self.draw_effects('FIRE', lim=50, target=player):
            self.effects.clear()
            return False
        return True

    def thunder(self, player):
        self.create_thunder()
        self.is_damage = True
        dmg = player.max_health*0.1
        self.atk_tmp = dmg
        if not self.draw_effects('THUNDER', lim=50, target=player):
            self.effects.clear()
            return False
        return True

    def gravity(self, player):
        self.create_gravity()
        self.is_damage = True
        dmg = player.coin*0.3
        self.atk_tmp = dmg
        if not self.draw_effects(eff='GRAVITY', lim=50, target=player):
            self.effects.clear()
            return False
        return True
    
    def doom(self, player):
        self.create_doom()
        self.is_damage = True
        dmg = player.health - 1
        self.atk_tmp = dmg
        if not self.draw_effects(eff='DOOM', lim=25, target=player):
            self.effects.clear()
            return False
        return True
    
    def crunch(self, player):
        self.create_crunch()
        self.is_damage = True
        dmg = self.damage//(self.health/10)
        self.atk_tmp = dmg
        if not self.draw_skill_attack(player, lim=50):
            self.effects.clear()
            return False
        return True
    
    def haste(self, a):
        if not self.already_save:
            self.save(haste=True)
            self.already_save = True
        self.is_damage = False
        dmg = 0
        self.atk_tmp = dmg
        self.state = 'HASTE'
        self.skill_chances['HASTE'] = 0

        if not self.draw_effects(eff='HASTE', lim=50):
            self.effects.clear()
            return False
        return True
    
    def evil_sword(self, player):
        self.create_evil()
        if not player.run_lock:
            print("lock")
            player.run_lock = True

        self.is_damage = False
        dmg = 0
        self.atk_tmp = dmg
        self.skill_chances['EVIL SWORD'] = 0
        if not self.draw_effects(eff='EVIL', lim=0, target=player):
            self.effects.clear()
            return False
        return True
    
    def slash(self, player):
        self.create_slash()
        self.is_damage = True
        dmg = self.damage//(self.health/10)
        self.atk_tmp = dmg
        if not self.draw_skill_attack(player, lim=50):
            self.effects.clear()
            return False
        return True
    
    # Etc series
    def roll_evasion(self):
        return random.choices([False, True], [1-self.evasion,self.evasion])[0]

    def in_range(self, player):
        distance = self.calculate_dist(player)
        if distance < self.encounter_dist:
            self.draw_mob_info()
            return True
        else:
            self.prep_size = 0

    # Calculate dist player from mobs
    def calculate_dist(self, player):
        a = player.x - (self.x + self.x_offset)
        b = player.y - (self.y + self.y_offset)
        distance = math.hypot(a, b)
        return distance 

    def save(self, haste=False, evil=False):
        self.save_stats['State'] = None
        if haste:
            self.save_stats['Haste_rate'] = self.skill_chances['HASTE']
        if evil:
            self.save_stats['Evil_rate'] = self.skill_chances['EVIL SWORD']
        self.save_stats['Chances'] = self.skill_chances    

    def return_stats(self, haste=False, evil=False):
        self.state = self.save_stats['State']
        if haste:
            self.skill_chances['HASTE'] = self.save_stats['Haste_rate']
        if evil:
            self.skill_chances['EVIL SWORD'] = self.save_stats['Evil_rate']
        self.skill_chances = self.save_stats['Chances']
        self.already_save = False

class Slime(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="SLIME", health=8, damage=1, level=1, evasion=0.1,
                 steps=6, size=1, pixel=128, exp=2, coin=2):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin) 
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}
        
        self.skill_chances = {'ATTACK': 0.1,
                            'RUN': 0}

class Goblin(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="GOBLIN", health=20, damage=7, level=2, evasion=0.1,
                 steps=3, size=1, pixel=300, exp=10, coin=5):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'INSTINCT': self.hunter_instinct}
        self.skill_chances = {'ATTACK': 0.1,
                            'RUN': 0,
                            'INSTINCT': 0.9}
        
class Dark_Goblin(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="DARK", health=30, damage=2, level=3, evasion=0.3,
                 steps=3, size=3, pixel=64, exp=15, coin=8):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'INSTINCT': self.hunter_instinct}

        self.skill_chances = {'ATTACK': 0.1,
                            'RUN': 0,
                            'INSTINCT': 0.9}
    
    def hunter_instinct(self, a):
        self.create_aura()
        self.ui.draw_skill_display(f"{self.name}'s damage increased by 1.5x!")
        dmg = 0
        self.is_damage = False
        if not self.already_boost:
            self.damage *= 2
            self.damage = round(self.damage)
            self.already_boost = True
        # print(self.damage)
        self.atk_tmp = dmg
        if not self.draw_effects('AURA', lim=150):
            self.effects.clear()
            self.already_boost = False
            return False
        return True

class Scorpion(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="SCORPION", health=55, damage=10, level=4, evasion=0.1,
                 steps=3, size=1, pixel=64, exp=25, coin=15):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee}

        self.skill_chances = {'ATTACK': 0.9,
                            'RUN': 0.1
                            }   

class Blue_worm(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="BLUE", health=70, damage=8, level=5, evasion=0.3,
                 steps=9, size=2, pixel=90, exp=30, coin=15):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'FIRE': self.fire,
                       'CRUNCH': self.crunch
                       }

        self.skill_chances = {'ATTACK': 0,
                            'RUN': 0,
                            'FIRE': 0.5,
                            'CRUNCH': 0.5}
    
    def fire(self, player):
        self.create_fire()
        self.is_damage = True
        dmg = player.max_health*0.2
        self.atk_tmp = dmg
        if not self.draw_effects('FIRE', lim=50, target=player):
            self.effects.clear()
            return False
        return True

class Purple_worm(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="PURPLE", health=70, damage=8, level=5, evasion=0.4,
                 steps=9, size=2, pixel=90, exp=30, coin=10):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'THUNDER': self.thunder,
                       'CRUNCH': self.crunch
                       }
        
        self.skill_chances = {'ATTACK': 0,
                            'RUN': 0,
                            'THUNDER': 0.5,
                            'CRUNCH': 0.5}

class Minotaur1(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR1", health=100, damage=10, level=8, evasion=0.2,
                 steps=5, size=1, pixel=128, exp=50, coin=25):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'GRAVITY': self.gravity,
                       'SLASH': self.slash,
                       'EVIL SWORD': self.evil_sword}
    
        self.skill_chances = {'ATTACK': 0.5,
                            'RUN': 0,
                            'GRAVITY': 0,
                            'SLASH': 0.5,
                            'EVIL SWORD': 1}
    
class Minotaur2(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR2", health=200, damage=15, level=8, evasion=0.2,
                 steps=5, size=1, pixel=128, exp=30, coin=10):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'SLASH': self.slash,
                       'HASTE': self.haste,
                       'EVIL SWORD': self.evil_sword}
        
        self.skill_chances = {'ATTACK': 0.1,
                            'RUN': 0,
                            'SLASH': 0.4,
                            'HASTE': 0.9,
                            'EVIL SWORD': 1}

class Minotaur3(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="MINOTAUR3", health=100, damage=10, level=8, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=25, coin=20):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'GRAVITY': self.gravity,
                       'FIRE': self.fire,
                       'THUNDER': self.thunder,
                       'EVIL SWORD': self.evil_sword}
        
        self.skill_chances = {'ATTACK': 0,
                            'RUN': 0,
                            'GRAVITY': 0.4,
                            'FIRE': 0.3,
                            'THUNDER': 0.3,
                            'EVIL SWORD': 1}

class Vampire1(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE1", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       'DOOM': self.doom,
                       'FIRE': self.fire,
                       'CRUNCH': self.crunch}
        
        self.skill_chances = {'ATTACK': 0,
                            'RUN': 0,
                            'DOOM': 0,
                            'FIRE': 1,
                            'CRUNCH': 0}
    
    def create_crunch(self):
        sprite_sheet_image1 = pg.image.load(Configs.effects(self.name)).convert_alpha()
        sprite_sheet1 = SpriteSheet(sprite_sheet_image1)
        sprite_sheet_image2 = pg.image.load(Configs.monster(self.name)).convert_alpha()
        sprite_sheet2 = SpriteSheet(sprite_sheet_image2)

        if len(self.effects) <= 0:
            for i in range(3):
                self.effects.append(sprite_sheet2.get_effects((0, 0), i, 128, 128, 1, Configs.get('TRANSPARENT')))
            for i in range(5):
                self.effects.append(sprite_sheet1.get_effects((0, 0), i, 128, 128, 1, Configs.get('TRANSPARENT')))
            for i in range(3):
                self.effects.append(sprite_sheet2.get_effects((0, 0), i, 128, 128, 1, Configs.get('TRANSPARENT')))
    
    def crunch(self, player):
        self.create_crunch()
        self.is_damage = True
        dmg = self.damage//(self.health/10)
        self.atk_tmp = dmg
        if not self.draw_skill_attack(player, lim=75):
            self.effects.clear()
            return False
        return True

class Vampire2(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE2", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       "DOOM": self.doom,
                       "THUNDER":self.thunder,
                       'HASTE': self.haste}
        
        self.skill_chances = {'ATTACK': 0.2,
                            'RUN': 0,
                            'DOOM': 0,
                            'THUNDER': 0.2,
                            'HASTE': 0.8
                            }     

class Vampire3(Monster_TMP):
    def __init__(self, screen, x_off, y_off, x, y, name="VAMPIRE3", health=200, damage=30, level=10, evasion=0.4,
                 steps=5, size=1, pixel=128, exp=100, coin=50):
        super().__init__(screen, x_off, y_off, x, y, name, health, damage, level, evasion, steps, size, pixel, exp, coin)
        self.skill = {'ATTACK': self.draw_monster_attack,
                       'RUN': self.draw_monster_flee,
                       "DOOM": self.doom}
        
        self.skill_chances = {'ATTACK': 0,
                            'RUN': 0,
                            'DOOM': 0,
                            }
