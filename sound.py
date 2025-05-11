import pygame as pg

class Sound:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.__music = {"HALL": "final_prog2/music/hall.mp3",
                        "PLAIN": "final_prog2/music/plain.wav",
                        "DESERT": "final_prog2/music/desert.wav",
                        "SNOW": "final_prog2/music/snow.wav",
                        "CAVE": "final_prog2/music/cave.wav",
                        "SHOP": "final_prog2/music/hall.mp3",
                        "COMBAT": "final_prog2/music/combat.mp3"
        }
        self.__sound = {"TRANSITION": "final_prog2/sound/transition.wav"}
        self.play = False
        self.transition = False
    
    def load_music(self, scene):
        pg.mixer.music.load(self.__music[scene])
        pg.mixer.music.play(-1)

    def load_sound(self, key):
        pg.mixer.music.load(self.__sound[key])
        pg.mixer.music.play()

    def set_volumue(self, volume=None, scene=None):
        if scene is not None:
            if scene == "HALL" or scene == "SHOP":
                pg.mixer.music.set_volume(1)
        elif volume is not None:
            pg.mixer.music.set_volume(volume)
        else:
            pg.mixer.music.set_volume(0.2)