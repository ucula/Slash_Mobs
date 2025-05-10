import pygame as pg
from config import Configs

class AllUI:
    def __init__(self, screen):
        self.__screen = screen
        # transition cutscene
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
    def animate_text_center(screen, message, color, x, y, font=None):
        if font is None:
            font = pg.font.Font(None, 30)
        text = font.render(message, True, Configs.get(color))
        rect = text.get_rect(center=(x, y))
        screen.blit(text, rect)
    
    @staticmethod
    def animate_text_topleft(screen, message, color, x, y, font=None):
        if font is None:
            font = pg.font.Font(None, 30)
        text = font.render(message, True, Configs.get(color))
        rect = text.get_rect(topleft=(x, y))
        screen.blit(text, rect)
    
    @staticmethod
    def animate_text_midtop(screen, message, color, x, y, font=None):
        if font is None:
            font = pg.font.Font(None, 30)
        text = font.render(message, True, Configs.get(color))
        rect = text.get_rect(topleft=(x, y))
        screen.blit(text, rect)

    @staticmethod
    def create_box(screen, settings):
        pg.draw.rect(screen, Configs.get(settings[0]), (settings[2], settings[3], settings[4], settings[5]), settings[7])
        pg.draw.rect(screen, Configs.get(settings[1]), (settings[2]+settings[6], settings[3]+settings[6], settings[4]-2*settings[6], settings[5]-2*settings[6]))
    
    # Delay
    def delay(self, limit):
        current_time = pg.time.get_ticks()
        if not self.time_lock:
            self.start_time = pg.time.get_ticks()
            self.time_lock = True
        if current_time - self.start_time >= limit:
            return False
        return True

    # Get bg
    def draw_bg(self, scene):
        image = pg.image.load(Configs.background(scene)).convert()
        return image

    # Cut scene series 
    def draw_screen_transition(self, range):
        if self.curtain < range:
            pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, self.curtain, 600))
            self.curtain += 20
            return False
        else:
            self.curtain = 0
            return True
        
    """
    :Normal scene series: 
    """
    # Help box at top left of screen
    def draw_help(self, shop=False):
        settings = Configs.ui_pos("HELP")
        AllUI.create_box(self.__screen, settings)    
        if shop:
            AllUI.animate_text_topleft(self.__screen,message=f"Press \"E\" to open shop", color='BLACK', x=10, y=30)
        AllUI.animate_text_topleft(self.__screen, message=f"Press \"I\" to open status", color='BLACK', x=10, y=10)

    # Status window for normal scene
    def draw_status_window(self, player):
        x1 = 200
        x2 = 400
        c1 = (x1 + x2)/2
        c2 = 230
        offset = 30
        settings = Configs.ui_pos("STATUS")
        AllUI.create_box(self.__screen, settings)

        AllUI.animate_text_topleft(self.__screen, message=f"Name: {player.name}", color="BLACK", x=c1, y=c2)
        AllUI.animate_text_topleft(self.__screen, message=f"Level: {player.level}", color="BLACK", x=c1, y=c2+offset)
        AllUI.animate_text_topleft(self.__screen, message=f"Health: {player.health:.0f}/{player.max_health:.0f}", color="BLACK", x=c1, y=c2+(2*offset))
        AllUI.animate_text_topleft(self.__screen, message=f"Attack: {player.damage:.0f}", color="BLACK", x=c1, y=c2+(3*offset))
        AllUI.animate_text_topleft(self.__screen, message=f"Evasion: {(player.evasion * 100):.0f}%", color="BLACK", x=c1, y=c2+(4*offset))
        AllUI.animate_text_topleft(self.__screen, message=f"Exp: {player.exp:.0f}/{player.exp_threshold:.0f}", color="BLACK", x=c1, y=c2+(5*offset))
        AllUI.animate_text_topleft(self.__screen, message=f"Coin: {player.coin:.0f}", color="BLACK", x=c1, y=c2+(6*offset))
        if player.weapon is None:
            AllUI.animate_text_topleft(self.__screen, message=f"Weapon: None", color="BLACK", x=c1, y=c2+(7*offset))
        elif player.weapon is not None:
            AllUI.animate_text_topleft(self.__screen, message=f"Weapon: {player.weapon.name}", color="BLACK", x=c1, y=c2+(7*offset))

    """
    :Combat series:
    """
    def draw_item_menu(self, player):
        settings = Configs.ui_pos("ITEM_TIP")
        pg.draw.polygon(self.__screen, Configs.get('GREEN'), self.player_arrow)
        pg.draw.rect(self.__screen, Configs.get('BLACK'), self.box_pos)
        posx = 200
        for i in range(4):
            pg.draw.rect(self.__screen, Configs.get('WHITE'), (posx*i, 450, self.box_width, self.box_height), self.box_border)

        for i in range(4):
            pg.draw.rect(self.__screen, Configs.get('WHITE'), (posx*i, 525, self.box_width, self.box_height), self.box_border)

        for j in range(2):
            for i in range(3):
                y = 487.5
                name = list(player.items.keys())[i+3*j]
                count = player.items[name].count
                AllUI.animate_text_center(self.__screen, f"{name} ({count})", "WHITE", 100+i*200, y+j*74.5)
        AllUI.animate_text_center(self.__screen, "Go back (I)", "WHITE", 700 , 487.5)
        AllUI.animate_text_center(self.__screen, "Select (Space)", "WHITE", 700 , 562.5)
        AllUI.create_box(self.__screen, settings)
        AllUI.animate_text_center(self.__screen, "Move with (LEFT) (RIGHT)", "BLACK", 397 , 409.5)

    def draw_selector(self, index):
        posx = 200
        posy = 450
        if index in (3, 4, 5):
            posy = 525
        if index == 3:
            index = 0
        elif index == 4:
            index = 1
        elif index == 5:
            index = 2
        pg.draw.rect(self.__screen, Configs.get('RED'), (posx*index, posy, self.box_width, self.box_height), self.box_border)

    # Draw damage above player and mob's head after damage calculation
    def draw_damage(self, turn, player, monster, evade=None):
        font = pg.font.SysFont(None, 48)
        x = Configs.monster_damage(monster.name)[0]
        y = Configs.monster_damage(monster.name)[1]
        if turn == "player":
            if evade:
                AllUI.animate_text_center(self.__screen, f"MISS", 'BLACK', x, y, font)
                AllUI.animate_text_center(self.__screen, f"MISS", 'RED', x+4, y, font)
            else:
                AllUI.animate_text_center(self.__screen, f"{player.atk_tmp:.0f}", 'BLACK', x, y, font)
                AllUI.animate_text_center(self.__screen, f"{player.atk_tmp:.0f}", 'RED', x+4, y, font)
        elif turn == "mob":
            if evade:
                AllUI.animate_text_center(self.__screen, f"MISS", 'BLACK', player.x+35, player.y-10, font)
                AllUI.animate_text_center(self.__screen, f"MISS", 'RED', player.x+39, player.y-10, font)
            else:
                AllUI.animate_text_center(self.__screen, f"{monster.atk_tmp:.0f}", 'BLACK', player.x+35, player.y-10, font)
                AllUI.animate_text_center(self.__screen, f"{monster.atk_tmp:.0f}", 'RED', player.x+39, player.y-10, font)
    
    def draw_heal(self, player):
        font = pg.font.SysFont(None, 48)
        AllUI.animate_text_center(self.__screen, f"{player.atk_tmp:.0f}", 'BLACK', player.x+35, player.y-10, font)
        AllUI.animate_text_center(self.__screen, f"{player.atk_tmp:.0f}", 'GREEN', player.x+39, player.y-10, font)

    """
    Draw summarization of battle (exp and money droped or whether player level up or not)
    """
    def draw_summary(self, drops, player, up):
        pg.draw.rect(self.__screen, Configs.get('BLACK'), (0, 0, 800, 120), 5)
        pg.draw.rect(self.__screen, Configs.get('WHITE'), (3, 3, 794, 114))
        AllUI.animate_text_center(self.__screen, f"You earned {drops[0]} coins", "BLACK", 420, 25)
        AllUI.animate_text_center(self.__screen, f"You earned {drops[1]} exp", "BLACK", 420, 50)
        AllUI.animate_text_center(self.__screen, f"Press \"SPACE\" to continue", "BLACK", 420, 75)
        if up:
            AllUI.animate_text_center(self.__screen, f"{player.name} level up!", "BLACK", 420, 100)

    # health bar in combat
    def draw_health_bar(self, player):
        settings = Configs.ui_pos("HEALTH")
        AllUI.create_box(self.__screen, settings)
        AllUI.animate_text_center(self.__screen, f"Health: {player.health:.0f}/{player.max_health:.0f}", "RED", 700, 412.5)     

    """
    For displaying what skill is being used by mob or how does that skill affect player or the mob itself
    """
    def draw_skill_display(self, message=None):
        settings = Configs.ui_pos("SKILL_DISPLAY")
        AllUI.create_box(self.__screen, settings)
        AllUI.animate_text_center(self.__screen, message, "BLACK", 420, 25)    

    # GUI menu
    def draw_gui_combat(self, player):
        pg.draw.polygon(self.__screen, Configs.get('GREEN'), self.player_arrow)
        pg.draw.rect(self.__screen, Configs.get('BLACK'), self.box_pos)
        posx = 200
        for i in range(4):
            pg.draw.rect(self.__screen, Configs.get('WHITE'), (posx*i, 450, self.box_width, self.box_height), self.box_border)

        for i in range(4):
            pg.draw.rect(self.__screen, Configs.get('WHITE'), (posx*i, 525, self.box_width, self.box_height), self.box_border)

        AllUI.animate_text_center(self.__screen, "Attack (Z)", "WHITE", 100, 487.5)
        if not player.all_lock:
            AllUI.animate_text_center(self.__screen, "Defend (D)", "WHITE", 100, 562.5)
            AllUI.animate_text_center(self.__screen, "Item (I)", "WHITE",300, 562.5)

            if player.run_lock:
                AllUI.animate_text_center(self.__screen, "CURSED", "RED", 300, 487.5)
            else:
                AllUI.animate_text_center(self.__screen, "Run (R)", "WHITE", 300, 487.5)  

            if player.skill1_unlock:
                AllUI.animate_text_center(self.__screen, f"Steal (X) ({player.steal_count}/2)", "WHITE", 500, 487.5)
            else:
                AllUI.animate_text_center(self.__screen, "Locked", "WHITE", 500, 487.5)

            if player.skill2_unlock:
                AllUI.animate_text_center(self.__screen, "Fire (C)", "WHITE", 500, 562.5)
            else:
                AllUI.animate_text_center(self.__screen, "Locked", "WHITE", 500, 562.5)

            if player.skill3_unlock:
                AllUI.animate_text_center(self.__screen, "Thunder (V)", "WHITE", 700, 487.5)
            else:
                AllUI.animate_text_center(self.__screen, "Locked", "WHITE", 700, 487.5)

            if player.skill4_unlock:
                AllUI.animate_text_center(self.__screen, "Instinct (B)", "WHITE", 700, 562.5)
            else:
                AllUI.animate_text_center(self.__screen, "Locked", "WHITE", 700, 562.5)

        else:
            y = [487.5, 562.5]

        # Cursed
            AllUI.animate_text_center(self.__screen, "CURSED", "RED", 100, 562.5)
            step = 200
            for j in range(3):
                for i in range(2): 
                    if i % 2 == 0:
                        picky = y[0]
                    else:
                        picky = y[1]
                    AllUI.animate_text_center(self.__screen, "CURSED", "RED", 300+j*step, picky)

