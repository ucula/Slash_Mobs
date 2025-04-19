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
        self.__rand_mob = monster.Monster_TMP.monster
        self.__hostile_areas = ["PLAIN"]
        # [slime, goblin, hop]
        self.__mob_rate = {"PLAIN": [0.8, 0.15, 0.05]}
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
        self.__engage_ready = False
        # for check skill animation status
        self.__skill_animating = False
        self.__gui = False
        self.__combat = False
        self.__transition = False
        self.__action = False
        # Player animation (DONE)
        self.__player_state = "IDLE"
        self.__states = {'IDLE': self.__player.draw_idle,
                               'LEFT': self.__player.draw_walk_left,
                               'RIGHT': self.__player.draw_walk_right ,
                               'UP': self.__player.draw_walk_up ,
                               'DOWN': self.__player.draw_walk_down}
        # for player
        self.__player_turn = True
        self.__select = None
        self.__skill = {"ATTACK": self.__ui.draw_attack}
        # for monster
        self.__mob_turn = not self.__player_turn
        self.__mob_select = None
        self.__generate = True
        self.__before = None
        self.__scene = 'HALL'
        self.__enter_scene = False
        
    # Known bug
    def character_animate(self, scene):
        self.__player.borders[scene]()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.__player_state = "UP"
            self.__player.y -= self.__player.speed  
            # self.__player.draw_walk_up()
            # self.__screen.blit(self.__player.animation_up[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_s]:
            self.__player_state = "DOWN"
            self.__player.y += self.__player.speed
            # self.__player.draw_walk_down()
            # self.__screen.blit(self.__player.animation_down[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_a]:
            self.__player_state = "LEFT"
            self.__player.x -= self.__player.speed
            # self.__player.draw_walk_left()
            # self.__screen.blit(self.__player.animation_left[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_d]:
            self.__player_state = "RIGHT"
            self.__player.x += self.__player.speed
            # self.__player.draw_walk_right()
            # self.__screen.blit(self.__player.animation_right[self.__player.frame], (self.__player.x, self.__player.y))       
        self.__screen.blit(self.__states[self.__player_state]() , (self.__player.x, self.__player.y))
    
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
            self.__generate = True
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
        if self.__generate:
            self.__mobs = self.random_mob()
            self.__generate = False
        self.__mobs.draw_monster()
        self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))

    # Place mob on determined pos when enter combat scene
    def create_mob_incombat(self):
        if self.__mobs.name == "SLIME":
            self.__mobs.x = Configs.get('MOB_x') + 50
            self.__mobs.y = Configs.get('MOB_y') + 120
        elif self.__mobs.name == "GOBLIN":
            self.__mobs.x = Configs.get('MOB_x')
            self.__mobs.y = Configs.get('MOB_y')
        elif self.__mobs.name == "DARK":
            self.__mobs.x = Configs.get('MOB_x')
            self.__mobs.y = Configs.get('MOB_y') + 70
       
    # Colelction of scenes
    def normal_scene(self):
        bg = self.__ui.draw_bg(self.__scene)
        self.__screen.blit(bg, (0, 0))
        self.start_point(self.__scene, self.__before)
        self.character_animate(self.__scene)
        if self.check_scene_change(self.__scene):
            self.__enter_scene = True    

    """
    TODO: 
    - make code looks cleaner
    - Add Mob's turn 
    - Add End battle 
    - Add Flee option
    - Add Health bar on top left

    """
    # 3.Combat scene เเบบเละๆ
    def combat_scene(self):
        # Animation intro (1 time)
        self.start_point(combat=1)

        # Main
        bg = self.__ui.draw_bg(self.__scene)
        self.__screen.blit(bg, (0, 0))
        self.create_mob_incombat()

        # Player's turn
        if self.__player_turn:
            if self.__gui:
                self.__ui.draw_gui_combat()
                self.__action = True
        else:
            self.__gui = False

        # Mob's turn
        if self.__mob_turn and self.__mob_select is not None:
            self.__mob_select = random.choices(list(self.__mobs.skill.key()), self.__mobs.skill_chances)

        self.__mobs.draw_monster()
        self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))
        self.__screen.blit(self.__player.draw_walk_left(), (self.__player.x, self.__player.y))

    def animate_player_skill(self):
        if self.__skill_animating:
            self.__skill_animating = self.__skill[self.__select](self.__player)
        else:
            self.__action = True
            self.__ui.animate1 = True
    
    def animate_monster_skill(self):
        if self.__skill_animating:
            self.__skill_animating = self.__mobs.skill[self.__select](self.__mobs)

    def user_event(self):
        event = pg.event.get()
        for e in event:
            if (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE) or e.type == pg.QUIT:
                self.__running = False

            # Check for combat start
            if self.__engage_ready:
                if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                    # self.__before = self.__scene
                    self.__combat = True
                    self.__enter_scene = True
                    self.__engage_ready = False
                    self.__transition = True

            # Check for skill trigger
            if self.__action:
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_z:
                        self.__select = "ATTACK"
                        self.__skill_animating = True
                    elif e.key == pg.K_r:
                        self.reset()
                    self.__gui = False
                    self.__action = False
                    # self.__player_turn = False

    def reset(self):
        self.__generate = True
        self.__mobs = None
        self.__combat = False
        self.__engage_ready = False
        self.__skill_animating = False
        self.__player_turn = True
        self.__gui = False
        self.__action = False
        self.__select = None
        self.__transition = True
        
# Main loop
    def run(self):
        while self.__running:
            self.__clock.tick(Configs.get('FPS'))
            self.user_event()
            # 1. Normal scene without engaing in combat (DONE)
            if not self.__combat:
                if self.__transition:
                    self.__transition = self.__ui.draw_screen_transition(Configs.get('WIN_SIZE_W')+100)
                else:
                    self.normal_scene()
                    if self.__scene in self.__hostile_areas: 
                        self.create_mob()
                        if self.__mobs.in_range(self.__player):
                            self.__engage_ready = True
            # 2. Combat scene
            else: 
                # Do intro first
                if self.__transition:
                    self.__transition = self.__ui.draw_screen_transition(Configs.get('WIN_SIZE_W')+100)
                else:
                    if not self.__ui.draw_enter_animation(self.__player):
                        if not self.__skill_animating:
                            self.__gui = True
                    self.combat_scene()
                    if self.__player_turn:
                        self.animate_player_skill()
                    else:
                        self.animate_monster_skill()
                         
            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
