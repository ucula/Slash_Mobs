import pygame as pg

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image
    
    def get_effects(self, cords: tuple, frame, width, height, scale, color, row=0):
        image = pg.Surface((width, height)).convert()
        image.fill((1,2,3))
        image.blit(self.sheet, cords, ((frame * width), height*row, width, height))

        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((1,2,3))
        return image
    
    def get_monster(self, cords: tuple, frame, width, height, scale, color=None):
        image = pg.Surface((width, height)).convert() 
        image.fill((1,2,3))
        image.blit(self.sheet, cords, ((frame * width), 0, width, height))

        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((1,2,3))
        return image

    def get_walk(self, cords: tuple, frame, width, height, scale, color, row=0):
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, cords, (width*row, (frame * height), width, height))

        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image
    
    def get_item(self, cords: tuple, frame, width, height, scale, color, row=0):
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, cords, (width*row, (frame * height), width, height))

        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image
    