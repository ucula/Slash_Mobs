import pygame as pg
from config import Configs

class AllUI:
    def __init__(self, screen):
        self.__font = pg.font.Font(None, 30)
        self.__screen = screen
        self.__prep_size = 0
        self.curtain = 0 

        self.state = "forward"
        self.animate1 = True
        self.animate2 = False
        self.speed = 20
        self.start_pos = None

        self.player_arrow = [(575, 300), (590, 270), (560, 270)]
        self.box_y = 450
        self.box_pos = (0, self.box_y, 800, Configs.get('WIN_SIZE_H') - self.box_y)

        self.btn_border = 2
        self.btn_width = 200
        self.btn_height = 75
        self.btn = [0, 450, self.btn_width, self.btn_height]

    @property
    def prep_size(self):
        return self.__prep_size
    
    @prep_size.setter
    def prep_size(self, val):
        self.__prep_size = val

    def draw_bg(self, scene):
        image = pg.image.load(Configs.background(scene)).convert()
        return image
    
    def draw_mob_info(self, name):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (250, 180, self.prep_size, self.prep_size), width=5, border_radius=10)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (255, 185, self.prep_size-10, self.prep_size-10))
        if self.prep_size != 300:
            self.prep_size += 50
        if self.prep_size == 300:
            text1 = self.__font.render("Monster info: bla bla", True, Configs.get("BLACK"))
            text1_rect = text1.get_rect(center=(400, 300))

            text2 = self.__font.render("Press SPACE to fight", True, Configs.get("BLACK"))
            text2_rect = text1.get_rect(center=(400, 350))

            self.__screen.blit(text1, text1_rect)
            self.__screen.blit(text2, text2_rect)

    def draw_enter_animation(self, player):
        if player.x != 540:
            player.x -= 10
            # print("entering")
            return True
        return False

    def draw_screen_transition(self, range):
        if self.curtain < range:
            pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, self.curtain, 600))
            self.curtain += 20
            return True
        else:
            self.curtain = 0
            return False

    def draw_attack(self, player):
        if self.animate1:
            player.x -= self.speed
            if player.x == 310:
                self.animate1 = False
                self.animate2 = True
        elif self.animate2:
            player.x += self.speed
            if player.x == 540:
                self.animate2 = False
        
        elif self.animate1 == False and self.animate2 == False:
            return False
        return True
    
    def draw_monster_attack(self, player, monster):
        if self.start_pos is None:
            self.start_pos = monster.x
            self.state = "forward"

        if self.state == "forward":
            monster.x += self.speed
            if monster.x >= player.x - 150:
                self.state = "backward"

        elif self.state == "backward":
            monster.x -= self.speed
            if monster.x <= self.start_pos:
                monster.x = self.start_pos
                self.state = "idle"
                self.start_pos = None
                return False

        return True
            
        # if self.animate1:
        #     monster.x += self.attack_speed
        #     if monster.x > 400:
        #         self.animate1 = False
        #         self.animate2 = True
        # elif self.animate2:
        #     monster.x -= 20
        #     if monster.x < self.start_pos:
        #         self.animate2 = False
        #         monster.x = self.start_pos
        
        # elif self.animate1 == False and self.animate2 == False:
        #     return False
        # return True
    
    def draw_game_over(self):
        pass

    def draw_start(self):
        pass

    def draw_tutorial(self):
        pass

    def draw_status(self):
        pass
    
    # Done
    def draw_mob_skill_display(self, message=None):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, 800, 50), 5)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (3, 3, 794, 44))
        text = self.__font.render("ATTACK", True, Configs.get("BLACK"))
        rect = text.get_rect(center=(420, 25))
        self.__screen.blit(text, rect)

    # Done
    def draw_gui_combat(self):
        pg.draw.polygon(self.__screen, Configs.get('GREEN'), self.player_arrow)
        pg.draw.rect(self.__screen, Configs.get('BLACK'), self.box_pos)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (0, 450, self.btn_width, self.btn_height), self.btn_border)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (200, 450, self.btn_width, self.btn_height), self.btn_border)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (400, 450, self.btn_width, self.btn_height), self.btn_border)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (600, 450, self.btn_width, self.btn_height), self.btn_border)

        pg.draw.rect(self.__screen, Configs.get('WHITE'), (0, 525, self.btn_width, self.btn_height), self.btn_border)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (200, 525, self.btn_width, self.btn_height), self.btn_border)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (400, 525, self.btn_width, self.btn_height), self.btn_border)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (600, 525, self.btn_width, self.btn_height), self.btn_border)

    
        atk_text = self.__font.render("Attack (Z)", True, Configs.get("WHITE"))
        atk_rect = atk_text.get_rect(center=(100, 487.5))
        self.__screen.blit(atk_text, atk_rect)

        atk_text = self.__font.render("Run (R)", True, Configs.get("WHITE"))
        atk_rect = atk_text.get_rect(center=(300, 487.5))
        self.__screen.blit(atk_text, atk_rect)

       