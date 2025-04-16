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
        # self.__weapon = Weapons()
        self.__mob_gacha = monster.Monster_TMP.monster
        self.__hostile_area = ["plain"]
        # [slime, goblin, hop]
        self.__mob_rate = {"plain": [1, 0, 0]}
        self.__mobs = None
        
        pg.init()
        pg.display.set_caption("Slash Mobs!")
        self.__screen = pg.display.set_mode((Configs.get('WIN_SIZE_W'), Configs.get('WIN_SIZE_H')))
        self.__clock = pg.time.Clock()
        self.__player = Player(screen=self.__screen, name="")
        self.__ui = AllUI(self.__screen)

        # for main loop
        self.__running = True
        # for check combat status
        self.__ready = False
        # for check skill animation status
        self.animate = None
        
        # for combat
        self.__player_turn = True
        self.__draw_gui = False
        self.__combat = False
        
        self.__action = False

        self.__select = None
        self.__action_dct = {"attack": self.__ui.draw_attack}

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
                self.__before = scene
                return True
        elif scene == "plain":
            if self.__player.y < 100:
                self.__scene = "hall"
                self.__before = scene
                return True    
            if self.__player.x > 750:
                self.__scene = "shop"
                self.__before = scene
                return True
        elif scene == "shop":
            if self.__player.y > 600:
                self.__scene = "plain"
                self.__before = scene
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
            elif scene == "combat":
                self.__player.x = 800
                self.__player.y = 300
                print(self.__player.x, self.__player.y)
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

    # Place mob on determined pos when enter combat scene
    def create_mob_incombat(self):
        if self.__mobs.name == "slime":
            self.__mobs.x = Configs.get('MOB_x') + 50
            self.__mobs.y = Configs.get('MOB_y') + 120
        elif self.__mobs.name == "goblin":
            self.__mobs.x = Configs.get('MOB_x')
            self.__mobs.y = Configs.get('MOB_y')
        elif self.__mobs.name == "dark":
            self.__mobs.x = Configs.get('MOB_x')
            self.__mobs.y = Configs.get('MOB_y') + 70
        else:
            pass
        self.__mobs.draw_mon()
        self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))
    
    # Colelction of scenes
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

    # 3.Combat scene เเบบเละๆ
    def combat_scene(self):
        # BG
        img = self.__ui.draw_plain_bg()
        self.__screen.blit(img, (0, 0))

        # Animation intro 
        self.start_point(self.__scene, None)

        done = self.__ui.draw_enter_animation(self.__player)
        self.__draw_gui = done

        # Main
        self.create_mob_incombat()
        # Check ว่าถึง turn ของผู้เล่นรึยัง
        if self.__player_turn:
            # ถึงเเล้วให้วาด GUI
            if self.__draw_gui:
                self.__ui.draw_gui_combat()
                # print("GUI ON!")
                self.__action = True
        self.__screen.blit(self.__player.draw_walk_left(), (self.__player.x, self.__player.y))

    # Main loop
    def run(self):
        while self.__running:
            self.__clock.tick(Configs.get('FPS'))
            event = pg.event.get()
            for e in event:
                if e.type == pg.QUIT:
                    self.__running = False

                # Check for combat start
                if self.__ready:
                    if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                        self.__combat = True
                        self.__enter_scene = True
                        self.__ready = False

                # Check for skill trigger
                if self.__action:
                    # self.__draw_gui = False
                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_z:
                            self.__select = "attack"
                            self.__draw_gui = False
                            print("GUI OFF!")
                            print(self.__draw_gui)
                            self.animate = True
                            self.__action = False

            # Check animation
            if self.animate:
                print(self.__draw_gui)
                # print("animating")
                done = self.__action_dct[self.__select](self.__player)
                self.__draw_gui = done
                if self.__draw_gui:
                    print("finish animating")
                    self.__ui.animate1 = True
                    self.animate = False
                    self.__action = True

            # 2. Combat scene
            if self.__combat:
                self.__scene = "combat"
                # Do intro first
                if self.__ui.intro_battle:
                    self.__ui.draw_intro_battle()

                # After intro add in elements
                else:
                    self.__scene_dct[self.__scene]()
                        
            else:
                # 1. Normal scene without engaing in combat
                self.__scene_dct[self.__scene]()
                if self.__scene in self.__hostile_area: 
                    self.__ready = self.create_mob()

            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
