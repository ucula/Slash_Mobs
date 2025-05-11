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
    
    __EFFECTS = {"AURA": "Slash_Mobs/assets/effects/aura.png",
                 "FIRE": "Slash_Mobs/assets/effects/fire.png",
                 "THUNDER": "Slash_Mobs/assets/effects/thunder.png",
                 "GRAVITY": "Slash_Mobs/assets/effects/gravity.png",
                 "DOOM": "Slash_Mobs/assets/effects/doom.png",
                 "BLUE": "Slash_Mobs/assets/effects/blue_attack.png",
                 "PURPLE": "Slash_Mobs/assets/effects/purple_attack.png", 
                 "VAMPIRE1": "Slash_Mobs/assets/effects/vampire1_attack.png",
                 "MINOTAUR1": "Slash_Mobs/assets/effects/minotaur1_attack.png",
                 "MINOTAUR2": "Slash_Mobs/assets/effects/minotaur2_attack.png",
                 'EVIL': "Slash_Mobs/assets/effects/evil.png",
                 'HASTE': "Slash_Mobs/assets/effects/haste.png",
                 'CURSE': "Slash_Mobs/assets/effects/curse.png",
                 'HEAL': "Slash_Mobs/assets/effects/heal.png",
                 'BOMB': "Slash_Mobs/assets/effects/bomb.png",
                 'GREED': "Slash_Mobs/assets/effects/greed.png"}
    
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


    __MONS = {'SLIME': "Slash_Mobs/assets/mobs/slime.png",
              'GOBLIN': "Slash_Mobs/assets/mobs/goblin.png",
              'DARK': "Slash_Mobs/assets/mobs/dark.png",
              'VAMPIRE1': "Slash_Mobs/assets/mobs/vampire1.png",
              'VAMPIRE2': "Slash_Mobs/assets/mobs/vampire2.png",
              'VAMPIRE3': "Slash_Mobs/assets/mobs/vampire3.png",
              'MINOTAUR1': "Slash_Mobs/assets/mobs/minotaur1.png",
              'MINOTAUR2': "Slash_Mobs/assets/mobs/minotaur2.png",
              'MINOTAUR3': "Slash_Mobs/assets/mobs/minotaur3.png",
              'SCORPION': "Slash_Mobs/assets/mobs/scorpion.png",
              'BLUE': "Slash_Mobs/assets/mobs/blue.png",
              'PURPLE': "Slash_Mobs/assets/mobs/purple.png" 
              }
              
    __BG = {
        'HALL': "Slash_Mobs/assets/bg/hall.jpg",
        'PLAIN': "Slash_Mobs/assets/bg/plain.jpg",
        'SHOP': "Slash_Mobs/assets/bg/shop.jpg",
        'DESERT': "Slash_Mobs/assets/bg/desert.jpg",
        'SNOW': "Slash_Mobs/assets/bg/snow.jpg",
        'CAVE': "Slash_Mobs/assets/bg/cave.jpg"
    }

    __PLAYER = {
        'IDLE': "Slash_Mobs/assets/player/char.png",  
        'LEFT': "Slash_Mobs/assets/player/char.png",
        'RIGHT': "Slash_Mobs/assets/player/char2.png",
        'UP': "Slash_Mobs/assets/player/char.png",
        'DOWN': "Slash_Mobs/assets/player/char.png"
    }
    
    # (border_color, bg_color, initial, terminal, width, height, offset, border)
    __UI_POS = {"HELP": ('BLACK', 'CREAMY', 0, 0, 260, 60, 3, 5),
                "HEALTH": ('WHITE', 'BLACK', 600, 375, 200, 75, 3, 5),
                "STATUS": ('BLACK', 'CREAMY', 200, 200, 400, 300, 3, 5),
                "SKILL_DISPLAY": ("BLACK", "WHITE", 0, 0, 800, 50, 3, 5),
                "SHOP": ('BLACK', 'CREAMY', 100, 100, 600, 400, 3, 5),
                "COIN_BOX": ('BLACK', 'CREAMY', 600, 0, 800, 60, 3, 5),
                "ITEM_TIP": ('BLACK', 'CREAMY', 197, 372, 400, 75, 3, 5)}
    
    __ITEM = {"sword": "Slash_Mobs/assets/items/longsword.png",
              "knife": "Slash_Mobs/assets/items/knife.png",
              "hammer": "Slash_Mobsnal_prog2/assets/items/hammer.png",
              "potion": "Slash_Mobs/assets/items/potion.png",
              "hpotion": "Slash_Mobs/assets/items/hpotion.png",
              "xpotion": "Slash_Mobs/assets/items/xpotion.png",
              "drum": "Slash_Mobs/assets/items/drum.png",
              "greed": "Slash_Mobs/assets/items/greed.png",
              "bomb": "Slash_Mobs/assets/items/bomb.png"
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