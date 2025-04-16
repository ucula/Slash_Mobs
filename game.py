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
        self.__mob_gacha = monster.Monster_TMP.monster
        
        # [slime, goblin, hop]
        self.__mob_rate = {"plain": [0.8, 0.15, 0.05]}
        self.__mobs = None
        # self.__weapon = Weapons()
        self.__combat = False

        pg.init()
        pg.display.set_caption("Slash Mobs!")
        self.__screen = pg.display.set_mode((Configs.get('WIN_SIZE_W'), Configs.get('WIN_SIZE_H')))
        self.__clock = pg.time.Clock()

        self.__player = Player(screen=self.__screen, name="")
        self.__ui = AllUI(self.__screen)

        self.__running = True

        self.__scene_dct = {"hall": self.hall_scene,
                            "plain": self.plain_scene,
                            "shop": self.shop_scene
                            }
        self.__max_range = 1
        self.__generate = True
        self.__before = None
        self.__scene = 'hall'
        self.__enter_scene = False
        
    # Known bug
    def char_animate(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.__player.y -= self.__player.speed  
            self.__screen.blit(self.__player.draw_walk_up(), 
                               (self.__player.x, self.__player.y))
            # self.__player.draw_walk_up()
            # self.__screen.blit(self.__player.animation_up[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_s]:
            self.__player.y += self.__player.speed
            self.__screen.blit(self.__player.draw_walk_down(), 
                               (self.__player.x, self.__player.y))
            # self.__player.draw_walk_down()
            # self.__screen.blit(self.__player.animation_down[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_a]:
            self.__player.x -= self.__player.speed
            self.__screen.blit(self.__player.draw_walk_left(), 
                               (self.__player.x, self.__player.y))
            # self.__player.draw_walk_left()
            # self.__screen.blit(self.__player.animation_left[self.__player.frame], (self.__player.x, self.__player.y))

        elif keys[pg.K_d]:
            self.__player.x += self.__player.speed
            self.__screen.blit(self.__player.draw_walk_right(), 
                               (self.__player.x, self.__player.y))
            # self.__player.draw_walk_right()
            # self.__screen.blit(self.__player.animation_right[self.__player.frame], (self.__player.x, self.__player.y))
            
        else:
            img = self.__player.draw_idle()
            self.__screen.blit(img , (self.__player.x, self.__player.y))
    
    # Set player pos when entering new map
    def start_point(self, x, y):
        if self.__enter_scene:
            self.__player.x = x
            self.__player.y = y
            self.__enter_scene = False
    
    # Generate random x, y coordinates according to scene
    def gen_cords(self):
        if self.__scene == "plain":
            x = random.randint(100, 600)
            y = random.randint(180, 250)
        else:
            pass

        return x, y

    # Return random mob to generate on that scene
    def random_mob(self):
        tmp = random.choices(self.__mob_gacha, self.__mob_rate[self.__scene])
        select = tmp[0]
        pos_x, pos_y = self.gen_cords()
        if select == "slime":
            tmp_mob = monster.Slime(self.__screen, pos_x, pos_y)
        elif select == "goblin":
            tmp_mob = monster.Goblin(self.__screen, pos_x, pos_y)
        elif select == "hop":
            tmp_mob = monster.Dark_Goblin(self.__screen, pos_x, pos_y)
        else:
            pass

        return tmp_mob

    # Add random mobs to list
    def create_mob(self):
        self.__mobs = self.random_mob()

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
        # Background
        plain_img = self.__ui.draw_plain_bg()
        self.__screen.blit(plain_img, (0, 0))
        if self.__before == "shop":
            self.start_point(750, 300)
        else:
            self.start_point(500, 150)

        # Player's animation
        self.char_animate()
        self.__player.check_lim_plain()

        # Create monsters and make themm appear on screen
        if self.__generate:
            self.create_mob()
            self.__generate = False
        
        img = self.__mobs.draw_mon()
        self.__screen.blit(img, (self.__mobs.x, self.__mobs.y))
        self.__mobs.check_distance(self.__player)

        # Check scene change
        if self.__player.y < 100:
            self.__scene = "hall"
            self.__enter_scene = True
            self.__mobs = None
            self.__generate = True

        if self.__player.x > 750:
            self.__scene = "shop"
            self.__enter_scene = True
            self.__mobs = None
            self.__generate = True
    
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
            
            # If player encounter check if want to fight
            # if self.__mobs.ready:
            #     print(self.__mobs.ready)
            #     if event.type == pg.KEYDOWN and pg.K_SPACE:
            #         self.__combat = True
            #         self.__mobs.ready = False
                
            # if self.__combat:
            #     self.__ui.draw_intro_battle()
                
            # else:
            # Start scene
            self.__scene_dct[self.__scene]() 

            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
