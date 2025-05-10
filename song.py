import pygame as pg

class Song:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.__music = {"PLAIN": ,
                           "DESERT": ,
                           "SNOW": ,
                           "CAVE": ,
        }
        self.__sound = {}
    
    def load_music(self, key):
        pg.mixer.music.load(self.__music[key])
        pg.mixer.music.play()

    def load_sound(self, key):
        pg.mixer.music.load(self.__sound[key])
        pg.mixer.music.play()