import pygame as pg

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, cords: tuple, frame, width, height, scale, color):
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, cords, (0, (frame * height), width, height))

        # Make image larger
        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image
