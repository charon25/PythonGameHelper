import os
import random

import pygame

import pyghelper.config as config


class SoundManager:
    """
    A class to ease the use of the mixer module of Pygame.
    """

    def __init__(self):
        """Initialize the sound manager instance and Pygame's Mixer."""

        self.sounds: dict[str, list[pygame.mixer.Sound]] = dict()
        self.musics: dict[str, str] = dict()
        pygame.mixer.init()

    def add_sound(self, sound_path: str, sound_name: str, volume: float = 1.0) -> None:
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

        sound = pygame.mixer.Sound(sound_path)

        sound.set_volume(volume)
        self.sounds[sound_name].append(sound)


    def play_random_sound(self, sound_name: str) -> None:
        """
        Play a random sound among those with the specified name.

        Parameters
        ----------
        sound_name : str
            Name of the sound to be played. It should have been added beforehand.
        """

        sound_candidates = self.sounds.get(sound_name, None)

        if sound_candidates is None:
            return

        sound_to_play = random.choice(sound_candidates)
        sound_to_play.play()


    def add_music(self, music_path: str, music_name: str) -> None:
        """
        Add a new music to the manager.

        Parameters
        ----------
        music_path : str
            Path to the music file.
        music_name : str
            Name of the music, used to play it later.
        """

        self.musics[music_name] = music_path


    def __play_music(self, music_path: str, loop: bool, volume: int = 1.0):
        # Pygame expects -1 to loop and 0 to play the music only once
        # So we take the negative value so when it is 'True' we send -1
        pygame.mixer.music.load(music_path)
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
        self.__play_music(music_to_play, loop=loop, volume=volume)

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

        self.__play_music(self.musics[music_name], loop=loop, volume=volume)


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
