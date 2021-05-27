import pygame
import pyaudio


class SoundManager:
    """
    A class to ease the use of the mixer module of Pygame.
    """

    def __init__(self):
        """Initialize the instance and Pygame's Mixer."""

        self.sounds = {}
        self.musics = {}
        pygame.mixer.init()


    def __add_sound_dic(self, sound, sound_name):
        """Add the sound to the dictionary of sound, creating the entry if it does not exist."""
        if not sound_name in self.sounds:
            self.sounds[sound_name] = []

        self.sounds[sound_name].append(sound)


    def add_sound(self, sound_path, sound_name):
        """
        Add a new sound to the manager.

        sound_path: string containing the path to the sound file.
        sound_name: string containing the name of the sound, used to play it later.
        """

        if sound_name == "":
            raise ValueError("The sound name can't be empty.")

        try:
            sound = pygame.mixer.Sound(sound_path)
        except:
            raise FileNotFoundError("Sound file does not exist or is inaccessible.")
        
        self.__add_sound_dic(sound, sound_name)
