class Configs:
    __CONFIGS = {
        'FPS': 80,
        'SPEED': 5,
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
    @classmethod
    def get(cls, key):
        return cls.__CONFIGS[key]