from player import Player
from weapon import Weapons
from monster import Monsters
from ui import AllUI
from config import Configs
import pygame as pg

class Game:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((Configs.get('WIN_SIZE_W'), Configs.get('WIN_SIZE_H')))
        self.__screen.fill(Configs.get('WHITE'))
        self.__clock = pg.time.Clock()
        self.__running = True
        # self.__player = Player()
        # self.__monster = Monsters()
        # self.__weapon = Weapons()
        # self.__ui = AllUI()
        self.__keys = {}

    def __game_reset(self):
        pass

    def user_event(self):
        pass

    def __screen_update(self):
        pass

    def run(self):
        while self.__running:
            self.__clock.tick(Configs.get('FPS'))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
                    break
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
