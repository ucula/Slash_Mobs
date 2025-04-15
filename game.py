from player import Player
from weapon import Weapons
from monster import Monsters
from ui import AllUI
from spritesheet import SpriteSheet
from config import Configs
import pygame as pg
import time

class Game:
    def __init__(self):
        # name = input("What is your name? : ")
        self.__player = Player("g")

        pg.init()
        pg.display.set_caption("Slash Mobs!")
        self.__screen = pg.display.set_mode((Configs.get('WIN_SIZE_W'), Configs.get('WIN_SIZE_H')))
        self.__screen.fill(Configs.get('WHITE'))
        self.__clock = pg.time.Clock()

        self.__ui = AllUI()
        self.__running = True
        self.__scene = 'hall'
        self.__enter_scene = False
        self.__auto_walk = False
        # self.__monster = Monsters()
        # self.__weapon = Weapons()
    
    def char_animate(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.__player.y -= self.__player.speed  
            self.__player.draw_walk_up()
            self.__screen.blit(self.__player.animation_up[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_s]:
            self.__player.y += self.__player.speed
            self.__player.draw_walk_down()
            self.__screen.blit(self.__player.animation_down[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_a]:
            self.__player.x -= self.__player.speed
            self.__player.draw_walk_left()
            self.__screen.blit(self.__player.animation_left[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_d]:
            self.__player.draw_walk_right()
            self.__screen.blit(self.__player.animation_right[self.__player.frame], (self.__player.x, self.__player.y))
            self.__player.x += self.__player.speed
        else:
            img = self.__player.draw_idle()
            self.__screen.blit(img , (self.__player.x, self.__player.y))

    def hall_scene(self):
        # BG
        hall_img = self.__ui.draw_hall_bg()
        self.__screen.blit(hall_img, (0, 0))

        # Enter scene
        if self.__enter_scene:
            self.__player.x = 390
            self.__player.y = 600
            self.__enter_scene = False
            self.__auto_walk = True

        if self.__auto_walk:
            self.__player.y -= Configs.get('SPEED')
            self.__player.speed = 0

            self.char_animate()
            if self.__player.y < 500:
                self.__player.speed = Configs.get('SPEED')
                self.__auto_walk = False

        else:
            # Char animation
            self.char_animate()
            # Check border
            self.__player.check_lim_hall()
            # Check scene change
            if self.__player.y > 600:
                self.__scene = "plain"
                self.__enter_scene = True
        
    def plain_scene(self):
        # BG
        plain_img = self.__ui.draw_plain_bg()
        self.__screen.blit(plain_img, (0, 0))

        # Walk in intro
        if self.__enter_scene:
            self.__player.x = 500
            self.__player.y = 150
            self.__enter_scene = False
            self.__auto_walk = True
        
        if self.__auto_walk:
            self.__player.y += Configs.get('SPEED')
            self.__player.speed = 0
            
            self.char_animate()
            if self.__player.y > 200:
                self.__player.speed = Configs.get('SPEED')
                self.__auto_walk = False
        
        else:
            # Check border
            self.__player.check_lim_plain()
            self.char_animate()
            
            # Check scene change
            if self.__player.y < 100:
                self.__scene = "hall"
                self.__enter_scene = True
        
    def run(self):
        while self.__running:
            self.__clock.tick(Configs.get('FPS'))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
            
            # Hall scene
            if self.__scene == 'hall':
                self.hall_scene()

            # Plain scene
            if self.__scene == "plain":
                self.plain_scene()

            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
