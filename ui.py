import pygame as pg
from config import Configs

class AllUI:
    def __init__(self, screen):
        self.__font = pg.font.Font(None, 30)
        self.__screen = screen
        self.curtain = 0 

        self.start_time = 0
        self.time_lock = False
        self.display_delay = 1000

        self.pstate = "forward"
        self.mstate = "forward"
        self.p_pos = None
        self.m_pos = None
        self.speed = 20
        self.start_pos = None

        self.player_arrow = [(575, 300), (590, 270), (560, 270)]
        self.box_y = 450
        self.box_pos = (0, self.box_y, 800, Configs.get('WIN_SIZE_H') - self.box_y)

        self.box_border = 2
        self.box_width = 200
        self.box_height = 75
        self.btn = [0, 450, self.box_width, self.box_height]

    @staticmethod
    def animate_text_center(message, color, x, y):
        font = pg.font.Font(None, 30)
        text = font.render(message, True, Configs.get(color))
        rect = text.get_rect(center=(x, y))
        return text, rect
    
    @staticmethod
    def animate_text_topleft(message, color, x, y):
        font = pg.font.Font(None, 30)
        text = font.render(message, True, Configs.get(color))
        rect = text.get_rect(topleft=(x, y))
        return text, rect

    @staticmethod
    def create_box(screen, settings):
        pg.draw.rect(screen, Configs.get(settings[0]), (settings[2], settings[3], settings[4], settings[5]), settings[7])
        pg.draw.rect(screen, Configs.get(settings[1]), (settings[2]+settings[6], settings[3]+settings[6], settings[4]-2*settings[6], settings[5]-2*settings[6]))

    def delay(self, limit):
        current_time = pg.time.get_ticks()
        if not self.time_lock:
            self.start_time = pg.time.get_ticks()
            self.time_lock = True
        if current_time - self.start_time >= limit:
            return False
        return True

    def draw_bg(self, scene):
        image = pg.image.load(Configs.background(scene)).convert()
        return image

    # Normal scene series
    def draw_help(self, shop=None):
        settings = Configs.ui_pos("HELP")
        AllUI.create_box(self.__screen, settings)
        help_text, help_rect = AllUI.animate_text_topleft(message=f"Press \"I\" to open status", color='BLACK', x=10, y=10)
        shop_text, shop_rect = AllUI.animate_text_topleft(message=f"Press \"E\" to open shop", color='BLACK', x=10, y=30)
        if shop:
            self.__screen.blit(shop_text, shop_rect)
        self.__screen.blit(help_text, help_rect)

    # Cut scene series
    def draw_screen_transition(self, range):
        if self.curtain < range:
            pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, self.curtain, 600))
            self.curtain += 20
            return False
        else:
            self.curtain = 0
            return True

    def draw_damage(self, turn, player, monster, evade=None):
        font = pg.font.SysFont(None, 48)
        x = Configs.monster_damage(monster.name)[0]
        y = Configs.monster_damage(monster.name)[1]
        if turn == "player":
            if evade:
                text1 = font.render(f"MISS", True, Configs.get("BLACK"))
                text2 = font.render(f"MISS", True, Configs.get("RED"))
            else:
                text1 = font.render(f"{player.atk_tmp:.0f}", True, Configs.get("BLACK"))
                text2 = font.render(f"{player.atk_tmp:.0f}", True, Configs.get("RED"))
            rect1 = text1.get_rect(midtop=(x, y))
            rect2 = text2.get_rect(midtop=(x+4, y))
        elif turn == "mob":
            if evade:
                text1 = font.render(f"MISS", True, Configs.get("BLACK"))
                text2 = font.render(f"MISS", True, Configs.get("RED"))
            else:
                text1 = font.render(f"{monster.atk_tmp:.0f}", True, Configs.get("BLACK"))
                text2 = font.render(f"{monster.atk_tmp:.0f}", True, Configs.get("RED"))
            rect1 = text1.get_rect(center=(player.x+35, player.y-10))
            rect2 = text2.get_rect(center=(player.x+39, player.y-10))

        self.__screen.blit(text1, rect1)
        self.__screen.blit(text2, rect2)

    def draw_summary(self, drops, player, up):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, 800, 120), 5)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (3, 3, 794, 114))
        text1, rect1 = AllUI.animate_text_center(f"You earned {drops[0]} coins", "BLACK", 420, 25)
        text2, rect2 = AllUI.animate_text_center(f"You earned {drops[1]} exp", "BLACK", 420, 50)
        text3, rect3 = AllUI.animate_text_center(f"Press \"SPACE\" to continue", "BLACK", 420, 75)
        text4, rect4 = AllUI.animate_text_center(f"{player.name} level up!", "BLACK", 420, 100)

        self.__screen.blit(text1, rect1)
        self.__screen.blit(text2, rect2)
        self.__screen.blit(text3, rect3)
        if up:
            self.__screen.blit(text4, rect4)

    def draw_health_bar(self, player):
        settings = Configs.ui_pos("HEALTH")
        AllUI.create_box(self.__screen, settings)
        health_text, health_rect = AllUI.animate_text_center(f"Health: {player.health:.0f}/{player.max_health:.0f}", "RED", 700, 412.5)     
        self.__screen.blit(health_text, health_rect)

    def draw_skill_display(self, message=None):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, 800, 50), 5)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (3, 3, 794, 44))
        text = self.__font.render(message, True, Configs.get("BLACK"))
        rect = text.get_rect(center=(420, 25))
        self.__screen.blit(text, rect)

    def draw_gui_combat(self, player):
        pg.draw.polygon(self.__screen, Configs.get('GREEN'), self.player_arrow)
        pg.draw.rect(self.__screen, Configs.get('BLACK'), self.box_pos)
        posx = 200
        for i in range(4):
            pg.draw.rect(self.__screen, Configs.get('WHITE'), (posx*i, 450, self.box_width, self.box_height), self.box_border)

        for i in range(4):
            pg.draw.rect(self.__screen, Configs.get('WHITE'), (posx*i, 525, self.box_width, self.box_height), self.box_border)

        atk_text, atk_rect = AllUI.animate_text_center("Attack (Z)", "WHITE", 100, 487.5)

        if not player.run_lock:
            run_text, run_rect = AllUI.animate_text_center("Run (R)", "WHITE", 300, 487.5)
        else:
            run_text, run_rect = AllUI.animate_text_center("CURSED", "RED", 300, 487.5)

        defend_text, defend_rect = AllUI.animate_text_center("Defend (D)", "WHITE", 100, 562.5)
        item_text, item_rect = AllUI.animate_text_center("Item (I)", "WHITE",300, 562.5)

        skill1_text, skill1_rect = AllUI.animate_text_center("Locked", "WHITE", 500, 487.5)
        if player.skill1_unlock:
            skill1_text, skill1_rect = AllUI.animate_text_center(f"Steal (X) ({player.steal_count}/2)", "WHITE", 500, 487.5)

        skill2_text, skill2_rect = AllUI.animate_text_center("Locked", "WHITE", 500, 562.5)
        if player.skill2_unlock:
            skill2_text, skill2_rect = AllUI.animate_text_center("Fire (C)", "WHITE", 500, 562.5)

        skill3_text, skill3_rect = AllUI.animate_text_center("Locked", "WHITE", 700, 487.5)
        if player.skill3_unlock:
            skill3_text, skill3_rect = AllUI.animate_text_center("Thunder (V)", "WHITE", 700, 487.5)

        skill4_text, skill4_rect = AllUI.animate_text_center("Locked", "WHITE", 700, 562.5)
        if player.skill4_unlock:
            skill4_text, skill4_rect = AllUI.animate_text_center("Instinct (B)", "WHITE", 700, 562.5)

        self.__screen.blit(atk_text, atk_rect)
        self.__screen.blit(run_text, run_rect)
        self.__screen.blit(defend_text, defend_rect)
        self.__screen.blit(item_text, item_rect)
        self.__screen.blit(skill1_text, skill1_rect)
        self.__screen.blit(skill2_text, skill2_rect)
        self.__screen.blit(skill3_text, skill3_rect)
        self.__screen.blit(skill4_text, skill4_rect)

    # Done
    def draw_status_window(self, player):
        x1 = 200
        x2 = 400
        y1 = 200
        y2 = 300
        c1 = (x1 + x2)/2
        c2 = 230
        offset = 30
        settings = Configs.ui_pos("STATUS")
        AllUI.create_box(self.__screen, settings)

        name_text, name_rect = AllUI.animate_text_topleft(message=f"Name: {player.name}", color="BLACK", x=c1, y=c2)
        lvl_text, lvl_rect = AllUI.animate_text_topleft(message=f"Level: {player.level}", color="BLACK", x=c1, y=c2+offset)
        health_text, health_rect = AllUI.animate_text_topleft(message=f"Health: {player.health:.0f}/{player.max_health:.0f}", color="BLACK", x=c1, y=c2+(2*offset))
        atk_text, atk_rect = AllUI.animate_text_topleft(message=f"Attack: {player.damage:.0f}", color="BLACK", x=c1, y=c2+(3*offset))
        eva_text, eva_rect = AllUI.animate_text_topleft(message=f"Evasion: {(player.evasion * 100):.0f}%", color="BLACK", x=c1, y=c2+(4*offset))
        exp_text, exp_rect = AllUI.animate_text_topleft(message=f"Exp: {player.exp:.0f}/{player.exp_threshold:.0f}", color="BLACK", x=c1, y=c2+(5*offset))
        coin_text, coin_rect = AllUI.animate_text_topleft(message=f"Coin: {player.coin:.0f}", color="BLACK", x=c1, y=c2+(6*offset))
        if player.weapon is None:
            weapon_text, weapon_rect = AllUI.animate_text_topleft(message=f"Weapon: None", color="BLACK", x=c1, y=c2+(7*offset))
        elif player.weapon is not None:
            weapon_text, weapon_rect = AllUI.animate_text_topleft(message=f"Weapon: {player.weapon.name}", color="BLACK", x=c1, y=c2+(7*offset))

        self.__screen.blit(name_text, name_rect)
        self.__screen.blit(lvl_text, lvl_rect) 
        self.__screen.blit(health_text, health_rect)
        self.__screen.blit(atk_text, atk_rect)  
        self.__screen.blit(eva_text, eva_rect)
        self.__screen.blit(exp_text, exp_rect)
        self.__screen.blit(coin_text, coin_rect)
        self.__screen.blit(weapon_text, weapon_rect)
