class Configs:
    __CONFIGS = {
        'FPS': 60,
        'SPEED': 4,
        'WIN_SIZE_W': 800,
        'WIN_SIZE_H': 600,
        'WHITE': (255, 255, 255),
        'BLACK': (0, 0, 0),
        'MAGENTA': (255, 5, 238),
        'YELLOW': (255, 255, 0),
        'BLUE': (0, 0, 255),
        'GRAY': (128, 128, 128),
        'GREEN': (0, 255, 0),
        'RED': (255, 0, 0),
        'CREAMY': (242, 217, 174),
        'TRANSPARENT': (1, 2, 3),
        'MOB_x': 100,
        'MOB_y': 160
        }
    
    __MONS_OFFSET = {'SLIME': (28, 25),
                    'GOBLIN': (117, 133),
                    'DARK': (57, 72),
                    'VAMPIRE1': (38, 72),
                    'VAMPIRE2': (38, 72),
                    'VAMPIRE3': (38, 72),
                    'MINOTAUR1': (38, 72),
                    'MINOTAUR2': (38, 72),
                    'MINOTAUR3': (38, 72),
                    'SCORPION': (0, 0),
                    'BLUE': (60, 80),
                    'PURPLE': (60, 80)
                    }
    
    __MONS_COMBAT_CORDS = {'SLIME': (150, 280),
                            'GOBLIN': (100, 160),
                            'DARK': (100, 230),
                            'VAMPIRE1': (130, 230),
                            'VAMPIRE2': (130, 230),
                            'VAMPIRE3': (130, 230),
                            'MINOTAUR1': (130, 230),
                            'MINOTAUR2': (130, 230),
                            'MINOTAUR3': (130, 230),
                            'SCORPION': (200, 300),
                            'BLUE': (130, 250),
                            'PURPLE': (130, 250)
                            }
    
    __MONS_UI_COORDS = {'SLIME': (230, 320),
                        'GOBLIN': (260, 290),
                        'DARK': (210, 320),
                        'VAMPIRE1': (210, 320),
                        'VAMPIRE2': (210, 320),
                        'VAMPIRE3': (210, 320),
                        'MINOTAUR1': (210, 320),
                        'MINOTAUR2': (210, 320),
                        'MINOTAUR3': (210, 320),
                        'SCORPION': (210, 320),
                        'BLUE': (210, 320),
                        'PURPLE': (210, 320)
                        }
    
    __EFFECTS = {"AURA": "final_prog2/assets/aura.png",
                 "FIRE": "final_prog2/assets/fire.png",
                 "THUNDER": "final_prog2/assets/thunder.png",
                 "GRAVITY": "final_prog2/assets/gravity.png",
                 "DOOM": "final_prog2/assets/doom.png",
                 "BLUE": "final_prog2/assets/blue_attack.png",
                 "PURPLE": "final_prog2/assets/purple_attack.png", 
                 "VAMPIRE1": "final_prog2/assets/vampire1_attack.png"}
    
    __EFFECTS_OFFSET = {'GOBLIN': (105, 150),
                    'DARK': (50, 80),
                    'BLUE': (230, 120),
                    'PURPLE': (230, 120),
                    'VAMPIRE1': (200, 100),
                    'FIRE': (-60, -130),
                    'THUNDER': (-47, -240),
                    'GRAVITY': (-60, -120),
                    'DOOM': (-100, -220)
                    }

    __MONS = {'SLIME': "final_prog2/assets/slime.png",
              'GOBLIN': "final_prog2/assets/goblin.png",
              'DARK': "final_prog2/assets/dark.png",
              'VAMPIRE1': "final_prog2/assets/vampire1.png",
              'VAMPIRE2': "final_prog2/assets/vampire2.png",
              'VAMPIRE3': "final_prog2/assets/vampire3.png",
              'MINOTAUR1': "final_prog2/assets/minotaur1.png",
              'MINOTAUR2': "final_prog2/assets/minotaur2.png",
              'MINOTAUR3': "final_prog2/assets/minotaur3.png",
              'SCORPION': "final_prog2/assets/scorpion.png",
              'BLUE': "final_prog2/assets/blue.png",
              'PURPLE': "final_prog2/assets/purple.png" 
              }
              
    __BG = {
        'HALL': "final_prog2/assets/hall.jpg",
        'PLAIN': "final_prog2/assets/plain.jpg",
        'SHOP': "final_prog2/assets/shop.jpg",
        'DESERT': "final_prog2/assets/desert.jpg",
        'SNOW': "final_prog2/assets/snow.jpg",
        'CAVE': "final_prog2/assets/cave.jpg"
    }

    __PLAYER = {
        'IDLE': "final_prog2/assets/char.png",  
        'LEFT': "final_prog2/assets/char.png",
        'RIGHT': "final_prog2/assets/char2.png",
        'UP': "final_prog2/assets/char.png",
        'DOWN': "final_prog2/assets/char.png"
    }
    
    # (border_color, bg_color, initial, terminal, width, height, offset, border)
    __UI_POS = {"HELP": ('BLACK', 'CREAMY', 0, 0, 250, 60, 3, 5),
                "HEALTH": ('WHITE', 'BLACK', 600, 375, 200, 75, 3, 5),
                "STATUS": ('BLACK', 'CREAMY', 200, 200, 400, 300, 3, 5)}
    
    @classmethod
    def monster(cls, key):
        return cls.__MONS[key]
    
    @classmethod
    def get(cls, key):
        return cls.__CONFIGS[key]
    
    @classmethod
    def background(cls, key):
        return cls.__BG[key]
    
    @classmethod
    def player_animation(cls, key):
        return cls.__PLAYER[key]
    
    @classmethod
    def monster_offsets(cls, key):
        return cls.__MONS_OFFSET[key]
    
    @classmethod
    def monster_combat(cls, key):
        return cls.__MONS_COMBAT_CORDS[key]
    
    @classmethod
    def monster_damage(cls, key):
        return cls.__MONS_UI_COORDS[key]
    
    @classmethod
    def effects(cls, key):
        return cls.__EFFECTS[key]
    
    @classmethod
    def effect_offset(cls, key):
        return cls.__EFFECTS_OFFSET[key]
    
    @classmethod
    def ui_pos(cls, key):
        return  cls.__UI_POS[key]