from config import Configs
import item 
import pygame as pg

class Shop:
    def __init__(self, screen):
        self.__font = pg.font.Font(None, 30)
        self.__screen = screen
        self.potion = item.Potion()
        self.hi_potion = item.Hi_Potion()
        self.x_potion = item.X_Potion()
        self.bomb = item.Bomb()
        self.battle_drum = item.Battle_drum()
        self.greed = item.Greed_bag()
        self.longsword = item.Longsword()
        self.mace = item.Mace()
        self.knife = item.Knife()
        # print(self.knife)
        
        self.select = None
        self.check = None

    def draw_menu(self, player, weapon=0):
        coords = [100, 100, 600, 400]
        offset = 3
        box_width = 200
        box_height = 133
        box_x = 100
        box_y = 100
        tmp1 = 0
        tmp2 = 0
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (coords[0], coords[1], coords[2], coords[3]))
        pg.draw.rect(self.__screen, Configs.get('CREAMY'), (coords[0]+offset, coords[1]+offset, coords[2]-2*offset, coords[3]-2*offset))
        for _ in range(3):
            for _ in range(3):
                pg.draw.rect(self.__screen, Configs.get('BLACK'), (box_x+tmp1, box_y+tmp2, box_width, box_height), 3)
                tmp1 += box_width
            tmp1 = 0
            tmp2 += box_height

        pg.draw.rect(self.__screen, Configs.get('BLACK'), (600, 0, 800, 60), 60)
        pg.draw.rect(self.__screen, Configs.get('CREAMY'), (600+offset,0+offset, 800-2*offset, 60-2*offset))
        coin_text = self.__font.render(f"Coin: {player.coin:.0f}", True, Configs.get("BLACK"))
        coin_rect = coin_text.get_rect(center=(700, 30))

        box1_text = self.__font.render(f"{self.longsword.name} {self.longsword.price}$ (1)", True, Configs.get("BLACK"))
        box1_rect = coin_text.get_rect(topleft=(105, 116.5))

        box2_text = self.__font.render(f"{self.knife.name} {self.knife.price}$ (2)", True, Configs.get("BLACK"))
        box2_rect = coin_text.get_rect(topleft=(305, 116.5))

        box3_text = self.__font.render(f"{self.mace.name} {self.mace.price}$ (3)", True, Configs.get("BLACK"))
        box3_rect = coin_text.get_rect(topleft=(505, 116.5))

        box4_text = self.__font.render(f"{self.potion.name} {self.potion.price}$ (4)", True, Configs.get("BLACK"))
        box4_rect = coin_text.get_rect(topleft=(105, 249.5))

        box5_text = self.__font.render(f"{self.hi_potion.name} {self.hi_potion.price}$ (5)", True, Configs.get("BLACK"))
        box5_rect = coin_text.get_rect(topleft=(305, 249.5))

        box6_text = self.__font.render(f"{self.x_potion.name} {self.x_potion.price}$ (6)", True, Configs.get("BLACK"))
        box6_rect = box6_text.get_rect(topleft=(505, 249.5))

        box7_text = self.__font.render(f"{self.battle_drum.name} {self.battle_drum.price}$ (7)", True, Configs.get("BLACK"))
        box7_rect = box7_text.get_rect(topleft=(105, 382.5))

        box8_text = self.__font.render(f"{self.greed.name} {self.greed.price}$ (8)", True, Configs.get("BLACK"))
        box8_rect = box8_text.get_rect(topleft=(305, 382.5))

        box9_text = self.__font.render(f"{self.bomb.name} {self.bomb.price}$ (9)", True, Configs.get("BLACK"))
        box9_rect = box9_text.get_rect(topleft=(505, 382.5))

        self.__screen.blit(coin_text, coin_rect)
        self.__screen.blit(box1_text, box1_rect)
        self.__screen.blit(box2_text, box2_rect)
        self.__screen.blit(box3_text, box3_rect)
        self.__screen.blit(box4_text, box4_rect)
        self.__screen.blit(box5_text, box5_rect)
        self.__screen.blit(box6_text, box6_rect)
        self.__screen.blit(box7_text, box7_rect)
        self.__screen.blit(box8_text, box8_rect)
        self.__screen.blit(box9_text, box9_rect)
    
    def buy(self, player, select=None):
        if select == 49:
            self.select = self.longsword
        elif select == 50:
            self.select = self.knife
        elif select == 51:
            self.select = self.mace
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
        