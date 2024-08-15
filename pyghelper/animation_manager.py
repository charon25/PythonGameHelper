import pygame


class Animation:
    """
    A class which manage the working of an animation.
    """

    def __init__(
            self,
            sprites: list[pygame.Surface],
            durations: list[float],
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

        assert len(sprites) > 0
        assert len(durations) > 0

        self.sprites = sprites
        self.sprites_count = len(self.sprites)

        self.durations: list[float] = durations
        self.cumulated_durations: list[float] = [sum(self.durations[:i]) for i in range(1, self.sprites_count + 1)]
        self.animation_duration: float = self.cumulated_durations[-1]  # The last cumulated sum is the total sum

        self.current_sprite_index: int = starting_sprite_index
        self.time: float = self.cumulated_durations[starting_sprite_index]

    def __get_current_sprite_index(self) -> int:
        for index, sprite_start_time in enumerate(self.cumulated_durations):
            if sprite_start_time >= self.time:
                return index

    def play(self, elapsed_time: float):
        """Play the specified number of ticks of the animation.

        Parameters
        ----------
        elapsed_time : float
            elapsed time in second since last call
        """

        self.time = (self.time + elapsed_time) % self.animation_duration
        self.current_sprite_index = self.__get_current_sprite_index()

    def get_current_sprite(self) -> pygame.Surface:
        """Returns the current sprite of the animation."""

        return self.sprites[self.current_sprite_index]


class AnimationManager:
    """
    A class to manages multiple Animation classes simultaneously.
    """

    def __init__(self, animations: list[Animation] = None):
        """Initialize the manager."""

        if animations is None:
            self.animations: list[Animation] = list()
        else:
            self.animations = animations

    def add_animation(self, animation: Animation) -> None:
        """
        Add the specified animation to the manager.

        Parameters
        ----------
        animation : Animation
            Animation to add to the manager.
        name : str
            Name of the animation.
        """

        assert isinstance(animation, Animation), "The animation should be of type Animation."
        self.animations.append(animation)

    def remove_animation(self, animation: Animation):
        """
        Remove and return the specified animation from the manager.

        Parameters
        ----------
        animation : Animation
            Animation object to remove
        """

        self.animations.remove(animation)

    def play_all(self, elapsed_time: float) -> None:
        """
        Play the specified number of ticks of all the animations.

        Parameters
        ----------
        elapsed_time : float
            elapsed time in second since last call
        """

        [animation.play(elapsed_time) for animation in self.animations]
