class Configs:
    __CONFIGS = {
        'FPS': 60,
        'WIN_SIZE_W': 1000,
        'WIN_SIZE_H': 800,
        'WHITE': (255, 255, 255),
}
    @classmethod
    def get(cls, key):
        return cls.__CONFIGS[key]