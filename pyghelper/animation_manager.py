from typing import Union

import pygame

import pyghelper.utils as utils


class Animation:
    """
    A class which manage the working of an animation.
    """

    def __init__(
        self,
        sprites: list[pygame.Surface],
        durations: Union[int, list[int]],
        starting_sprite_index: int = 0
    ):
        """
        Initialize the animation with the specified sprites and durations.

        Parameters
        ----------
        sprites : list of pygame.Surfaces.
            Can be obtained from a file name using the Image class static methods.
        durations : int or list of int
            Indicates the time to spend on each sprite.
            If an int is passed, it will be used for every sprite.
            If the list does not contain enough values, it will be completed by the last one.
            If the list has too much values, it will be cut off.
        starting_sprite_index : int, default = 0
            The index of the first sprite of the animation.
        """

        self.sprites = sprites
        self.sprites_count = len(self.sprites)
        self.durations = self.__correct_durations(durations, self.sprites_count)
        self.clock: int = 0
        self.current_sprite_index: int = starting_sprite_index
        self.cumulated_durations: list[int] = [sum(self.durations[:i]) for i in range(1, self.sprites_count + 1)]
        self.animation_duration: int = self.cumulated_durations[-1] # The last cumulated sum is the total sum

    def __correct_durations(self, durations: Union[int, list[int]], sprites_count: int) -> list[int]:
        if type(durations) == int:
            return [durations for _ in range(sprites_count)]

        if len(durations) < sprites_count:
            missing_count = sprites_count - len(durations)
            durations.extend([durations[-1]] * missing_count)

        elif len(durations) > sprites_count:
            durations = durations[:sprites_count]

        return durations

    def __get_current_sprite_index(self) -> int:
        return next(
            index
            for index, sprite_start_time in enumerate(self.cumulated_durations)
            if sprite_start_time >= self.clock
        )

    def play(self, ticks: int = 1) -> None:
        """Play the specified number of ticks of the animation.

        Parameters
        ----------
        ticks : int, default = 1
            Number of ticks to play.
        """

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

        self.animations: dict[str, Animation] = dict()

    def add_animation(self, animation: Animation, name: str) -> None:
        """
        Add the specified animation to the manager.

        Parameters
        ----------
        animation : Animation
            Animation to add to the manager.
        name : str
            Name of the animation.
        """

        if type(animation) != Animation:
            raise TypeError("The animation should be of type Animation.")

        if name == "":
            raise ValueError("Animation name cannot be empty.")

        if name in self.animations:
            raise IndexError(f"This name '{name}' is already used for another animation.")

        self.animations[name] = animation

    def remove_animation(self, name: str) -> Animation:
        """
        Remove and return the specified animation from the manager.

        Parameters
        ----------
        name : str
            Name of the animation to remove.
        """

        if name not in self.animations:
            raise ValueError(f"This animation ('{name}') does not exist.")

        return self.animations.pop(name)

    def __getitem__(self, name: str) -> Animation:
        if name not in self.animations:
            raise IndexError(f"This animation ('{name}') does not exist.")

        return self.animations[name]

    def get_animation(self, name: str) -> Animation:
        """
        Return the animation at the specified index. Can be accessed with square brackets.

        Parameters
        ----------
        name : str
            Name of the animation to get.
        """

        return self[name]

    def get_current_sprite(self, name: str) -> pygame.Surface:
        """
        Return the sprite of the specified animation.

        Parameters
        ----------
        name : str
            Name of the animation to get the sprite of.
        """

        return self[name].get_current_sprite()

    def play_all(self, ticks: int = 1) -> None:
        """
        Play the specified number of ticks of all the animations.

        Parameters
        ----------
        ticks : int, default = 1
            Number of ticks to play.
        """

        for animation in self.animations.values():
            animation.play(ticks)
