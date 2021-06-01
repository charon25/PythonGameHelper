from typing import List, Union

import pygame

import pyghelper.utils as utils


class Animation:
    """
    A class which manage the details of an animation.
    """

    def __init__(
        self,
        sprites: List[pygame.Surface],
        durations: Union[int, List[int]],
        starting_sprite_index: int = 0
    ):
        """
        Initialize the animation with the specified sprites and durations.

        sprites: list of Pygame's Surfaces. Can be obtained from a file name using the Image static methods.
        durations: int or list of ints indicating the time to spend on each sprite.
            If an int is passed, it will be used for every sprite.
            If the list does not contain enough values, it will be completed by the last one.
            If the list has too much values, it will be cut off.
        starting_sprite_index: the index of the first sprite of the animation (default: 0).
        """

        self.sprites = sprites
        self.sprites_count = len(self.sprites)
        self.durations = self._correct_durations(durations, self.sprites_count)
        self.clock = 0
        self.current_sprite_index = starting_sprite_index
        self.cumulated_durations = [sum(self.durations[:i]) for i in range(1, self.sprites_count + 1)]
        self.animation_duration = self.cumulated_durations[-1] # The last cumulated sum is the total sum

    def _correct_durations(self, durations, sprites_count):
        if type(durations) == int:
            durations = [durations]

        if len(durations) < sprites_count:
            missing_count = sprites_count - len(durations)
            durations.extend([durations[-1]] * missing_count)
        elif len(durations) > sprites_count:
            durations = durations[:sprites_count]

        return durations

    def __get_current_sprite_index(self):
        return next(
            index
            for index, sprite_start_time in enumerate(self.cumulated_durations)
            if sprite_start_time >= self.clock
        )

    def play(self, ticks=1) -> None:
        """Play the specified number of ticks (default: 1) of the animation."""

        self.clock = (self.clock + ticks) % self.animation_duration
        self.current_sprite_index = self.__get_current_sprite_index()

    def get_current_sprite(self) -> pygame.Surface:
        """Returns the current sprite of the animation."""

        return self.sprites[self.current_sprite_index]


class AnimationManager:
    """
    A class to manages multiple Animation classes simultaneously.
    """

    def __init__(self):
        """Initialize the manager."""

        self.animations = {}

    def add_animation(self, animation: Animation, name: str) -> None:
        """Add the specified animation to the manager."""

        if type(animation) != Animation:
            raise TypeError("The animation should be of type Animation.")
        
        if name == "":
            raise ValueError("Animation name cannot be empty.")

        if name in self.animations:
            raise IndexError("This name ('{}') is already used for another animation.".format(name))

        self.animations[name] = animation

    def remove_animation(self, name: str) -> Animation:
        """Remove and return the specified animation from the manager."""

        if name not in self.animations:
            raise ValueError("This animation ('{}') does not exist.")

        return self.animations.pop(name)

    def get_animation(self, name: str) -> Animation:
        """Return the animation at the specified index."""

        if name not in self.animations:
            raise IndexError("This animation ('{}') does not exist.".format(name))

        return self.animations[name]

    def get_current_sprite(self, name: str) -> pygame.Surface:
        """Return the sprite of the specified animation."""

        if name not in self.animations:
            raise IndexError("This animation ('{}') does not exist.".format(name))

        return self.animations[name].get_current_sprite()

    def play_all(self, ticks = 1) -> None:
        """Play the specified number of ticks (default: 1) of all the animations."""

        for animation in self.animations.values():
            animation.play(ticks)
