import collections
import pathlib
import random

import pygame

import pyghelper.config as config


class SoundManager:
    """
    A class to ease the use of the mixer module of Pygame.
    """

    def __init__(self):
        """Initialize the sound manager instance and Pygame's Mixer."""

        self.sounds = collections.defaultdict(list)
        self.musics = dict()
        pygame.mixer.init()

    def add_sound(self, sound_path: str, sound_name: str, volume: float = 1.0):
        """
        Add a new sound to the manager.

        Parameters
        ----------
        sound_path : str
            Path to the sound file.
        sound_name : str
            Name of the sound, used to play it later.
        volume : float, default = 1.0
            Volume of the sound, between 0.0 and 1.0 inclusive.
        """

        if sound_name == "":
            raise ValueError("The sound name cannot be empty.")

        try:
            sound = pygame.mixer.Sound(sound_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Sound file '{sound_path}' does not exist or is inaccessible.")

        sound.set_volume(volume)
        self.sounds[sound_name].append(sound)

    def play_sound(self, sound_name: str):
        """
        Play a random sound among those with the specified name.

        Parameters
        ----------
        sound_name : str 
            Name of the sound to be played. It should have been added beforehand.
        """

        sound_candidates = self.sounds.get(sound_name)

        if not sound_candidates:
            raise IndexError(f"Sound '{sound_name}' does not exist.")

        sound_to_play = random.choice(sound_candidates)
        sound_to_play.play()

    def add_music(self, music_path: str, music_name: str):
        """
        Add a new music to the manager.

        Parameters
        ----------
        music_path : str
            Path to the music file.
        music_name : str
            Name of the music, used to play it later.
        """

        if music_name == "":
            raise ValueError("The music name cannot be empty.")

        if not pathlib.Path.isfile(music_path):
            raise FileNotFoundError(f"Music file '{music_path}' does not exist or is inaccessible.")

        if music_name in self.musics:
            raise ValueError("This name is already used by another music.")

        self.musics[music_name] = music_path

    def __load_music(self, music_path: str):
        try:
            pygame.mixer.music.load(music_path)
        except pygame.error:
            raise FileNotFoundError(f"File '{music_path}' does not exist or is inaccessible.")

    def __play_music(self, loop: bool, volume: int = 1.0):
        # Pygame expects -1 to loop and 0 to play the music only once
        # So we take the negative value so when it is 'True' we send -1
        pygame.mixer.music.play(loops=-int(loop))
        pygame.mixer.music.set_volume(volume)

    def play_random_music(self, loop: bool = False, volume: int = 1.0):
        """
        Play a random music from the list.

        Parameters
        ----------
        loop : bool, default = False
            Indicates if the music should be looped.
        volume : float, default = 1.0
            Volume at which to play the music, between 0.0 and 1.0 inclusive.
        """

        if len(self.musics) == 0:
            raise ValueError("No music previously added.")

        music_to_play = random.choice(list(self.musics.values()))
        self.__load_music(music_to_play)
        self.__play_music(loop=loop, volume=volume)

    def play_music(self, music_name: str, loop: bool = False, volume: int = 1.0):
        """
        Play the music with the specified name.

        Parameters
        ----------
        music_name : str
            Name of the music to be played.
        loop : bool, default = False
            Indicates if the music should be looped.
        volume : float, default = 1.0
            Volume at which to play the music, between 0.0 and 1.0 inclusive (default: 1.0).
        """

        if music_name not in self.musics:
            raise IndexError(f"Music '{music_name}' does not exist.")

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

    def enable_music_endevent(self):
        """
        Enable the posting of an event when the music ends.

        Notes
        -----
        Uses pygame.USEREVENT+1 as type, so be aware of any conflict.
        """

        pygame.mixer.music.set_endevent(config.MUSICENDEVENT)

    def disable_music_endevent(self):
        """Disable the posting of an event when the music ends (default state)."""

        pygame.mixer.music.set_endevent()
