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
        self.__hostile_area = ["plain"]
        # [slime, goblin, hop]
        self.__mob_rate = {"plain": [0.5, 0.5, 0.5]}
        self.__mobs = None
        # self.__weapon = Weapons()

        pg.init()
        pg.display.set_caption("Slash Mobs!")
        self.__screen = pg.display.set_mode((Configs.get('WIN_SIZE_W'), Configs.get('WIN_SIZE_H')))
        self.__clock = pg.time.Clock()

        self.__player = Player(screen=self.__screen, name="")
        self.__ui = AllUI(self.__screen)

        self.__running = True

        self.__combat = False

        self.__scene_dct = {"hall": self.hall_scene,
                            "plain": self.plain_scene,
                            "shop": self.shop_scene,
                            "combat": self.combat_scene
                            }
        self.__generate = True
        self.__before = None
        self.__scene = 'hall'
        self.__enter_scene = False
        
    # Known bug
    def character_animate(self, scene):
        self.__player.borders[scene]()
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
    
    def check_scene_change(self, scene):
        if scene == "hall":
            if self.__player.y > 600:
                self.__scene = "plain"
                self.__before = "hall"
                return True
        elif scene == "plain":
            if self.__player.y < 100:
                self.__scene = "hall"
                self.__before = "plain"
                return True    
            if self.__player.x > 750:
                self.__scene = "shop"
                self.__before = "plain"
                return True
        elif scene == "shop":
            if self.__player.y > 600:
                self.__scene = "plain"
                self.__before = "shop"
                return True
        else:
            pass

        if scene not in self.__hostile_area:
            self.__generate = True
            self.__mobs = None
    
    # Set player pos when entering new scene
    def start_point(self, scene, before):
        if self.__enter_scene:
            if scene == "hall":
                self.__player.x = 390
                self.__player.y = 550
                print("coords set")
            elif scene == "plain" and before == "hall":
                self.__player.x = 500
                self.__player.y = 150
            elif scene == "plain" and before == "shop": 
                self.__player.x = 750
                self.__player.y = 300
            elif scene == "shop":
                self.__player.x = 350
                self.__player.y = 550
        self.__enter_scene = False
    
    # Generate random x, y coordinates according to scene
    def gen_cords(self):
        if self.__scene == "plain":
            x = random.randint(80, 650)
            y = random.randint(190, 250)
        else:
            # x = random.randint(0,Configs.get('WIN_SIZE_W'))
            # y = random.randint(0,Configs.get('WIN_SIZE_H'))
            pass
        return x, y

    # Return random mob to generate on that scene
    def random_mob(self):
        tmp = random.choices(self.__mob_gacha, self.__mob_rate[self.__scene])
        select = tmp[0]
        pos_x, pos_y = self.gen_cords()
        if select == "slime":
            tmp_mob = monster.Slime(self.__screen, 28, 25, pos_x, pos_y)
        elif select == "goblin":
            tmp_mob = monster.Goblin(self.__screen, 117, 133, pos_x, pos_y)
        elif select == "hop":
            tmp_mob = monster.Dark_Goblin(self.__screen, 57, 72, pos_x, pos_y)
        else:
            pass
        return tmp_mob

    # Create mob on and display on screen
    def create_mob(self):
        if self.__generate:
            self.__mobs = self.random_mob()
            self.__generate = False
        self.__mobs.draw_mon()
        self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))
        activate = self.__mobs.check_distance(self.__player)
        return activate

    # Reduce repeatness in scenes function
    def tmp_scene(self):
        self.start_point(self.__scene, self.__before)
        self.character_animate(self.__scene)
        if self.check_scene_change(self.__scene):
            self.__enter_scene = True 

    # Colelctions of scene
    def hall_scene(self):
        hall_img = self.__ui.draw_hall_bg()
        self.__screen.blit(hall_img, (0, 0))
        self.tmp_scene()
         
    def plain_scene(self):
        plain_img = self.__ui.draw_plain_bg()
        self.__screen.blit(plain_img, (0, 0))
        self.tmp_scene()

    def shop_scene(self):
        shop_img = self.__ui.draw_shop_bg()
        self.__screen.blit(shop_img, (0, 0))
        self.tmp_scene()

    def combat_scene(self):
        img = self.__ui.draw_combat_bg()
        self.__screen.blit(img, (0, 0))

    # Main loop
    def run(self):
        while self.__running:
            self.__clock.tick(Configs.get('FPS'))
            event = pg.event.get()
            for e in event:
                if e.type == pg.QUIT:
                    self.__running = False

            if self.__combat:
                self.__scene = "combat"
                if self.__ui.intro:
                    self.__ui.draw_intro_battle()
                else:
                    self.__scene_dct[self.__scene]()
                    
            else:
                self.__scene_dct[self.__scene]()
                if self.__scene in self.__hostile_area: 
                    ready = self.create_mob()
                    if ready:
                        for e in event:
                            if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                                self.__combat = True

            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
