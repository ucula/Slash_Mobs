from player import Player
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

        self.__ui = AllUI(self.__screen)
        self.__shopee = Shop(self.__screen)
        self.__hostile_areas = ["PLAIN", "DESERT", "SNOW", "CAVE"]
        self.__mob_rate = {"PLAIN": [0.4, 0.3, 0.4],
                           "DESERT": [0.4, 0.3, 0.3],
                           "SNOW": [0.3, 0.4, 0.3],
                           "CAVE": [0, 1, 0]}
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
        
        self.__scene_manager = "NORMAL"
        # Normal scene
        self.__before = None

        # self.__scene = "HALL"
        # self.__scene = "SHOP"
        # self.__scene = "PLAIN"
        # self.__scene = "DESERT"
        self.__scene = "SNOW"
        # self.__scene = "CAVE"

        self.__enter_scene = False
        self.__enable_walk = True
        self.__shop = False
        self.__status = False
        self.__help = True

        # for Shop
        self.potion_count = 0
        self.hipotion_count = 0
        self.xpotion_count = 0
        self.battledrum_count = 0
        self.greedbag_count = 0
        self.bomb_count = 0
        self.__just_buy = False

        # for check combat status
        self.__engage_ready = False
        self.__combat = False
        self.__move_combat = True
        self.__move_normal = False

        # for player
        self.__player_turn = False
        self.__pstate = "IDLE"
        self.__pselect = None
        self.__up = False
        self.__health = False
        self.__revert_stat = False
        self.__already_save = False

        # for monster
        self.__mob_turn = False
        self.__mstate = "IDLE"
        self.__mob_select = None
        self.__evade = None
        self.__already_place_mob = False
        self.__is_skill_animating = False
        
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
        self.__player.direction = 'DOWN'
        self.__player.steal_count = 0
        self.__already_save = False
        self.__player.run_lock = False
        self.__player.return_stats(evade=True, damage=True)
   
    # Delays
    def delay(self, limit):
        current_time = pg.time.get_ticks()
        if not self.__time_lock:
            self.__start_time = pg.time.get_ticks()
            self.__time_lock = True
        if current_time - self.__start_time >= limit:
            return False
        return True
    # Done
    def character_animate(self, scene):
        self.__player.borders[scene]()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.__move_normal = True
            self.__player.direction = "UP"
            self.__player.y -= self.__player.speed  
        elif keys[pg.K_s]:
            self.__move_normal = True
            self.__player.direction = "DOWN"
            self.__player.y += self.__player.speed
        elif keys[pg.K_a]:
            self.__move_normal = True
            self.__player.direction = "LEFT"
            self.__player.x -= self.__player.speed
        elif keys[pg.K_d]:
            self.__move_normal = True
            self.__player.direction = "RIGHT"
            self.__player.x += self.__player.speed
        else:
            self.__move_normal = False
        
        if not self.__move_normal:
            self.__player.draw_idle()
        elif self.__move_normal:
            self.__player.draw_walk()

    # Done
    def check_scene_change(self, scene):
        if scene == "HALL":
            if self.__player.y > 600: 
                self.__mobs = None
                self.__before = scene
                self.__scene = "PLAIN"
                return True
            
        elif scene == "PLAIN":
            if self.__player.y < 100:
                self.__mobs = None
                self.__before = scene
                self.__scene = "HALL"
                return True    
            elif self.__player.x > 750:
                self.__mobs = None
                self.__before = scene
                self.__scene = "SHOP"
                return True
            elif self.__player.x < 0:
                self.__mobs = None
                self.__before = scene
                self.__scene = "DESERT"
                return True
            
        elif scene == "SHOP":
            if self.__player.y > 600:
                self.__mobs = None
                self.__before = scene
                self.__scene = "PLAIN"
                return True
            
        elif scene == "DESERT":
            if self.__player.x > 750:
                self.__mobs = None
                self.__before = scene
                self.__scene = "PLAIN"
                return True
            elif self.__player.x < 0:
                self.__mobs = None
                self.__before = scene
                self.__scene = "SNOW"
                return True
            
        elif scene == "SNOW":
            if self.__player.x > 750:
                self.__mobs = None
                self.__before = scene
                self.__scene = "DESERT"
                return True
            elif self.__player.y < 100:
                self.__mobs = None
                self.__before = scene
                self.__scene = "CAVE"
                return True
        
        elif scene == "CAVE":
            if self.__player.y > 580:
                self.__mobs = None
                self.__before = scene
                self.__scene = "SNOW"
                return True

    # Done
    def start_point(self, scene=None, before=None, combat=None):
        if self.__enter_scene:
            # Hall
            if scene == "HALL":
                self.__player.x = 366
                self.__player.y = 460
            # Plain
            if scene == "PLAIN":
                if before == "HALL":
                    self.__player.x = 500
                    self.__player.y = 150
                elif before == "SHOP":
                    self.__player.x = 750
                    self.__player.y = 300
                elif before == "DESERT":
                    self.__player.x = 50
                    self.__player.y = 300
                else:
                    self.__player.x = 400
                    self.__player.y = 300
            # Shop
            if scene == "SHOP":
                self.__player.x = 350
                self.__player.y = 550
            # Desert
            if scene == "DESERT":
                if before == "PLAIN":
                    self.__player.x = 700
                    self.__player.y = 375
                elif before == "SNOW":
                    self.__player.x = 50
                    self.__player.y = 375
                else:
                    self.__player.x = 400
                    self.__player.y = 500
            # Snow
            if scene == "SNOW":
                if before == "DESERT":
                    self.__player.x = 700
                    self.__player.y = 375
                elif before == "CAVE":
                    self.__player.x = 400
                    self.__player.y = 150
                else:
                    self.__player.x = 400
                    self.__player.y = 300
            # Cave
            if scene == "CAVE":
                self.__player.x = 400
                self.__player.y = 500
                
            # Combat
            if combat is not None:
                self.__player.x = 800
                self.__player.y = 300
        self.__enter_scene = False

    # Done
    def gen_cords(self):
        if self.__scene == "PLAIN":
            x = random.randint(80, 550)
            y = random.randint(190, 250)
        elif self.__scene == "DESERT":
            x = random.randint(80, 550)
            y = random.randint(280, 300)
        elif self.__scene == "SNOW":
            x = random.randint(80, 550)
            y = random.randint(280, 300)
        elif self.__scene == "CAVE":
            x = random.randint(80, 550)
            y = random.randint(350, 440)
        return x, y
    
    # Done
    def random_mob(self):
        if self.__scene == "PLAIN":
            mob_set = monster.Monster_TMP.monster1
        elif self.__scene == "DESERT":
            mob_set = monster.Monster_TMP.monster2
        elif self.__scene == "SNOW":
            mob_set = monster.Monster_TMP.monster3
        elif self.__scene == "CAVE":
            mob_set = monster.Monster_TMP.monster4

        select = random.choices(mob_set, self.__mob_rate[self.__scene])[0]
        pos_x, pos_y = self.gen_cords()
        # print("call")
        offsetx = Configs.monster_offsets(select)[0]
        offsety = Configs.monster_offsets(select)[1]
        if select == "SLIME":
            tmp_mob = monster.Slime(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "GOBLIN":
            tmp_mob = monster.Goblin(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "DARK":
            tmp_mob = monster.Dark_Goblin(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "VAMPIRE1":
            tmp_mob = monster.Vampire1(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "VAMPIRE2":
            tmp_mob = monster.Vampire2(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "VAMPIRE3":
            tmp_mob = monster.Vampire3(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "MINOTAUR1":
            tmp_mob = monster.Minotaur1(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "MINOTAUR2":
            tmp_mob = monster.Minotaur2(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "MINOTAUR3":
            tmp_mob = monster.Minotaur3(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "BLUE":
            tmp_mob = monster.Blue_worm(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "PURPLE":
            tmp_mob = monster.Purple_worm(self.__screen, offsetx, offsety, pos_x, pos_y)
        elif select == "SCORPION":
            tmp_mob = monster.Scorpion(self.__screen, offsetx, offsety, pos_x, pos_y)
        return tmp_mob  
    
    # Done
    def create_mob(self):
        if self.__scene in self.__hostile_areas and self.__mobs is None:
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
        if not self.__is_skill_animating:
            self.__mobs.draw_monster()
            self.__screen.blit(self.__mobs.animation[self.__mobs.frame], (self.__mobs.x, self.__mobs.y))

    # Non-combat
    def normal_scene(self):
        self.__player.save()
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
                if self.__mobs.in_range(self.__player):
                    self.__engage_ready = True
                else:
                    self.__engage_ready = False
        if self.__just_buy:
            self.__player.weapon.up_stats(self.__player)
            self.__just_buy = False

        # Status window
        if self.__status:   
            self.__ui.draw_status_window(self.__player)
        
        # tips for shop scene
        if self.__help:
            if self.__scene == "SHOP":
                self.__ui.draw_help(shop=True)
                # Shop menu
                if self.__shop:
                    self.__shopee.draw_menu(self.__player)
            else:
                self.__ui.draw_help()

    # Simple walk-in intro when combat triggered
    def enter_stage(self):
        if self.__enter_combat:
            if not self.__player.draw_enter_animation():
                self.__player_turn = True
                self.__pstate = "IDLE"
                self.__enter_combat = False
                self.__health = True
                self.__move_combat = False

    # Random skill for mobs based on fixed probability
    def m_pick_skill(self):
        if self.__mob_select is None:
            self.__mob_select = random.choices(list(self.__mobs.skill_chances.keys()), list(self.__mobs.skill_chances.values()))[0]

    # Display what skill mob chose to attack  player
    def m_show_skill(self):
        if not self.delay(self.__mob_delay):
            self.__mstate = "ATTACKING"
            self.__ui.start_pos = None
            self.__time_lock = False
        else:
            self.__ui.draw_skill_display(self.__mob_select)

    # Animate any player's skill
    def p_action(self):
        if self.__pselect != "DEFEND":
            self.__move_combat = True
        animating = self.__player.attacks[self.__pselect](self.__mobs)
        if not animating:
            self.move = False
            if self.__pselect == "RUN":
                self.reset()
            elif self.__pselect == "DEFEND":
                self.__pstate = "CHANGE_TURN"
            elif self.__pselect != "RUN":
                self.__pstate = "CALCULATING"
                self.__evade = self.__mobs.roll_evasion()

    def m_action(self):
        animating = self.__mobs.skill[self.__mob_select](self.__player)
        self.__is_skill_animating = self.__mobs.bool_tmp
        if not animating:
            if self.__mob_select == "RUN":
                self.reset()
                self.__move_combat = True
            elif self.__mob_select != "RUN":
                self.__mstate = "CALCULATING"
                self.__evade = self.__player.roll_evasion()   

    def p_calculate_stage(self):
        self.__move_combat = False
        if self.__pselect == "STEAL":
            item = self.__player.tmp
            self.__ui.draw_skill_display(f"Stole {item}!")             
            if not self.delay(1500):
                self.manage_item(name=item)
                self.__pstate = "CHANGE_TURN"

        elif self.__pselect != "STEAL":
            if self.__player.is_damage:
                self.__ui.draw_damage("player", self.__player, self.__mobs, self.__evade)

            if not self.delay(self.__turn_delay):
                if not self.__evade and self.__player.is_damage:
                    self.__mobs.health -= self.__player.atk_tmp
                self.__pstate = "CHANGE_TURN"

    def m_calculate_stage(self):
        if self.__mobs.is_damage:
            self.__ui.draw_damage("mob", self.__player, self.__mobs, self.__evade)
            
        if not self.delay(self.__turn_delay):
            if not self.__evade and self.__mobs.is_damage:
                self.__player.health -= self.__mobs.atk_tmp

            if self.__mobs.state == "HASTE" and self.__mobs.action_count < 1:
                # print(self.__mobs.turn_count)
                self.__mob_select = None
                self.__mstate = "IDLE"
                self.__mobs.action_count += 1
                self.__time_lock = False
                if self.__mobs.turn_count >= 4:
                    self.__mobs.return_stats(haste=True)
                    self.__mobs.turn_count = 0
            else:
                self.__mobs.action_count = 0
                self.__mobs.turn_count += 1
                self.__mstate = "CHANGE_TURN"
    
    def p_change_turn(self):
        self.__player.is_damage = False
        self.__player_turn = False
        self.__mob_turn = True
        self.__time_lock = False
        self.__pstate = "IDLE"
        if self.__mobs.health <= 0:
            self.__pstate = "SUMMARY"
            self.__mob_drops = (self.__mobs.coin, self.__mobs.exp)
            self.__mobs = None
            self.__mob_turn = False
            self.__player_turn = True
            self.__player.coin += self.__mob_drops[0]
            self.__player.exp += self.__mob_drops[1]
            self.__up = self.__player.level_up()
    
    def m_change_turn(self):
        self.__mobs.is_damage = False
        self.__mstate = "IDLE"
        self.__mob_select = None
        self.__time_lock = False
        self.__player_turn = True
        self.__mob_turn = False
        if self.__revert_stat:
            self.__player.return_stats(evade=True)
            self.__revert_stat = False
        if self.__player.health <= 0:
            self.reset()
            self.__player.reset_stats()
            self.__pstate = None
            self.__scene = "HALL"
            self.__before = None
            self.__enter_scene = True

    def summary(self):
        if not self.delay(self.__turn_delay):
            self.__ui.draw_summary(self.__mob_drops, self.__player, self.__up)
            self.__health = False
    
    def ending(self):
        self.__move_combat = True
        self.__up = False
        walk_out = self.__player.draw_walk_out()
        if walk_out:
            self.__player.return_stats(evade=True, damage=True)
            self.reset()
    
    # 3.Combat scene
    def combat_scene(self):
        if not self.__already_save:
            # print(self.__player.save_stats)
            self.__player.save()
            self.__already_save = True
        self.start_point(combat=1)
        bg = self.__ui.draw_bg(self.__scene)
        self.__screen.blit(bg, (0, 0))
        if self.__mobs is not None:
            self.create_mob_incombat()
        # Enter animation
        self.enter_stage()

        # Some certain skills require player to move
        if self.__move_combat:
            self.__player.draw_walk_in_combat()
        else:
            self.__player.draw_idle_in_combat()
    
        # Player's turn
        if self.__player_turn:
            if self.__pstate == "IDLE":
                self.__ui.draw_gui_combat(self.__player)

            elif self.__pstate == "ATTACKING":
                self.p_action()

            elif self.__pstate == "CALCULATING":
                self.p_calculate_stage()

            elif self.__pstate == "CHANGE_TURN":
                self.p_change_turn()
                    
            elif self.__pstate == "SUMMARY":
                self.summary()

            elif self.__pstate == "ENDING":
                self.ending()
        
        # Mob's turn
        if self.__mob_turn:
            # Mob pick skill
            self.m_pick_skill()

            # Mob stages
            if self.__mstate == "IDLE":
                self.m_show_skill()
                    
            elif self.__mstate == "ATTACKING":
                self.m_action()
                print(self.__player.run_lock)

            elif self.__mstate == "CALCULATING":
                self.m_calculate_stage()
                # print(self.__player.run_lock)

            elif self.__mstate == "CHANGE_TURN":
                # print(self.__player.run_lock)
                self.m_change_turn()
                print(self.__player.run_lock)

        # Show healh bar for player in combat
        if self.__health:
            self.__ui.draw_health_bar(self.__player)
        
        # print(self.__mobs.skill_chances)
    def manage_item(self, item=None, name=None):
        if name is None:
            name = item.name

        if name == "Potion":
            self.potion_count += 1
        elif name == "Hi_Potion":
            self.hipotion_count += 1
        elif name == "X-Potion":
            self.xpotion_count += 1
        elif name == "Drum":
            self.battledrum_count += 1
        elif name == "Loot bag":
            self.greedbag_count += 1
        elif name == "Bomb":
            self.bomb_count += 1
    
    def open_shop(self):
        self.__shop = True
        self.__enable_walk = False

    def close_shop(self):
        self.__shop = False
        self.__enable_walk = True

    # Check action for every scenarios
    def user_event(self):
        event = pg.event.get()
        for e in event:
            if (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE) or e.type == pg.QUIT:
                self.__running = False
            
            # Status window
            if self.__scene_manager == "NORMAL" and self.__enable_walk and not self.__shop:
                if e.type == pg.KEYDOWN and e.key == pg.K_i:
                    self.__status = True
                    self.__enable_walk = False
            elif self.__scene_manager == "NORMAL" and not self.__enable_walk and not self.__shop:
                if e.type == pg.KEYDOWN and e.key == pg.K_i:
                    self.__status = False
                    self.__enable_walk = True

            # Shop menu
            if self.__scene == "SHOP":
                # On-off shop switches
                if self.__enable_walk:
                    if e.type == pg.KEYDOWN and e.key == pg.K_e and not self.__status:
                        self.open_shop()

                elif not self.__enable_walk and not self.__status:
                    if e.type == pg.KEYDOWN and e.key == pg.K_e:
                        self.close_shop()

                # Buy item
                if self.__shop and e.type == pg.KEYDOWN:
                    if e.key in (pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9):
                        item, type = self.__shopee.buy(self.__player, e.key) 
                        if type == "weapon":
                            if self.__player.weapon is not None:
                                self.__player.weapon.return_stats(self.__player)
                            self.__player.weapon = item
                            self.__just_buy = True
                            self.close_shop()

                        elif item is not None and type is not None:
                            self.manage_item(item)

            # Ready up
            if self.__engage_ready:
                if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                    self.__combat = True
                    self.__enter_scene = True
                    self.__engage_ready = False
                    self.__help = False
                    self.__scene_manager = "CHANGING"

            # Player skill checker
            if self.__player_turn and self.__pstate == "IDLE":
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_z:
                        self.__pselect = "ATTACK"
                        self.__pstate = "ATTACKING"
                    elif e.key == pg.K_r and not self.__player.run_lock:
                        self.__pselect = "RUN"
                        self.__pstate = "ATTACKING"
                    elif e.key == pg.K_d:
                        self.__pselect = "DEFEND"
                        self.__revert_stat = True
                        self.__pstate = "ATTACKING"
                    elif self.__player.skill1_unlock and self.__player.steal_count < 2 and e.key == pg.K_x:
                        self.__pselect = "STEAL"
                        self.__player.steal_count += 1
                        self.__pstate = "ATTACKING"
                    elif self.__player.skill2_unlock and e.key == pg.K_c:
                        self.__pselect = "FIRE"
                        self.__pstate = "ATTACKING"
                    elif self.__player.skill1_unlock and e.key == pg.K_v:
                        self.__pselect = "THUNDER"
                        self.__pstate = "ATTACKING"
                    elif self.__player.skill1_unlock and e.key == pg.K_b:
                        self.__pselect = "INSTINCT"
                        self.__pstate = "ATTACKING"
                        self.__revert_stat = True
                        
            if self.__pstate == "SUMMARY" :
                if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                    self.__pstate = "ENDING"
    
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
                    self.__before = None

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
