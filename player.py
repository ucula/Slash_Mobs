from ui import AllUI
from config import Configs
from spritesheet import SpriteSheet
import pygame as pg

class Player:
    def __init__(self, name: str):
        self.ui = AllUI()
        self.name = name
        self.health = 100
        self.level = 1
        self.exp = 0
        self.damage = 1
        self.evasion = 0.1
        self.skill1_status = False
        self.skill2_status = False

        self.x = 390
        self.y = 500
        self.speed = Configs.get('SPEED')

        self.animation_list = []
        self.animation_steps = 2
        self.last_up = pg.time.get_ticks()
        self.cool_down = 250
        self.frame = 0

        self.idle = True
    def level_up(self):
        pass

    def reduce_hp(self, damage: int):
        pass

    def die(self):
        pass

    def attack(self, enemy):
        pass

    def dodge(self):
        pass

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
        elif (self.x < 330) and (185 <= self.y <= 188) or (self.x > 550) and (185 <= self.y <= 188):
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
        
    def draw_walk(self):
        sprite_sheet_image = pg.image.load("final_prog2/assets/char.png").convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        current_time = pg.time.get_ticks()
        if current_time - self.last_up >= self.cool_down:
            self.frame += 1
            self.last_up = current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0

        for i in range(self.animation_steps):
            self.animation_list.append(sprite_sheet.get_image((0, 0), i, 24, 24, 2.5, Configs.get('MAGENTA')))
    