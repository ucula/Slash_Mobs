from weapon import Weapons
from config import Configs
import pygame as pg

class Shop:
    def __init__(self, screen):
        self.__font = pg.font.Font(None, 30)
        self.__screen = screen

    def draw_menu(self):
        coords = [100, 100, 600, 400]
        offset = 3
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (coords[0], coords[1], coords[2], coords[3]))
        pg.draw.rect(self.__screen, Configs.get('CREAMY'), (coords[0]+offset, coords[1]+offset, coords[2]-2*offset, coords[3]-2*offset))

        atk_text = self.__font.render("Shop", True, Configs.get("BLACK"))
        atk_rect = atk_text.get_rect(center=(400, 120))
        self.__screen.blit(atk_text, atk_rect)