from player import Player
from weapon import Weapons
import monster
from ui import AllUI
from spritesheet import SpriteSheet
from config import Configs
import pygame as pg
import random

class Game:
    def __init__(self):
        # name = input("What is your name? : ")
        self.__player = Player("g")
        self.__slime_lst = []
        # self.__weapon = Weapons()

        pg.init()
        pg.display.set_caption("Slash Mobs!")
        self.__screen = pg.display.set_mode((Configs.get('WIN_SIZE_W'), Configs.get('WIN_SIZE_H')))
        self.__screen.fill(Configs.get('WHITE'))
        self.__clock = pg.time.Clock()

        self.__ui = AllUI()
        self.__running = True

        self.__generate = True
        self.__before = None
        self.__scene = 'hall'
        self.__enter_scene = False
        
    # Known bug
    def char_animate(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.__player.y -= self.__player.speed  
            self.__screen.blit(self.__player.draw_walk_up(), (self.__player.x, self.__player.y))
            # self.__player.draw_walk_up()
            # self.__screen.blit(self.__player.animation_up[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_s]:
            self.__player.y += self.__player.speed
            self.__screen.blit(self.__player.draw_walk_down(), (self.__player.x, self.__player.y))
            # self.__player.draw_walk_down()
            # self.__screen.blit(self.__player.animation_down[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_a]:
            self.__player.x -= self.__player.speed
            self.__screen.blit(self.__player.draw_walk_left(), (self.__player.x, self.__player.y))
            # self.__player.draw_walk_left()
            # self.__screen.blit(self.__player.animation_left[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_d]:
            self.__player.x += self.__player.speed
            self.__screen.blit(self.__player.draw_walk_right(), (self.__player.x, self.__player.y))
            # self.__player.draw_walk_right()
            # self.__screen.blit(self.__player.animation_right[self.__player.frame], (self.__player.x, self.__player.y))
            
        else:
            img = self.__player.draw_idle()
            self.__screen.blit(img , (self.__player.x, self.__player.y))
    
    # Determine char pos when entering new map
    def start_point(self, x, y):
        if self.__enter_scene:
            self.__player.x = x
            self.__player.y = y
            self.__enter_scene = False
    
    def create_slime(self):
        if len(self.__slime_lst) == 0:
            for _ in range(random.randint(1, 1)):
                x = random.randint(100, 600)
                y = random.randint(200, 300)
                self.__slime_lst.append(monster.Slime(x, y))

    # function for displaying hall bg
    def hall_scene(self):
        # BG
        hall_img = self.__ui.draw_hall_bg()
        self.__screen.blit(hall_img, (0, 0))
        self.start_point(390, 550)

        # Animation/Border checker
        self.char_animate()
        self.__player.check_lim_hall()

        # Check scene change
        if self.__player.y > 600:
            self.__scene = "plain"
            self.__enter_scene = True
            self.__before = "hall"

    def plain_scene(self):
        # BG
        plain_img = self.__ui.draw_plain_bg()
        self.__screen.blit(plain_img, (0, 0))
        if self.__before == "shop":
            self.start_point(750, 300)
        else:
            self.start_point(500, 150)

        # Animation/Border checker
        self.char_animate()
        self.__player.check_lim_plain()

        # Slime 
        if self.__generate:
            self.create_slime()
            self.generate = False

        for slime in self.__slime_lst:
            slime_img = slime.draw_slime()
            # slime.check_distance(self.__player)
            self.__screen.blit(slime_img, (slime.x, slime.y))
            # self.__screen.blit(slime.animation[slime.frame], (slime.x, slime.y))

        # Check scene change
        if self.__player.y < 100:
            self.__scene = "hall"
            self.__enter_scene = True
            self.__slime_lst.clear()

        if self.__player.x > 750:
            self.__scene = "shop"
            self.__enter_scene = True
            self.__slime_lst.clear()
    
    def shop_scene(self):
        # BG
        shop_img = self.__ui.draw_shop_bg()
        self.__screen.blit(shop_img, (0, 0))
        self.start_point(350, 550)

        # Animation/Border checker
        self.char_animate()
        self.__player.check_lim_shop()
        
        # Check scene change
        if self.__player.y > 600:
            self.__scene = "plain"
            self.__enter_scene = True
            self.__before = "shop"

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
                self.plain_scene()

            # Shop scene
            if self.__scene == "shop":
                self.shop_scene()

            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
