from ui import AllUI
from config import Configs
from spritesheet import SpriteSheet
import pygame as pg
import random

class Player:
    def __init__(self, screen, name: str):
        self.screen = screen
        self.ui = AllUI(screen)
        self.name = name
        self.max_health = 1000
        self.health = self.max_health
        self.level = 100
        self.exp = 0
        self.exp_threshold = 30
        self.coin = 99999
        self.damage =7
        self.evasion = 0.2
        self.weapon = None
        self.skill1_unlock = False
        self.steal_count = 0
        self.skill2_unlock = False
        self.skill3_unlock = False
        self.skill4_unlock = False
        self.steal_chances = {"Potion": 0.6,
                             "Hi-Potion": 0.5,
                             "Loot bag": 0.5}
        self.attacks = {"ATTACK": self.draw_attack,
                        "RUN": self.draw_walk_out,
                        "DEFEND": self.defend}
        self.save_stats = {}
        self.tmp = None
        self.is_damage = False
        self.atk_tmp = 0
        self.already_boost = False

        self.run_lock = False
        self.all_lock = False   

        self.state = None

        # spawnpoint
        self.x = 366
        self.y = 460
        self.speed = Configs.get('SPEED')

        # for animating
        self.time_lock = False
        self.start = 0
        self.size = 3
        self.animation_steps = 2
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0
        self.frame2 = 0

        self.pstate = "idle"
        self.p_pos = None
        self.effects = []
        
        # for storing animation
        self.direction = "DOWN"
        self.walk_animations = {"LEFT": [],
                                "RIGHT": [],
                                "UP": [],
                                "DOWN": []}
        self.borders = {"HALL": self.check_lim_hall,
                       "PLAIN": self.check_lim_plain,
                       "SHOP": self.check_lim_shop,
                       "DESERT": self.check_lim_desert,
                       "SNOW": self.check_lim_snow,
                       "CAVE": self.check_lim_cave}
        self.create_walk()
        self.check_unlock_skill()

    def unlock(self):
        self.run_lock = False
        self.item_lock = False
        self.defend_lock = False
        self.skill1_lock = False
        self.skill2_lock = False
        self.skill3_lock = False
        self.skill4_lock = False

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
            # offsetx = Configs.effect_offset(self.name)[0]
            # offsety = Configs.effect_offset(self.name)[1]
            self.screen.blit(self.effects[self.frame2], 
                            (self.x-8, self.y+15))
            
        elif target is not None:
            x = Configs.effect_offset(eff)[0]
            y = Configs.effect_offset(eff)[1]
            self.screen.blit(self.effects[self.frame2], 
                            (x, y))
        return True
    
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
        if not self.draw_effects('P_INSTINCT', lim=150):
            self.already_boost = False
            return False
        return True
    
    def fire(self, mobs):
        self.create_fire()
        self.is_damage = True
        range = random.randint(0, round(self.level*2))
        dmg = self.damage + range
        self.atk_tmp = dmg
        if not self.draw_effects('P_FIRE', lim=50, target=mobs):
            return False
        return True

    def thunder(self, mobs):
        self.create_thunder()
        self.is_damage = True
        dmg = self.max_health*0.1
        self.atk_tmp = dmg
        if not self.draw_effects('P_THUNDER', lim=50, target=mobs):
            return False
        return True
    
    def defend(self, a):
        self.is_damage = False
        self.evasion = 1

    def save(self):
        self.save_stats["Evasion"] = self.evasion
        self.save_stats["Damage"] = self.damage
                           
    def return_stats(self, evade=False, damage=False):
        if damage and evade:
            if self.damage != self.save_stats["Damage"]:
                self.damage = self.save_stats["Damage"]
            if self.evasion != self.save_stats["Evasion"]:
                self.evasion = self.save_stats["Evasion"]
        elif evade:
            if self.evasion != self.save_stats["Evasion"]:
                self.evasion = self.save_stats["Evasion"]
    
    def draw_enter_animation(self):
        if self.x != 540:
            self.x -= 10
            return True
        return False
    
    def draw_walk_out(self, a=None):
        if self.x > 0:
            self.x -= 10
            return False
        return True
    
    def draw_attack(self, a=None):
        self.atk_tmp = self.damage
        self.is_damage = True
        if self.p_pos is None:
            self.p_pos = self.x
            self.pstate = "forward"

        if self.pstate == "forward":
            self.x -= 20
            if self.x <= 310:
                self.pstate = "backward"

        elif self.pstate == "backward":
            self.x += 20
            if self.x >= self.p_pos:
                self.x = self.p_pos
                self.pstate = "idle"
                self.p_pos = None
                return False
        return True
    
    def reset_stats(self):
        self.max_health = 20
        self.health = self.max_health
        self.level = 4
        self.exp = 29
        self.exp_threshold = 30
        self.coin = 0
        self.damage = 1000
        self.evasion = 0.2
        self.skill1_status = False
        self.skill2_status = False
        self.weapon = None

        self.x = 366
        self.y = 460

    def level_up(self):
        if self.exp >= self.exp_threshold:
            remain = self.exp - self.exp_threshold
            self.level += 1
            self.damage += 2
            self.exp_threshold += self.level*0.7
            self.exp = remain
            self.max_health += 5
            self.health = self.max_health
            self.check_unlock_skill()
            return True
        return False

    def steal(self, a=None):
        self.is_damage = False
        animating = self.draw_attack()
        if not animating:
            self.tmp = random.choices(list(self.steal_chances.keys()), list(self.steal_chances.values()))[0]
            return False
        return True

    def check_unlock_skill(self):
        if self.level >= 5:
            self.skill1_unlock = True
            self.attacks["STEAL"] = self.steal
        if self.level >= 10:
            self.skill2_unlock = True
            self.attacks["FIRE"] = self.fire
        if self.level >= 15:
            self.skill3_unlock = True
            self.attacks["THUNDER"] = self.thunder
        if self.level >= 20:
            self.skill4_unlock = True
            self.attacks["INSTINCT"] = self.hunter_instinct
        
    def roll_evasion(self):
        return random.choices([False, True], [1-self.evasion,self.evasion])[0]

    def check_lim_cave(self):
        if self.y < 300 or (self.x in range(0, 400) and self.y < 450) or (self.x in range(500, 800) and self.y < 425):
            self.speed = 0
            self.y += 1 
        elif self.x < 0 or (self.y in range(0, 450) and self.x < 410):
            self.speed = 0
            self.x += 1
        elif self.x > 750 or (self.y in range(0, 425) and self.x > 490):
            self.speed = 0
            self.x -= 1
        else:
            self.speed = Configs.get("SPEED")
    
    def check_lim_snow(self):
        # Bottom rock border
        if self.y > 525:
            self.speed = 0
            self.y -= 1

        # Left rock border
        elif (self.x < 330 and 50 <= self.y <= 180) or self.x < 0:
            self.speed = 0
            self.x += 1

        # Under Left/Right rock border
        elif (self.x < 330 and 185 <= self.y <= 188) or (self.x > 550 and 185 <= self.y <= 188):
            self.speed = 0
            self.y += 1

        # Right rock border
        elif (self.x > 550) and (50 <= self.y <= 180):
            self.speed = 0
            self.x -= 1
        else:
            self.speed = Configs.get('SPEED')

    def check_lim_desert(self):
        if self.y < 250:
            self.speed = 0
            self.y += 1
        elif self.y > 530:
            self.speed = 0
            self.y -= 1
        else:
            self.speed = Configs.get("SPEED")

    def check_lim_shop(self):
        # check top border
        if self.y < 400 or (self.x > 404 and self.y < 476) or (self.y < 475 and 40 <= self.x <= 151):
            self.speed = 0
            self.y += 1

        # check right borders
        elif (self.x > 400 and 400 <= self.y <= 470) or (self.x > 500 and 470 <= self.y <= 700):
            self.speed = 0
            self.x -= 1
        
        elif (self.x < 160 and 400 <= self.y <= 470) or self.x < 40:
            self.speed = 0
            self.x += 1
        
        else:
            self.speed = Configs.get("SPEED")

    def check_lim_plain(self):
        # Bottom rock border
        if self.y > 400:
            self.speed = 0
            self.y -= 1

        # Left rock border
        elif (self.x < 330) and (50 <= self.y <= 180):
            self.speed = 0
            self.x += 1

        # Under Left/Right rock border
        elif (self.x < 330 and 185 <= self.y <= 188) or (self.x > 550 and 185 <= self.y <= 188):
            self.speed = 0
            self.y += 1

        # Right rock border
        elif (self.x > 550) and (50 <= self.y <= 180):
            self.speed = 0
            self.x -= 1

        else:
            self.speed = Configs.get('SPEED')
    
    def check_lim_hall(self):
        # Door/Under pot border
        if (self.y < 460) or (self.x < 100 and 485 <= self.y <= 488):
            self.speed = 0
            self.y += 1
        
        # Left Screen border 
        elif self.x > 740:
            self.speed = 0
            self.x -= 1 

        # Pot/Right screen border
        elif (self.x < 100 and 460 <= self.y <= 480) or (self.x < 0):
            self.speed = 0
            self.x += 1       

        else:
            self.speed = Configs.get('SPEED')
    
    def create_walk(self):
        move = ["DOWN", "LEFT", "UP", "RIGHT"]
        for j in range(len(move)):
            sprite_sheet_image = pg.image.load(Configs.player_animation(move[j])).convert_alpha()
            sprite_sheet = SpriteSheet(sprite_sheet_image)
            if len(self.walk_animations[move[j]]) <= 0:
                if move[j] == "RIGHT":
                    for i in range(self.animation_steps):
                        self.walk_animations[move[j]].append(sprite_sheet.get_walk((0, 0), i, 24, 24, self.size, Configs.get('MAGENTA')))
                else:
                    for i in range(self.animation_steps):
                        self.walk_animations[move[j]].append(sprite_sheet.get_walk((0, 0), i, 24, 24, self.size, Configs.get('MAGENTA'), j))

    def draw_walk(self, direction=None):
        if direction is not None:
            self.screen.blit(self.walk_animations[direction][self.frame], (self.x, self.y))  
        else:
            current_time = pg.time.get_ticks()
            if current_time - self.last_up >= self.cool_down:
                self.frame += 1
                self.last_up = current_time
                if self.frame >= len(self.walk_animations[self.direction]):
                    self.frame = 0

            self.screen.blit(self.walk_animations[self.direction][self.frame], (self.x, self.y))  
        
    def draw_walk_in_combat(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.walk_animations["LEFT"]):
                self.frame = 0

        self.screen.blit(self.walk_animations["LEFT"][self.frame], (self.x, self.y)) 

    def draw_idle_in_combat(self):
        self.screen.blit(self.walk_animations["LEFT"][0], (self.x, self.y)) 
    
    def draw_idle(self, direction=None):
        if direction is not None:
            self.screen.blit(self.walk_animations[direction][0], (self.x, self.y)) 
        else:
            self.screen.blit(self.walk_animations[self.direction][0], (self.x, self.y)) 
