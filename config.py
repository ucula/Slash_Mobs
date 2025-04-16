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
        'GRAY': (128, 128, 128)
        }
    @classmethod
    def get(cls, key):
        return cls.__CONFIGS[key]