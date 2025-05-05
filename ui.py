import pygame as pg
from config import Configs

class AllUI:
    def __init__(self, screen):
        self.__font = pg.font.Font(None, 30)
        self.__screen = screen
        self.__prep_size = 0
        self.curtain = 0 

        self.pstate = "forward"
        self.mstate = "forward"
        self.p_pos = None
        self.m_pos = None
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

    # Done
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

    # Done
    def draw_enter_animation(self, player):
        if player.x != 540:
            player.x -= 10
            return True
        return False

    def draw_walk_out(self, player):
        if player.x > 0:
            player.x -= 10
            return False
        return True
    # Done
    def draw_screen_transition(self, range):
        if self.curtain < range:
            pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, self.curtain, 600))
            self.curtain += 20
            return False
        else:
            self.curtain = 0
            return True

    # Done
    def draw_attack(self, player):
        if self.p_pos is None:
            self.p_pos = player.x
            self.pstate = "forward"

        if self.pstate == "forward":
            player.x -= self.speed
            if player.x <= 310:
                self.pstate = "backward"

        elif self.pstate == "backward":
            player.x += self.speed
            if player.x >= self.p_pos:
                player.x = self.p_pos
                self.pstate = "idle"
                self.p_pos = None
                return False
        return True
    
    # Done
    def draw_monster_attack(self, player, monster):
        if self.m_pos is None:
            self.m_pos = monster.x
            self.mstate = "forward"

        if self.mstate == "forward":
            monster.x += self.speed
            if monster.x >= player.x - 150:
                self.mstate = "backward"

        elif self.mstate == "backward":
            monster.x -= self.speed
            if monster.x <= self.m_pos:
                monster.x = self.m_pos
                self.mstate = "idle"
                self.m_pos = None
                return False
        return True
    
    def draw_monster_flee(self, player, monster):
        if monster.x > -50:
            monster.x -= 10
            return True
        return False

    def draw_damage(self, turn, player, monster, evade=None):
        font = pg.font.SysFont(None, 48)
        x = Configs.monster_ui(monster.name)[0]
        y = Configs.monster_ui(monster.name)[1]
        if turn == "player":
            if evade:
                text1 = font.render(f"MISS", True, Configs.get("BLACK"))
                text2 = font.render(f"MISS", True, Configs.get("WHITE"))
            else:
                text1 = font.render(f"{player.damage}", True, Configs.get("BLACK"))
                text2 = font.render(f"{player.damage}", True, Configs.get("WHITE"))
            rect1 = text1.get_rect(bottomright=(x, y))
            rect2 = text2.get_rect(bottomright=(x+4, y))
        else:
            if evade:
                text1 = font.render(f"MISS", True, Configs.get("BLACK"))
                text2 = font.render(f"MISS", True, Configs.get("WHITE"))
            else:
                text1 = font.render(f"{monster.damage}", True, Configs.get("BLACK"))
                text2 = font.render(f"{monster.damage}", True, Configs.get("WHITE"))
            rect1 = text1.get_rect(center=(player.x+35, player.y-10))
            rect2 = text2.get_rect(center=(player.x+39, player.y-10))

        self.__screen.blit(text1, rect1)
        self.__screen.blit(text2, rect2)

    def draw_summary(self, drops):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, 800, 90), 5)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (3, 3, 794, 84))

        text1 = self.__font.render(f"You earned {drops[0]} coins", True, Configs.get("BLACK"))
        text2 = self.__font.render(f"You earned {drops[1]} exp", True, Configs.get("BLACK"))
        text3 = self.__font.render(f"Press \"SPACE\" to continue", True, Configs.get("BLACK"))
        rect1 = text1.get_rect(center=(420, 25))
        rect2 = text2.get_rect(center=(420, 50))
        rect3 = text3.get_rect(center=(420, 75))
        self.__screen.blit(text1, rect1)
        self.__screen.blit(text2, rect2)
        self.__screen.blit(text3, rect3)

    def draw_health_bar(self, player):
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (600, 375, self.btn_width, self.btn_height), 5)
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (603, 378, self.btn_width-6, self.btn_height-6))
        health_text = self.__font.render(f"Health: {player.health}/{player.max_health}", True, Configs.get("RED"))
        health_rect = health_text.get_rect(center=(700, 412.5))

        self.__screen.blit(health_text, health_rect)
    
    # Done
    def draw_mob_skill_display(self, message=None):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, 800, 50), 5)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (3, 3, 794, 44))
        text = self.__font.render(message, True, Configs.get("BLACK"))
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

    def draw_shop(self):
        rect = pg.Rect(0, 800, 0, 600)
        pg.draw.rect(self.__screen, Configs.get('BLACK'), rect)

        atk_text = self.__font.render("Attack (Z)", True, Configs.get("WHITE"))
        atk_rect = atk_text.get_rect(center=(100, 487.5))
        self.__screen.blit(atk_text, atk_rect)
