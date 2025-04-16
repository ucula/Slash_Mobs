import pygame as pg
from config import Configs

class AllUI:
    def __init__(self, screen):
        self.__font = pg.font.Font(None, 30)
        self.__screen = screen
        self.__prep_size = 0
        self.__intro_size = 0

    @property
    def prep_size(self):
        return self.__prep_size
    
    @prep_size.setter
    def prep_size(self, val):
        self.__prep_size = val

    def draw_hall_bg(self):
        image = pg.image.load("final_prog2/assets/hall.jpg").convert()
        return image
    
    def draw_plain_bg(self):
        image = pg.image.load("final_prog2/assets/plain.jpg").convert()
        return image
    
    def draw_shop_bg(self):
        image = pg.image.load("final_prog2/assets/shop.jpg").convert()
        return image
    
    def draw_mob_info(self):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (250, 180, self.prep_size, self.prep_size), width=5, border_radius=10)
        pg.draw.rect(self.__screen, Configs.get('GRAY'), (255, 185, self.prep_size-10, self.prep_size-10))
        if self.prep_size != 300:
            self.prep_size += 50
        if self.prep_size == 300:
            text1 = self.__font.render("Monster info: bla bla", True, Configs.get("BLACK"))
            text1_rect = text1.get_rect(center=(400, 300))

            text2 = self.__font.render("Press SPACE to fight", True, Configs.get("BLACK"))
            text2_rect = text1.get_rect(center=(400, 350))

            self.__screen.blit(text1, text1_rect)
            self.__screen.blit(text2, text2_rect)

    def draw_intro_battle(self):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (255, 185, self.__intro_size, 600))
        if self.__intro_size != 800:
            self.__intro_size += 50

    def draw_game_over(self):
        pass

    def draw_start(self):
        pass

    def draw_tutorial(self):
        pass

    def draw_status(self):
        pass
    