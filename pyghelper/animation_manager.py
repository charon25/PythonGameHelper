from typing import List, Union

import pygame


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

        if type(durations) == int:
            durations = [durations]

        if len(durations) < len(sprites):
            missing_count = len(sprites) - len(durations)
            durations.extend([durations[-1]] * missing_count)
        elif len(durations) > len(sprites):
            durations = durations[:len(sprites)]

        self.sprites = sprites
        self.durations = durations
        self.sprites_count = len(self.sprites)
        self.clock = 0
        self.current_sprite_index = starting_sprite_index
        self.animation_duration = sum(self.durations)
        self.cumulated_durations = [sum(self.durations[:i]) for i in range(1, self.sprites_count + 1)]

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
