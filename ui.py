import pygame as pg

class AllUI:
    def __init__(self):
        self.__font = None

    def draw_hall_bg(self):
        image = pg.image.load("final_prog2/assets/hall.jpg").convert()
        return image
    
    def draw_plain_bg(self):
        image = pg.image.load("final_prog2/assets/plain.jpg").convert()
        return image
    
    def draw_game_over(self):
        pass

    def draw_start(self):
        pass

    def draw_tutorial(self):
        pass

    def draw_status(self):
        pass
    