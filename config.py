class Configs:
    __CONFIGS = {
        'FPS': 60,
        'SPEED': 3,
        'WIN_SIZE_W': 800,
        'WIN_SIZE_H': 600,
        'WHITE': (255, 255, 255),
        'BLACK': (0, 0, 0),
        'MAGENTA': (255, 5, 238),
        }
    @classmethod
    def get(cls, key):
        return cls.__CONFIGS[key]