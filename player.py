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
        self.max_health = 500 
        self.health = self.max_health
        self.level = 1
        self.exp = 0
        self.exp_threshold = 30
        self.coin = 1000
        self.damage = 1000
        self.evasion = 0.2
        self.weapon = None
        self.skill1_status = False
        self.skill2_status = False
        self.skill3_status = False
        self.skill4_status = False
        self.attacks = {"ATTACK": self.draw_attack,
                        "RUN": self.draw_walk_out}

        # spawnpoint
        self.x = 366
        self.y = 460
        self.speed = Configs.get('SPEED')

        # for animating
        self.size = 3
        self.animation_steps = 2
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0
        self.pstate = "idle"
        self.p_pos = None
        
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

    def draw_enter_animation(self):
        if self.x != 540:
            self.x -= 10
            return True
        return False
    
    def draw_walk_out(self):
        if self.x > 0:
            self.x -= 10
            return False
        return True
    
    def draw_attack(self):
        print("attack")
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
        self.level = 1
        self.exp = 0
        self.exp_threshold = 30
        self.coin = 0
        self.damage = 10
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
            return True
        return False

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

    def draw_walk(self):
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
    
    def draw_idle(self):
        self.screen.blit(self.walk_animations[self.direction][0], (self.x, self.y)) 