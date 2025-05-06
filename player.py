from ui import AllUI
from config import Configs
from spritesheet import SpriteSheet
import pygame as pg
import random

class Player:
    def __init__(self, screen, name: str):
        self.ui = AllUI(screen)
        self.name = name
        self.health = 20
        self.max_health = 20
        self.level = 1
        self.exp = 0
        self.exp_threshold = 30
        self.coin = 0
        self.damage = 10
        self.evasion = 0.1
        self.skill1_status = False
        self.skill2_status = False

        self.x = 390
        self.y = 500
        self.speed = Configs.get('SPEED')

        # for storing animation
        self.animation_down = []
        self.animation_up = []
        self.animation_left = []
        self.animation_right = []

        # for animating
        self.size = 3
        self.animation_steps = 2
        self.last_up = pg.time.get_ticks()
        self.cool_down = 100
        self.frame = 0

        self.borders = {"HALL": self.check_lim_hall,
                       "PLAIN": self.check_lim_plain,
                       "SHOP": self.check_lim_shop}

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

    def die(self):
        pass

    def roll_evasion(self):
        return random.choices([False, True], [1-self.evasion,self.evasion])[0]

    def escape(self):
        pass

    def buy(self, item_name: str):
        pass

    def sell(self, item_name: str):
        pass

    def discard_item(self, item_name: str):
        pass

    def skill1(self):
        pass

    def skill2(self):
        pass

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
    
    def draw_idle_combat(self):
        sprite_sheet_image = pg.image.load(Configs.player_animation('LEFT')).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        return sprite_sheet.get_image2((0, 0), 0, 24, 24, self.size, Configs.get('MAGENTA'))
    
    def draw_walk_down(self):
        sprite_sheet_image = pg.image.load(Configs.player_animation('DOWN')).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation_down):
                self.frame = 0

        if len(self.animation_down) <= 0:
            for i in range(self.animation_steps):
                self.animation_down.append(sprite_sheet.get_image1((0, 0), i, 24, 24, self.size, Configs.get('MAGENTA')))
    
    def draw_walk_left(self):
        sprite_sheet_image = pg.image.load(Configs.player_animation('LEFT')).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        if len(self.animation_left) <= 0:
            for i in range(self.animation_steps):
                self.animation_left.append(sprite_sheet.get_image2((0, 0), i, 24, 24, self.size, Configs.get('MAGENTA')))

        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation_left):
                self.frame = 0

    def draw_walk_up(self):
        sprite_sheet_image = pg.image.load(Configs.player_animation('UP')).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        if len(self.animation_up) <= 0:
            for i in range(self.animation_steps):
                self.animation_up.append(sprite_sheet.get_image3((0, 0), i, 24, 24, self.size, Configs.get('MAGENTA')))

        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation_up):
                self.frame = 0

    def draw_walk_right(self):
        sprite_sheet_image = pg.image.load(Configs.player_animation('RIGHT')).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        if len(self.animation_right) <= 0:
            for i in range(self.animation_steps):
                self.animation_right.append(sprite_sheet.get_image4((0, 0), i, 24, 24, self.size, Configs.get('MAGENTA')))

        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation_right):
                self.frame = 0

    def draw_idle(self):
        sprite_sheet_image = pg.image.load(Configs.player_animation('IDLE')).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)
        
        return sprite_sheet.get_idle((0, 0), 0, 24, 24, self.size, Configs.get('MAGENTA'))
    