import os
import random

import pygame


class SoundManager:
    """
    A class to ease the use of the mixer module of Pygame.
    """

    def __init__(self):
        """Initialize the sound manager instance and Pygame's Mixer."""

        self.sounds = {}
        self.musics = {}
        pygame.mixer.init()

    def __add_sound_dic(self, sound: str, sound_name: str):
        """Add the sound to the dictionary of sound, creating the entry if it does not exist."""

        if sound_name not in self.sounds:
            self.sounds[sound_name] = []

        self.sounds[sound_name].append(sound)

    def add_sound(self, sound_path: str, sound_name:str , volume: int = 1.0):
        """
        Add a new sound to the manager.

        sound_path: path to the sound file.
        sound_name: name of the sound, used to play it later.
        volume: volume of the sound, between 0.0 and 1.0 inclusive (default: 1.0).
        """

        if sound_name == "":
            raise ValueError("The sound name cannot be empty.")

        try:
            sound = pygame.mixer.Sound(sound_path)
        except:
            raise FileNotFoundError("Sound file does not exist or is inaccessible.")

        sound.set_volume(volume)
        self.__add_sound_dic(sound, sound_name)

    def play_sound(self, sound_name: str):
        """
        Play a random sound among those with the specified name.

        sound_name: name of the sound to be played.
        """

        if sound_name not in self.sounds or len(self.sounds[sound_name]) == 0:
            raise IndexError("Sound '{}' does not exist.".format(sound_name))

        sound_to_play = random.choice(self.sounds[sound_name])
        sound_to_play.play()

    def add_music(self, music_path: str, music_name: str):
        """
        Add a new music to the manager.

        music_path: path to the music file.
        music_name: name of the music, used to play it later.
        """

        if music_name == "":
            raise ValueError("The music name cannot be empty.")

        if not os.path.isfile(music_path):
            raise FileNotFoundError("Music file does not exist or is inaccessible.")

        if music_name in self.musics:
            raise ValueError("This name is already used by another music.")

        self.musics[music_name] = music_path

    def __load_music(self, music_path: str):
        try:
            pygame.mixer.music.load(music_path)
        except:
            raise FileNotFoundError("File '{}' does not exist or is inaccessible.".format(music_path))

    def __play_music(self, loop: bool, volume: int = 1.0):
        pygame.mixer.music.play(loops=(-1 if loop else 0))
        pygame.mixer.music.set_volume(volume)

    def play_random_music(self, loop: bool = False, volume: int = 1.0):
        """
        Play a random music from the list.

        loop: indicates if the music should be looped (default: False)
        """

        if len(self.musics) == 0:
            raise ValueError("No music previously added.")

        music_to_play = random.choice(list(self.musics.values()))
        self.__load_music(music_to_play)
        self.__play_music(loop=loop, volume=volume)

    def play_music(self, music_name: str, loop: bool = False, volume: int = 1.0):
        """
        Play the music with the specified name.

        music_name: name of the music to be played.
        loop: indicates if the music should be looped (default: False).
        """

        if music_name not in self.musics:
            raise IndexError("Music '{}' does not exist.".format(music_name))

        music_to_play = self.musics[music_name]
        self.__load_music(music_to_play)
        self.__play_music(loop=loop, volume=volume)

    def pause_music(self):
        """Pause the music."""

        pygame.mixer.music.pause()

    def resume_music(self):
        """Unpause the music."""

        pygame.mixer.music.unpause()

    def stop_music(self):
        """Stop the music."""

        pygame.mixer.music.stop()

    def is_music_playing(self) -> bool:
        """Returns True when the music is playing and not paused."""

        return pygame.mixer.music.get_busy()
