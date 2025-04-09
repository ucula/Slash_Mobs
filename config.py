class Configs:
    __CONFIGS = {
        'WIN_SIZE_W': 800,
        'WIN_SIZE_H': 600,
        'WHITE': (255, 255, 255),
}
    @classmethod
    def get(cls, key):
        return cls.__CONFIGS[key]