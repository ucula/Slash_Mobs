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
        'MOB_x': 100,
        'MOB_y': 160
        }
    __MONS_OFFSET = {'SLIME': (28, 25),
                    'GOBLIN': (117, 133),
                    'DARK': (57, 72)
                    }
    
    __MONS_COMBAT_CORDS = {'SLIME': (150, 280),
                            'GOBLIN': (100, 160),
                            'DARK': (100, 230)
                            }
    
    __MONS_UI_COORDS = {'SLIME': (230, 320),
                        'GOBLIN': (260, 290),
                        'DARK': (210, 320)
                        }
    
    __MONS = {'SLIME': "final_prog2/assets/slime.png",
              'GOBLIN': "final_prog2/assets/goblin.png",
              'DARK': "final_prog2/assets/dark.png"
              }
              
    __BG = {
        'HALL': "final_prog2/assets/hall.jpg",
        'PLAIN': "final_prog2/assets/plain.jpg",
        'SHOP': "final_prog2/assets/shop.jpg",
    }

    __PLAYER = {
        'IDLE': "final_prog2/assets/char.png",  
        'LEFT': "final_prog2/assets/char.png",
        'RIGHT': "final_prog2/assets/char2.png",
        'UP': "final_prog2/assets/char.png",
        'DOWN': "final_prog2/assets/char.png"
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
    def monster_ui(cls, key):
        return cls.__MONS_UI_COORDS[key]