from config import Configs
import item 
import pygame as pg
import ui
from spritesheet import SpriteSheet

class Shop:
    def __init__(self, screen):
        self.__screen = screen
        self.icon_names = ["sword", "knife", "hammer", "potion", "hpotion", "xpotion", "drum", "greed", "bomb"]

        self.potion = item.Potion()
        self.hi_potion = item.Hi_Potion()
        self.x_potion = item.X_Potion()
        self.bomb = item.Bomb()
        self.battle_drum = item.Battle_drum()
        self.greed = item.Greed_bag()
        self.longsword = item.Sword()
        self.hammer = item.Hammer()
        self.knife = item.Knife()

        self.select = None

    """
    Create a shop interface that can be interacted with keyboard
    """
    def draw_menu(self, player):
        box_width = 200
        box_height = 133
        box_x = 100
        box_y = 100
        tmp1 = 0
        tmp2 = 0

        settings = Configs.ui_pos("SHOP")
        ui.AllUI.create_box(self.__screen, settings)
        for _ in range(3):
            for _ in range(3):
                pg.draw.rect(self.__screen, Configs.get('BLACK'), (box_x+tmp1, box_y+tmp2, box_width, box_height), 3)
                tmp1 += box_width
            tmp1 = 0
            tmp2 += box_height

        settings = Configs.ui_pos("COIN_BOX")
        ui.AllUI.create_box(self.__screen, settings)
        ui.AllUI.animate_text_center(self.__screen, f"Coin: {player.coin:.0f}", "BLACK", 700, 30)

        ui.AllUI.animate_text_topleft(self.__screen, f"{self.longsword.name} {self.longsword.price}$ (1)", "BLACK", 105, 116.5)
        ui.AllUI.animate_text_topleft(self.__screen, f"{self.knife.name} {self.knife.price}$ (2)", "BLACK", 305, 116.5)
        ui.AllUI.animate_text_topleft(self.__screen, f"{self.hammer.name} {self.hammer.price}$ (3)", "BLACK", 505, 116.5)

        ui.AllUI.animate_text_topleft(self.__screen, f"{self.potion.name} {self.potion.price}$ (4)", "BLACK", 105, 249.5)
        ui.AllUI.animate_text_topleft(self.__screen, f"{self.hi_potion.name} {self.hi_potion.price}$ (5)", "BLACK", 305, 249.5)
        ui.AllUI.animate_text_topleft(self.__screen, f"{self.x_potion.name} {self.x_potion.price}$ (6)", "BLACK", 505, 249.5)

        ui.AllUI.animate_text_topleft(self.__screen, f"{self.battle_drum.name} {self.battle_drum.price}$ (7)", "BLACK", 105, 382.5)
        ui.AllUI.animate_text_topleft(self.__screen, f"{self.greed.name} {self.greed.price}$ (8)", "BLACK", 305, 382.5)
        ui.AllUI.animate_text_topleft(self.__screen, f"{self.bomb.name} {self.bomb.price}$ (9)", "BLACK", 505, 382.5)
        self.icons()

    def icons(self):
        for j in range(3):
            for i in range(3):
                image = pg.image.load(Configs.item(self.icon_names[i+3*j])).convert_alpha()
                image = SpriteSheet(image).get_item(image, 32, 32, 2)
                image_rect = image.get_rect(center=(200+i*200, 180+j*133))
                item.Item_TMP.draw_item(self.__screen, image, image_rect)

    def buy(self, player, select=None):
        if select == 49:
            self.select = self.longsword
        elif select == 50:
            self.select = self.knife
        elif select == 51:
            self.select = self.hammer
        elif select == 52:
            self.select = self.potion
        elif select == 53:
            self.select = self.hi_potion
        elif select == 54:
            self.select = self.x_potion
        elif select == 55:
            self.select = self.battle_drum
        elif select == 56:
            self.select = self.greed
        elif select == 57:
            self.select = self.bomb
        
        diff = player.coin - self.select.price
        if diff < 0 or player.weapon == self.select:
            print("denied")
            return None, None
        else:
            print("success")
            player.coin -= self.select.price
            return [self.select, self.select.type]
        