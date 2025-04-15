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

        self.__running = True
        # self.__monster = Monsters()
        # self.__weapon = Weapons()
        # self.__ui = AllUI()

    def run(self):
        while self.__running:
            self.__clock.tick(Configs.get('FPS'))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False

            # Animtaion draw
            if self.__player.status == 'idle':
                self.__player.animation_list.clear()
            self.__screen.fill(Configs.get('WHITE'))
            self.__player.draw_walk()
            self.__screen.blit(self.__player.animation_list[self.__player.frame], (self.__player.x, self.__player.y))

            # Walk
            keys = pg.key.get_pressed()
            if keys:
                self.__player.status = 'walk'
                if keys[pg.K_w]:
                    self.__player.y -= self.__player.speed  

                elif keys[pg.K_s]:
                    self.__player.y += self.__player.speed

                elif keys[pg.K_a]:
                    self.__player.x -= self.__player.speed

                elif keys[pg.K_d]:
                    self.__player.x += self.__player.speed
            else:
                self.__player.status = 'idle'

            
            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
