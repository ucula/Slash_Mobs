class Configs:
    __CONFIGS = {
        'FPS': 60,
        'SPEED': 6,
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
                            'GOBLIN': (100-14, 160),
                            'DARK': (100+20, 230),
                            'VAMPIRE1': (130+30, 230+20),
                            'VAMPIRE2': (130+30, 230+20),
                            'VAMPIRE3': (130+30, 230+20),
                            'MINOTAUR1': (130+35, 230+20),
                            'MINOTAUR2': (130+30, 230+20),
                            'MINOTAUR3': (130+30, 230+20),
                            'SCORPION': (200, 300),
                            'BLUE': (130, 250),
                            'PURPLE': (130, 250)
                            }
    
    __MONS_UI_COORDS = {'SLIME': (210, 300),
                        'GOBLIN': (230, 270),
                        'DARK': (210, 285),
                        'VAMPIRE1': (210, 280),
                        'VAMPIRE2': (210, 280),
                        'VAMPIRE3': (210, 280),
                        'MINOTAUR1': (220, 260),
                        'MINOTAUR2': (220, 260),
                        'MINOTAUR3': (220, 260),
                        'SCORPION': (228, 275),
                        'BLUE': (225, 275),
                        'PURPLE': (225, 275)
                        }
    
    __EFFECTS = {"AURA": "final_prog2/assets/effects/aura.png",
                 "FIRE": "final_prog2/assets/effects/fire.png",
                 "THUNDER": "final_prog2/assets/effects/thunder.png",
                 "GRAVITY": "final_prog2/assets/effects/gravity.png",
                 "DOOM": "final_prog2/assets/effects/doom.png",
                 "BLUE": "final_prog2/assets/effects/blue_attack.png",
                 "PURPLE": "final_prog2/assets/effects/purple_attack.png", 
                 "VAMPIRE1": "final_prog2/assets/effects/vampire1_attack.png",
                 "MINOTAUR1": "final_prog2/assets/effects/minotaur1_attack.png",
                 "MINOTAUR2": "final_prog2/assets/effects/minotaur2_attack.png",
                 'EVIL': "final_prog2/assets/effects/evil.png",
                 'HASTE': "final_prog2/assets/effects/haste.png",
                 'CURSE': "final_prog2/assets/effects/curse.png",
                 'HEAL': "final_prog2/assets/effects/heal.png",
                 'BOMB': "final_prog2/assets/effects/bomb.png",
                 'GREED': "final_prog2/assets/effects/greed.png"}
    
    __EFFECTS_OFFSET = {'AURA_GOBLIN': (105, 150),
                    'AURA_DARK': (50, 80),
                    'BLUE': (230, 120),
                    'PURPLE': (230, 120),
                    'VAMPIRE1': (230, 90),
                    'FIRE': (-60, -130),
                    'THUNDER': (-47, -240),
                    'GRAVITY': (-60, -120),
                    'DOOM': (-100, -220),
                    'P_FIRE': (130, 200),
                    'P_THUNDER': (140, 50),
                    'P_INSTINCT': (-6, 10),
                    'MINOTAUR1': (230, 90),
                    'MINOTAUR2': (230, 90),
                    'EVIL': (-100, -100),
                    'HASTE': (0,0),
                    'CURSE': (-37,-37),
                    'HEAL': (-160, -200),
                    'BOMB': (70, 70),
                    'GREED': (170, 270)
                    }


    __MONS = {'SLIME': "final_prog2/assets/mobs/slime.png",
              'GOBLIN': "final_prog2/assets/mobs/goblin.png",
              'DARK': "final_prog2/assets/mobs/dark.png",
              'VAMPIRE1': "final_prog2/assets/mobs/vampire1.png",
              'VAMPIRE2': "final_prog2/assets/mobs/vampire2.png",
              'VAMPIRE3': "final_prog2/assets/mobs/vampire3.png",
              'MINOTAUR1': "final_prog2/assets/mobs/minotaur1.png",
              'MINOTAUR2': "final_prog2/assets/mobs/minotaur2.png",
              'MINOTAUR3': "final_prog2/assets/mobs/minotaur3.png",
              'SCORPION': "final_prog2/assets/mobs/scorpion.png",
              'BLUE': "final_prog2/assets/mobs/blue.png",
              'PURPLE': "final_prog2/assets/mobs/purple.png" 
              }
              
    __BG = {
        'HALL': "final_prog2/assets/bg/hall.jpg",
        'PLAIN': "final_prog2/assets/bg/plain.jpg",
        'SHOP': "final_prog2/assets/bg/shop.jpg",
        'DESERT': "final_prog2/assets/bg/desert.jpg",
        'SNOW': "final_prog2/assets/bg/snow.jpg",
        'CAVE': "final_prog2/assets/bg/cave.jpg"
    }

    __PLAYER = {
        'IDLE': "final_prog2/assets/player/char.png",  
        'LEFT': "final_prog2/assets/player/char.png",
        'RIGHT': "final_prog2/assets/player/char2.png",
        'UP': "final_prog2/assets/player/char.png",
        'DOWN': "final_prog2/assets/player/char.png"
    }
    
    # (border_color, bg_color, initial, terminal, width, height, offset, border)
    __UI_POS = {"HELP": ('BLACK', 'CREAMY', 0, 0, 260, 60, 3, 5),
                "HEALTH": ('WHITE', 'BLACK', 600, 375, 200, 75, 3, 5),
                "STATUS": ('BLACK', 'CREAMY', 200, 200, 400, 300, 3, 5),
                "SKILL_DISPLAY": ("BLACK", "WHITE", 0, 0, 800, 50, 3, 5),
                "SHOP": ('BLACK', 'CREAMY', 100, 100, 600, 400, 3, 5),
                "COIN_BOX": ('BLACK', 'CREAMY', 600, 0, 800, 60, 3, 5),
                "ITEM_TIP": ('BLACK', 'CREAMY', 197, 372, 400, 75, 3, 5)}
    
    __ITEM = {"sword": "final_prog2/assets/items/longsword.png",
              "knife": "final_prog2/assets/items/knife.png",
              "hammer": "final_prog2/assets/items/hammer.png",
              "potion": "final_prog2/assets/items/potion.png",
              "hpotion": "final_prog2/assets/items/hpotion.png",
              "xpotion": "final_prog2/assets/items/xpotion.png",
              "drum": "final_prog2/assets/items/drum.png",
              "greed": "final_prog2/assets/items/greed.png",
              "bomb": "final_prog2/assets/items/bomb.png"
              }

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
        return cls.__UI_POS[key]
    
    @classmethod
    def item(cls, key):
        return cls.__ITEM[key]