from player import Player
from weapon import Weapons
import monster
from ui import AllUI
from config import Configs
import pygame as pg
import random

class Game:
    def __init__(self):
        # self.__weapon = Weapons()
        self.__rand_mob = monster.Monster_TMP.monster
        self.__hostile_areas = ["PLAIN"]
        self.__mob_rate = {"PLAIN": [0.8, 0.15, 0.05]}
        self.__mobs = None
        
        pg.init()
        pg.display.set_caption("Slash Mobs!")
        self.__screen = pg.display.set_mode((Configs.get('WIN_SIZE_W'), Configs.get('WIN_SIZE_H')))
        self.__clock = pg.time.Clock()
        self.__player = Player(self.__screen, name="Ucula")
        self.__ui = AllUI(self.__screen)

        # for main loop
        self.__running = True
        
        # delay switches
        self.__delay_done = False
        self.__start_time = 0
        self.__time_lock = False
        self.__mob_delay = 1000

        # cut scene switch
        self.__transition = False

        # Player animation in non-combat (DONE)
        self.__walk = "IDLE"
        self.__walk_direction = {'IDLE': self.__player.draw_idle,
                               'LEFT': self.__player.draw_walk_left,
                               'RIGHT': self.__player.draw_walk_right ,
                               'UP': self.__player.draw_walk_up ,
                               'DOWN': self.__player.draw_walk_down}
        # Normal scene
        self.__before = None
        self.__scene = 'HALL'
        self.__enter_scene = False

        # for check combat status
        self.__engage_ready = False
        self.__combat = False

        # for player
        self.__state = "IDLE"
        self.__player_turn = False
        self.__skill = {"ATTACK": self.__ui.draw_attack,
                        "RUN": self.reset}

        # for monster
        self.__mob_turn = False
        self.__mob_select = None
        self.__already_place_mob = False
        
    # Reset Combat
    def reset(self, a):
        self.__combat = False
        self.__player_turn = False
        self.__engage_ready = False
        self.__transition = True

    # Cut scene (Done)
    def transition(self):
        if self.__transition:
            self.__transition = self.__ui.draw_screen_transition(Configs.get('WIN_SIZE_W')+100)
            return True
        return False
    
    # Known bug
    def character_animate(self, scene):
        self.__player.borders[scene]()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.__walk = "UP"
            self.__player.y -= self.__player.speed  
            # self.__player.draw_walk_up()
            # self.__screen.blit(self.__player.animation_up[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_s]:
            self.__walk = "DOWN"
            self.__player.y += self.__player.speed
            # self.__player.draw_walk_down()
            # self.__screen.blit(self.__player.animation_down[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_a]:
            self.__walk = "LEFT"
            self.__player.x -= self.__player.speed
            # self.__player.draw_walk_left()
            # self.__screen.blit(self.__player.animation_left[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_d]:
            self.__walk = "RIGHT"
            self.__player.x += self.__player.speed
            # self.__player.draw_walk_right()
            # self.__screen.blit(self.__player.animation_right[self.__player.frame], (self.__player.x, self.__player.y))       
        self.__screen.blit(self.__walk_direction[self.__walk]() , (self.__player.x, self.__player.y))
    
    def check_scene_change(self, scene):
        if scene == "HALL":
            if self.__player.y > 600:
                self.__scene = "PLAIN"
                self.__before = scene
                return True
        elif scene == "PLAIN":
            if self.__player.y < 100:
                self.__scene = "HALL"
                self.__before = scene
                return True    
            if self.__player.x > 750:
                self.__scene = "SHOP"
                self.__before = scene
                return True
        elif scene == "SHOP":
            if self.__player.y > 600:
                self.__scene = "PLAIN"
                self.__before = scene
                return True
        else:
            pass

        if scene not in self.__hostile_areas:
            self.__mobs = None
    
    # Set player pos when entering new scene
    def start_point(self, scene=None, before=None, combat=None):
        if self.__enter_scene:
            if scene == "HALL":
                self.__player.x = 390
                self.__player.y = 550
            elif scene == "PLAIN" and before == "HALL":
                self.__player.x = 500
                self.__player.y = 150
            elif scene == "PLAIN" and before == "SHOP": 
                self.__player.x = 750
                self.__player.y = 300
            elif scene == "SHOP":
                self.__player.x = 350
                self.__player.y = 550
            elif combat is not None:
                self.__player.x = 800
                self.__player.y = 300
        self.__enter_scene = False
    
    # Generate random x, y coordinates according to scene
    def gen_cords(self):
        if self.__scene == "PLAIN":
            x = random.randint(80, 650)
            y = random.randint(190, 250)
        else:
            # x = random.randint(0,Configs.get('WIN_SIZE_W'))
            # y = random.randint(0,Configs.get('WIN_SIZE_H'))
            pass
        return x, y

    # Return random mob to generate on that scene
    def random_mob(self):
        tmp = random.choices(self.__rand_mob, self.__mob_rate[self.__scene])
        select = tmp[0]
        pos_x, pos_y = self.gen_cords()
        if select == "SLIME":
            tmp_mob = monster.Slime(self.__screen, 28, 25, pos_x, pos_y)
        elif select == "GOBLIN":
            tmp_mob = monster.Goblin(self.__screen, 117, 133, pos_x, pos_y)
        elif select == "DARK":
            tmp_mob = monster.Dark_Goblin(self.__screen, 57, 72, pos_x, pos_y)
        else:
            pass
        return tmp_mob

    # Create mob on and display on screen
    def create_mob(self):
        if self.__mobs is None:
            self.__mobs = self.random_mob()

        self.__mobs.draw_monster()
        self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))

    # Place mob on determined pos when enter combat scene
    def create_mob_incombat(self):
        if not self.__already_place_mob:
            if self.__mobs.name == "SLIME":
                self.__mobs.x = Configs.get('MOB_x') + 50
                self.__mobs.y = Configs.get('MOB_y') + 120
            elif self.__mobs.name == "GOBLIN":
                self.__mobs.x = Configs.get('MOB_x')
                self.__mobs.y = Configs.get('MOB_y')
            elif self.__mobs.name == "DARK":
                self.__mobs.x = Configs.get('MOB_x')
                self.__mobs.y = Configs.get('MOB_y') + 70
            self.__already_place_mob = True

    # Non-combat
    def normal_scene(self):
        # BG
        bg = self.__ui.draw_bg(self.__scene)
        self.__screen.blit(bg, (0, 0))  

        self.start_point(self.__scene, self.__before)
        self.character_animate(self.__scene)
        if self.check_scene_change(self.__scene):
            self.__enter_scene = True  

    def user_event(self):
        event = pg.event.get()
        for e in event:
            if (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE) or e.type == pg.QUIT:
                self.__running = False

            # Ready up
            if self.__engage_ready:
                if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                    self.__combat = True
                    self.__enter_scene = True
                    self.__engage_ready = False
                    self.__transition = True

            # Check for skill trigger
            if self.__state == "IDLE" and self.__player_turn:
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_z:
                        self.__state = "ATTACK"
                    elif e.key == pg.K_r:
                        self.__state = "RUN"
                    print(self.__state)
        
    """
    TODO: 
    - Add Mob's turn 
    - Add End battle 
    - Add Health bar on top left
    """

    # 3.Combat scene
    def combat_scene(self):
        self.start_point(combat=1)
        bg = self.__ui.draw_bg(self.__scene)
        self.__screen.blit(bg, (0, 0))
        self.create_mob_incombat()

        # Enter animation
        if not self.__ui.draw_enter_animation(self.__player) and not self.__mob_turn:
            self.__player_turn = True

        # Player's turn
        if self.__player_turn:
            if self.__state == "IDLE":
                self.__ui.draw_gui_combat()
            else:
                if not self.__skill[self.__state](self.__player):
                    self.__player_turn = False

                    # ปิดอันนี้เพื่อลองสกิล Player
                    self.__mob_turn = True 
                    # -------------------------

                    self.__state = "IDLE"
                    self.__ui.animate1 = True

        # Mob's turn
        if self.__mob_turn:
            if self.__mob_select is None:
                print("Entering mob's turn")
                print(self.__mobs.x)
                self.__mob_select = random.choices(list(self.__mobs.skill.keys()), self.__mobs.skill_chances)
                print(f'Mobs : {self.__mob_select[0]}')
            else:
                if self.__delay_done:
                    if self.__mobs.skill[self.__mob_select[0]](self.__mobs):
                        # self.__mob_turn = False
                        # self.__mob_select = None
                        # self.__delay_done = False
                        # self.__player_turn = True
                        pass
                else:
                    self.__ui.draw_mob_skill_display(self.__mob_select)
                    self.delay()

        # Animate Mob and player
        self.__mobs.draw_monster()
        self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))
        self.__screen.blit(self.__player.draw_walk_left(), (self.__player.x, self.__player.y))
    
    def delay(self):
        current_time = pg.time.get_ticks()
        if not self.__time_lock:
            self.__start_time = pg.time.get_ticks()
            self.__time_lock = True
        if current_time - self.__start_time >= self.__mob_delay:
            self.__delay_done = True

# Main loop
    def run(self):
        while self.__running:
            self.__clock.tick(Configs.get('FPS'))

            # 1. Normal scene without engaing in combat (DONE)
            if not self.__combat:
                # Intro 
                if not self.transition():
                    # Scene
                    self.normal_scene()
                    if self.__scene in self.__hostile_areas: 
                        self.create_mob()
                        if self.__mobs.in_range(self.__player):
                            self.__engage_ready = True
                            
            # 2. Combat scene
            elif self.__combat:
                if not self.transition():
                    self.combat_scene()        
                    
            self.user_event()
            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
