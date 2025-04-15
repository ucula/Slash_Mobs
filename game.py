from player import Player
from weapon import Weapons
from monster import Monsters
from ui import AllUI
from spritesheet import SpriteSheet
from config import Configs
import pygame as pg

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
        if self.__player.idle:
            self.__player.animation_list.clear()
        self.__player.draw_walk()
        self.__screen.blit(self.__player.animation_list[self.__player.frame], (self.__player.x, self.__player.y))

        # Walk
        self.scene_keybind()

    def scene_keybind(self):
        keys = pg.key.get_pressed()
        if keys:
            self.__player.idle = False
            if keys[pg.K_w]:
                self.__player.y -= self.__player.speed  

            elif keys[pg.K_s]:
                self.__player.y += self.__player.speed

            elif keys[pg.K_a]:
                self.__player.x -= self.__player.speed

            elif keys[pg.K_d]:
                self.__player.x += self.__player.speed
        else:
            self.__player.idle = True

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
            self.__player.y -= 2
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
                # self.__screen.fill(Configs.get('WHITE'))

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
                # BG
                plain_img = self.__ui.draw_plain_bg()
                self.__screen.blit(plain_img, (0, 0))

                # Walk in intro
                if self.__enter_scene:
                    self.__player.x = 500
                    self.__player.y = 150
                    self.__enter_scene = False

                # Check border
                self.__player.check_lim_plain()

                # Char animation
                if self.__player.idle:
                    self.__player.animation_list.clear()
                self.__player.draw_walk()
                self.__screen.blit(self.__player.animation_list[self.__player.frame], (self.__player.x, self.__player.y))

                # Walk
                self.scene_keybind()

                # Check scene change
                if self.__player.y < 100:
                    self.__scene = "hall"
                    self.__enter_scene = True
                    # self.__screen.fill(Configs.get('WHITE'))

            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
