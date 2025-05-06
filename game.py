from player import Player
from weapon import Weapons
import monster
from ui import AllUI
from config import Configs
from shop import Shop
import pygame as pg
import random

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Slash Mobs!")
        self.__screen = pg.display.set_mode((Configs.get('WIN_SIZE_W'), Configs.get('WIN_SIZE_H')))
        self.__clock = pg.time.Clock()

        self.__player = Player(self.__screen, name="Ucula")
        # self.__weapon = Weapons()
        self.__ui = AllUI(self.__screen)
        self.__shopee = Shop(self.__screen)
        self.__rand_mob = monster.Monster_TMP.monster
        self.__hostile_areas = ["PLAIN"]
        self.__mob_rate = {"PLAIN": [0.4, 0.3, 0.3]}
        self.__mobs = None

        # for main loop
        self.__running = True
        
        # delay switches
        self.__start_time = 0
        self.__time_lock = False
        self.__mob_delay = 1000
        self.__turn_delay = 800

        # cut scene switch
        self.__enter_combat = True

        # Player animation in non-combat (DONE)
        self.__walk = "IDLE"
        self.__walk_direction = {'IDLE': self.__player.draw_idle,
                               'LEFT': self.__player.draw_walk_left,
                               'RIGHT': self.__player.draw_walk_right ,
                               'UP': self.__player.draw_walk_up ,
                               'DOWN': self.__player.draw_walk_down}
        
        self.__scene_manager = "NORMAL"
        # Normal scene
        self.__before = None
        self.__scene = 'HALL'
        self.__enter_scene = False
        self.__enable_walk = True
        self.__shop = False
        self.__status = False
        self.__help = True

        # for check combat status
        self.__engage_ready = False
        self.__combat = False
        self.__move = True

        # for player
        self.__up = False
        self.__health = False
        self.__pstate = "IDLE"
        self.__player_turn = False
        self.__pskill = {"ATTACK": self.__ui.draw_attack}

        # for monster
        self.__mstate = "IDLE"
        self.__mob_turn = False
        self.__mob_select = None
        self.__evade = None
        self.__already_place_mob = False
        
    # Reset Combat
    def reset(self):
        self.__combat = False
        self.__mobs = None
        self.__mob_turn = False
        self.__mob_select = None
        self.__player_turn = False
        self.__health = False
        self.__enter_scene = True
        self.__engage_ready = False
        
        self.__already_place_mob = False
        self.__time_lock = False
        self.__pstate = "IDLE"
        self.__mstate = "IDLE"
        self.__enter_combat = True
        self.__scene_manager = "CHANGING"
        self.__help = True

    # Delays
    def delay(self, limit):
        current_time = pg.time.get_ticks()
        if not self.__time_lock:
            self.__start_time = pg.time.get_ticks()
            self.__time_lock = True
        if current_time - self.__start_time >= limit:
            return False
        return True
    
    def character_animate(self, scene):
        self.__player.borders[scene]()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            # self.__walk = "UP"
            self.__player.draw_walk_up()
            self.__player.y -= self.__player.speed  
            self.__screen.blit(self.__player.animation_up[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_s]:
            # self.__walk = "DOWN"
            self.__player.draw_walk_down()
            self.__player.y += self.__player.speed
            self.__screen.blit(self.__player.animation_down[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_a]:
            # self.__walk = "LEFT"
            self.__player.draw_walk_left()
            self.__player.x -= self.__player.speed
            self.__screen.blit(self.__player.animation_left[self.__player.frame], (self.__player.x, self.__player.y))
        elif keys[pg.K_d]:
            # self.__walk = "RIGHT"
            self.__player.draw_walk_right()
            self.__player.x += self.__player.speed
            self.__screen.blit(self.__player.animation_right[self.__player.frame], (self.__player.x, self.__player.y))
        else:
              self.__screen.blit(self.__walk_direction["IDLE"]() , (self.__player.x, self.__player.y))    
    
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
            
        if scene not in self.__hostile_areas:
            self.__mobs = None
        
    def start_point(self, scene=None, before=None, combat=None):
        if self.__enter_scene:
            if scene == "HALL":
                self.__player.x = 390
                self.__player.y = 550
            if scene == "PLAIN" and before == "HALL":
                self.__player.x = 500
                self.__player.y = 150
            elif scene == "PLAIN" and before == "SHOP": 
                self.__player.x = 750
                self.__player.y = 300
            if scene == "SHOP":
                self.__player.x = 350
                self.__player.y = 550
            if combat is not None:
                self.__player.x = 800
                self.__player.y = 300
        self.__enter_scene = False
    
    def gen_cords(self):
        if self.__scene == "PLAIN":
            x = random.randint(80, 550)
            y = random.randint(190, 250)
        else:
            # x = random.randint(0,Configs.get('WIN_SIZE_W'))
            # y = random.randint(0,Configs.get('WIN_SIZE_H'))
            pass
        return x, y

    # Done
    def random_mob(self):
        select = random.choices(self.__rand_mob, self.__mob_rate[self.__scene])[0]
        pos_x, pos_y = self.gen_cords()
        if select == "SLIME":
            tmp_mob = monster.Slime(self.__screen, Configs.monster_offsets(select)[0], Configs.monster_offsets(select)[1], pos_x, pos_y)
        elif select == "GOBLIN":
            tmp_mob = monster.Goblin(self.__screen, Configs.monster_offsets(select)[0], Configs.monster_offsets(select)[1], pos_x, pos_y)
        elif select == "DARK":
            tmp_mob = monster.Dark_Goblin(self.__screen, Configs.monster_offsets(select)[0], Configs.monster_offsets(select)[1], pos_x, pos_y)
        else:
            pass
        return tmp_mob
    
    # Done
    def create_mob(self):
        if self.__mobs is None:
            self.__mobs = self.random_mob()

        self.__mobs.draw_monster()
        self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))

    # Done
    def create_mob_incombat(self):
        if not self.__already_place_mob:
            x = Configs.monster_combat(self.__mobs.name)[0]
            y = Configs.monster_combat(self.__mobs.name)[1]
            self.__mobs.x = x
            self.__mobs.y = y
            self.__already_place_mob = True
        self.__mobs.draw_monster()
        self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))

    # Non-combat
    def normal_scene(self):
        """
        TODO
        ทำให้ shop ติด
        """
        # BG
        bg = self.__ui.draw_bg(self.__scene)
        self.__screen.blit(bg, (0, 0))
        self.start_point(self.__scene, self.__before)

        if self.__enable_walk:
            self.character_animate(self.__scene)

        if self.check_scene_change(self.__scene):
            self.__enter_scene = True  
            self.__scene_manager = "CHANGING"
        
        if not self.__scene_manager == "CHANGING":
            if self.__scene in self.__hostile_areas: 
                self.create_mob()
                if self.__mobs.in_range(self.__player, self.__mobs):
                    self.__engage_ready = True
                else:
                    self.__engage_ready = False
        
        if self.__shop:
            self.__shopee.draw_menu()

        if self.__status:   
            self.__ui.draw_status_window(self.__player)
        
        if self.__help:
            if self.__scene == "SHOP":
                self.__ui.draw_help(shop=True)
            else:
                self.__ui.draw_help()

    def user_event(self):
        event = pg.event.get()
        for e in event:
            if (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE) or e.type == pg.QUIT:
                self.__running = False
            
            if self.__scene == "SHOP" and self.__enable_walk:
                if e.type == pg.KEYDOWN and e.key == pg.K_e and not self.__status:
                    self.__shop = True
                    self.__enable_walk = False
            elif self.__scene == "SHOP" and not self.__enable_walk and not self.__status:
                if e.type == pg.KEYDOWN and e.key == pg.K_e:
                    self.__shop = False
                    self.__enable_walk = True

            # Ready up
            if self.__engage_ready:
                if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                    self.__combat = True
                    self.__enter_scene = True
                    self.__engage_ready = False
                    self.__help = False
                    self.__scene_manager = "CHANGING"

            # Check for skill trigger
            if self.__player_turn and self.__pstate == "IDLE":
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_z:
                        self.__pstate = "ATTACK"
                    elif e.key == pg.K_r:
                        self.__pstate = "RUN"
            
            if self.__pstate == "SUMMARY" :
                if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                    self.__pstate = "ENDING"

            # Status window
            if self.__scene_manager == "NORMAL" and self.__enable_walk and not self.__shop:
                if e.type == pg.KEYDOWN and e.key == pg.K_i:
                    self.__status = True
                    self.__enable_walk = False
            elif self.__scene_manager == "NORMAL" and not self.__enable_walk and not self.__shop:
                if e.type == pg.KEYDOWN and e.key == pg.K_i:
                    self.__status = False
                    self.__enable_walk = True

    # 3.Combat scene
    def combat_scene(self):
        self.start_point(combat=1)
        bg = self.__ui.draw_bg(self.__scene)
        self.__screen.blit(bg, (0, 0))
        if self.__mobs is not None:
            self.create_mob_incombat()
    
        # Enter animation
        if self.__enter_combat:
            if not self.__ui.draw_enter_animation(self.__player):
                self.__player_turn = True
                self.__pstate = "IDLE"
                self.__enter_combat = False
                self.__health = True
                self.__move = False

        # Player's turn
        if self.__player_turn:
            if self.__pstate == "IDLE":
                self.__ui.draw_gui_combat()

            elif self.__pstate == "RUN":
                self.__move = True
                self.reset()

            elif self.__pstate == "CALCULATING":
                self.__move = False
                # if self.__mobs.attack_skill: 
                self.__ui.draw_damage("player", self.__player, self.__mobs, self.__evade)
                if not self.delay(self.__turn_delay):
                    self.__pstate = "CHANGE_TURN"

            elif self.__pstate == "CHANGE_TURN":
                self.__player_turn = False
                self.__mob_turn = True
                if not self.__evade:
                    self.__mobs.health -= self.__player.damage
                self.__pstate = "IDLE"
                self.__time_lock = False
                if self.__mobs.health <= 0:
                    self.__pstate = "SUMMARY"
                    self.__mob_drops = (self.__mobs.coin, self.__mobs.exp)
                    self.__mobs = None
                    self.__mob_turn = False
                    self.__player_turn = True
                    self.__player.coin += self.__mob_drops[0]
                    self.__player.exp += self.__mob_drops[1]
                    self.__up = self.__player.level_up()
                    # print(self.__up)
                    
            elif self.__pstate == "SUMMARY":
                if not self.delay(self.__turn_delay):
                    self.__ui.draw_summary(self.__mob_drops, self.__player, self.__up)
                    self.__health = False

            elif self.__pstate == "ENDING":
                self.__move = True
                self.__up = False
                walk_out = self.__ui.draw_walk_out(self.__player)
                if walk_out:
                    self.reset()
    
            else:
                self.__move = True
                animating = self.__pskill[self.__pstate](self.__player)
                if not animating:
                    self.__pstate = "CALCULATING"
                    self.__evade = self.__mobs.roll_evasion()
        
        # Mob's turn
        if self.__mob_turn:
            # Mob pick skill
            if self.__mob_select is None:
                self.__mob_select = random.choices(list(self.__mobs.skill.keys()), self.__mobs.skill_chances)[0]

            if self.__mstate == "IDLE":
                if not self.delay(self.__mob_delay):
                    self.__mstate = "ATTACKING"
                    self.__ui.start_pos = None
                    self.__time_lock = False
                else:
                    self.__ui.draw_mob_skill_display(self.__mob_select)
                    
            elif self.__mstate == "ATTACKING":
                animating = self.__mobs.skill[self.__mob_select](self.__player, self.__mobs)
                if not animating and self.__mob_select == "RUN":
                    self.reset()
                    self.__move = True
                
                elif not animating and self.__mob_select == "INSTINCT":
                    self.__mobs.hunter_instinct()
                    self.__mstate = "CALCULATING"

                elif not animating and self.__mob_select != "RUN":
                    self.__mstate = "CALCULATING"
                    self.__evade = self.__player.roll_evasion()

            elif self.__mstate == "CALCULATING":
                if self.__mobs.attack_skill:
                    self.__ui.draw_damage("mob", self.__player, self.__mobs, self.__evade)
                if not self.delay(self.__turn_delay):
                    if not self.__evade and self.__mobs.attack_skill:
                        self.__player.health -= self.__mobs.damage
                    self.__mstate = "CHANGE_TURN"

            elif self.__mstate == "CHANGE_TURN":
                self.__mobs.attack_skill = True
                self.__mstate = "IDLE"
                self.__mob_select = None
                self.__time_lock = False
                self.__player_turn = True
                self.__mob_turn = False
                if self.__player.health <= 0:
                    self.reset()
                    # ตรงนี้ใส่ cutscene สักอย่าง ฉากคืนชีพก้ได้มั้ง
                    self.__pstate = None
                    self.__player.health = 1

        if self.__health:
            self.__ui.draw_health_bar(self.__player)
            """
            TODO
            add check player health = 0, if so kill the player and reset progress/(or smth else)
            """
        if self.__move:
            self.__player.draw_walk_left()
            self.__screen.blit(self.__player.animation_left[self.__player.frame], (self.__player.x, self.__player.y))
        else:
            self.__screen.blit(self.__player.draw_idle_combat(), (self.__player.x, self.__player.y))
    
# Main loop
    def run(self):
        while self.__running:
            self.__clock.tick(Configs.get('FPS'))
            self.user_event()
            # Changing cutscene
            if self.__scene_manager == "CHANGING":
                done = self.__ui.draw_screen_transition(Configs.get('WIN_SIZE_W')+100)
                if done and self.__combat:
                    self.__scene_manager = "COMBAT"

                elif done and not self.__combat:
                    self.__scene_manager = "NORMAL"

            # Normal scene
            if self.__scene_manager == "NORMAL":
                self.normal_scene()
            
            # Combat scene
            if self.__scene_manager == "COMBAT":       
                self.combat_scene()        

            pg.display.update()
        pg.quit

if __name__ == '__main__':
    g1 = Game()
    g1.run()
