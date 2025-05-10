from ui import AllUI
from config import Configs
from spritesheet import SpriteSheet
import item
import pygame as pg
import random

class Player:
    def __init__(self, screen, name: str):
        self.screen = screen
        self.ui = AllUI(screen)
        self.name = name

        # Base stats
        # self.max_health = 20
        # self.health = self.max_health
        # self.level = 1
        # self.exp = 0
        # self.exp_threshold = 5
        # self.coin = 10
        # self.damage = 7
        # self.evasion = 0.2
        # self.weapon = None
        # self.dmg_up = 3
        # self.health_up = 5

        self.max_health = 2000
        self.health = self.max_health
        self.level = 100
        self.exp = 0
        self.exp_threshold = 500
        self.coin = 1000
        self.damage = 100
        self.evasion = 0.2
        self.weapon = None
        self.dmg_up = 3
        self.health_up = 5
        
        # Steal skill
        self.skill1_unlock = False
        self.steal_count = 0
        # Steal chances 
        self.steal_chances = {"Potion": 0, #0.5
                             "Hi-Potion": 0.2, #0.2
                             "Bag of greed": 0} # 0.3
        # Fire (% damage)
        self.skill2_unlock = False
        # Thunder (% damage)
        self.skill3_unlock = False
        # Instinct (increase % damage)
        self.skill4_unlock = False

        # Lock skills from some mob's skill
        self.run_lock = False
        self.all_lock = False  

        # Player's starter skill set
        self.attacks = {"ATTACK": self.attack,
                        "RUN": self.run,
                        "DEFEND": self.defend,
                        "HEAL": self.heal,
                        "MISC": self.misc}
        
        self.miscs = {"Battle drum": self.drum,
                      "Bag of greed": self.greed,
                      "Bomb": self.bomb}
        
        self.save_stats = {}
        self.is_damage = False
        self.is_heal = True
        self.already_boost = False
        self.count_level_up = 0

        # for exchanging
        self.tmp = None
        self.atk_tmp = 0
        self.double = False

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
        
        # for storing walking animation
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

        self.items = {'Potion': item.Potion(),
                      'Hi-Potion': item.Hi_Potion(),
                      "X-Potion": item.X_Potion(),
                      "Battle drum": item.Battle_drum(),
                      "Bag of greed": item.Greed_bag(),
                      "Bomb": item.Bomb()}

    """
    :Status series:

    All these functions are assocciated with player's stats. Some are used to increase or save stats
    """
    def check_unlock_skill(self):
        # Quick unlock change all == to >=
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
    
    def check_health(self):
        if self.health > self.max_health:
            self.health = self.max_health

    """
    Save some stats that is meant to be reversed at the end of battle 
    Ex. Intinct boosts damage. Damage has to be reversed back to its original value before the start of the combat 
    """
    def save(self, level=None):
        self.save_stats["Damage"] = self.damage
        self.save_stats["Evasion"] = self.evasion
                   
    def return_stats(self, evade=False, damage=False):
        if damage and evade:
            if self.damage != self.save_stats["Damage"]:
                self.damage = self.save_stats["Damage"]
            if self.evasion != self.save_stats["Evasion"]:
                self.evasion = self.save_stats["Evasion"]
        elif evade:
            if self.evasion != self.save_stats["Evasion"]:
                self.evasion = self.save_stats["Evasion"]
    
    """
    Reset stats back to when the game started
    """
    def half_stats(self):
        self.health = self.max_health // 2
        self.coin = self.coin // 2
        self.x = 366
        self.y = 460

    """
    In some battle, player's skill will be locked. this function purpose is to unlock those skills that have been locked
    """
    def unlock(self):
        self.run_lock = False
        self.all_lock = False   

    """
    Increase player's leve/stats and increase exp threshold
    """
    def level_up(self):
        print(self.count_level_up)
        if self.exp >= self.exp_threshold:
            remain = self.exp - self.exp_threshold
            self.level += 1
            self.exp_threshold += self.level*1.5
            self.exp = remain       
            self.count_level_up += 1
            self.check_unlock_skill()
            if self.exp >= self.exp_threshold:
                self.level_up()
            return True
        return False

    def up_stats(self):
        self.damage += self.dmg_up*self.count_level_up
        self.health += self.health_up*self.count_level_up
        self.health = self.max_health
        self.count_level_up = 0

    def roll_evasion(self):
        return random.choices([False, True], [1-self.evasion,self.evasion])[0]
    
    """
    :Create series:

    Create animations for further skills to be used
    """
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
    
    def create_heal(self):
        sprite_sheet_image = pg.image.load(Configs.effects("HEAL")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for j in range(4):
                for i in range(4):
                    self.effects.append(sprite_sheet.get_effects2((0, 0), i, 128, 128, 3, Configs.get('BLACK'), j))

    def create_greed(self):
        sprite_sheet_image = pg.image.load(Configs.effects("GREED")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for i in range(18):
                self.effects.append(sprite_sheet.get_effects((0, 0), i, 64, 64, 2, Configs.get('BLACK'), 2))

    def create_bomb(self):
        sprite_sheet_image = pg.image.load(Configs.effects("BOMB")).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        if len(self.effects) <= 0:
            for i in range(12):
                self.effects.append(sprite_sheet.get_effects((0, 0), i, 128, 128, 2.5, Configs.get('BLACK')))

    """
    :Skill series:

    Skill functions for player with their unique skill calculation and ability
    """
    # Control how player moves by using player_state(p_state)
    def attack(self, mobs=None, index=None):
        self.atk_tmp = self.damage
        self.is_heal = False
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
    
    def run(self, mobs=None, index=None):
        self.is_heal = False
        if self.x > 0:
            self.x -= 10
            return False
        return True
    
    def defend(self, mobs=None, index=None):
        self.is_heal = False
        self.is_damage = False
        self.evasion = 1

    # Requires unlock
    def steal(self, mobs=None, index=None):
        self.is_damage = False
        self.is_heal = False
        animating = self.attack()
        if not animating:
            self.tmp = random.choices(list(self.steal_chances.keys()), list(self.steal_chances.values()))[0]
            return False
        return True
    
    def heal(self, mobs=None, index=None):
        self.create_heal()
        dmg = list(self.items.values())[index].heal
        self.is_damage = False
        self.is_heal = True
        if not self.already_boost:
            self.damage *= 1.5
            self.damage = round(self.damage)
            self.already_boost = True
        self.atk_tmp = dmg
        if not self.draw_effects('HEAL', lim=50):
            self.already_boost = False
            return False
        return True 
    
    def misc(self, mobs=None, index=None):
        misc_name = list(self.items.keys())[index]
        done = self.miscs[misc_name](mobs)
        if done:
            return True
        return False 
    
    def drum(self, mobs=None):
        self.create_aura()
        self.ui.draw_skill_display(f"{self.name}'s damage increased by 2x!")
        dmg = 0
        self.is_heal = False
        self.is_damage = False
        if not self.already_boost:
            self.damage *= 2
            self.damage = round(self.damage)
            self.already_boost = True
        self.atk_tmp = dmg
        if not self.draw_effects('P_INSTINCT', lim=150):
            self.already_boost = False
            return False
        return True 

    def greed(self, mobs=None):
        self.create_greed()
        self.ui.draw_skill_display("Mob drops are now x2!")
        dmg = 0
        self.is_heal = False
        self.is_damage = False
        self.double = True
        self.atk_tmp = dmg
        if not self.draw_effects('GREED', lim=50, target=mobs):
            return False
        return True 

    def bomb(self, mobs=None):
        self.create_bomb()
        dmg = 50
        self.is_heal = False
        self.is_damage = True
        self.atk_tmp = dmg
        if not self.draw_effects('BOMB', lim=50, target=mobs):
            return False
        return True 

    """
    All player's skills with their own damage calculation system
    """
    def fire(self, mobs=None, index=None):
        self.create_fire()
        self.is_heal = False
        self.is_damage = True
        range = random.randint(10, round(self.level)*3)
        dmg = range
        self.atk_tmp = dmg
        if not self.draw_effects('P_FIRE', lim=50, target=mobs):
            return False
        return True

    def thunder(self, mobs=None, index=None):
        self.create_thunder()
        self.is_heal = False
        self.is_damage = True
        dmg = self.damage//(self.health/20)
        self.atk_tmp = dmg
        if not self.draw_effects('P_THUNDER', lim=50, target=mobs):
            return False
        return True
    
    def hunter_instinct(self, mobs=None, index=None):
        self.create_aura()
        self.ui.draw_skill_display(f"{self.name}'s damage increased by 1.5x!")
        dmg = 0
        self.is_heal = False
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

    """
    :Border series:

    Unfortunately, cannot come up with a better idea to detect map's border so if else are to be implemented here.
    These functions are used to limit player walking capability for each map.
    """
    def check_lim_cave(self):
        # upper border
        if self.y < 300 or (self.x in range(0, 400) and self.y < 450) or (self.x in range(500, 800) and self.y < 425):
            self.speed = 0
            self.y += 1 
        # left border
        elif self.x < 0 or (self.y in range(0, 450) and self.x < 410):
            self.speed = 0
            self.x += 1
        # right border
        elif self.x > 750 or (self.y in range(0, 425) and self.x > 490):
            self.speed = 0
            self.x -= 1
        else:
            self.speed = Configs.get("SPEED")
    
    def check_lim_snow(self):
        # bottom border
        if self.y > 525:
            self.speed = 0
            self.y -= 1

        # left border
        elif (self.x < 330 and 50 <= self.y <= 180) or self.x < 0:
            self.speed = 0
            self.x += 1

        # upper border
        elif (self.x < 330 and 185 <= self.y <= 188) or (self.x > 550 and 185 <= self.y <= 188):
            self.speed = 0
            self.y += 1

        # right border
        elif (self.x > 550) and (50 <= self.y <= 180):
            self.speed = 0
            self.x -= 1
        else:
            self.speed = Configs.get('SPEED')

    def check_lim_desert(self):
        # upper border
        if self.y < 250:
            self.speed = 0
            self.y += 1
        # bottom border
        elif self.y > 530:
            self.speed = 0
            self.y -= 1
        else:
            self.speed = Configs.get("SPEED")

    def check_lim_shop(self):
        # upper border
        if self.y < 400 or (self.x > 404 and self.y < 476) or (self.y < 475 and 40 <= self.x <= 151):
            self.speed = 0
            self.y += 1
        #  right border
        elif (self.x > 400 and 400 <= self.y <= 470) or (self.x > 500 and 470 <= self.y <= 700):
            self.speed = 0
            self.x -= 1
        # left border
        elif (self.x < 160 and 400 <= self.y <= 470) or self.x < 40:
            self.speed = 0
            self.x += 1
        else:
            self.speed = Configs.get("SPEED")

    def check_lim_plain(self):
        # bottom border
        if self.y > 400:
            self.speed = 0
            self.y -= 1
        # left border
        elif (self.x < 330) and (50 <= self.y <= 180):
            self.speed = 0
            self.x += 1
        # upper border
        elif (self.x < 330 and 185 <= self.y <= 188) or (self.x > 550 and 185 <= self.y <= 188):
            self.speed = 0
            self.y += 1
        # right border
        elif (self.x > 550) and (50 <= self.y <= 180):
            self.speed = 0
            self.x -= 1
        else:
            self.speed = Configs.get('SPEED')
    
    def check_lim_hall(self):
        # upper border
        if (self.y < 460) or (self.x < 100 and 485 <= self.y <= 488):
            self.speed = 0
            self.y += 1
        # left border 
        elif self.x > 740:
            self.speed = 0
            self.x -= 1 
        # right border
        elif (self.x < 100 and 460 <= self.y <= 480) or (self.x < 0):
            self.speed = 0
            self.x += 1       
        else:
            self.speed = Configs.get('SPEED')
    
    """
    :Drawing series:

    Functions for animating player in different circumstances. Mostly in combat area
    """
    # Combat
    def draw_idle_in_combat(self):
        self.screen.blit(self.walk_animations["LEFT"][0], (self.x, self.y)) 

    def draw_enter_animation(self):
        if self.x != 540:
            self.x -= 10
            return True
        return False
    
    def draw_walk_in_combat(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.walk_animations["LEFT"]):
                self.frame = 0
        self.screen.blit(self.walk_animations["LEFT"][self.frame], (self.x, self.y)) 

        # For animating every spritesheet skill effects
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
            self.time_lock = False
            return False
        
        if target is None:
            x = Configs.effect_offset(eff)[0]
            y = Configs.effect_offset(eff)[1]
            self.screen.blit(self.effects[self.frame2], 
                            (self.x+x, self.y+y))
            
        elif target is not None:
            x = Configs.effect_offset(eff)[0]
            y = Configs.effect_offset(eff)[1]
            self.screen.blit(self.effects[self.frame2], 
                            (x, y))
        return True
    
    # Non-combat drawing functions
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
    
    def draw_idle(self, direction=None):
        if direction is not None:
            self.screen.blit(self.walk_animations[direction][0], (self.x, self.y)) 
        else:
            self.screen.blit(self.walk_animations[self.direction][0], (self.x, self.y)) 
