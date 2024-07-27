import pygame
from pygame import Rect

import pyghelper.images as images


class Scale:
    """Class containing the relevant information to convert from and to game space and screen space."""

    def __init__(self, scale: float, x_offset: float, y_offset: float):
        assert scale > 0
        assert x_offset >= 0
        assert y_offset >= 0

        self.scale = scale
        self.x_offset = x_offset
        self.y_offset = y_offset

    def to_screen_pos(self, game_x: float, game_y: float) -> tuple[float, float]:
        """Convert a position in game space to its counterpart in screen space."""

        return game_x * self.scale + self.x_offset, game_y * self.scale + self.y_offset

    def to_screen_rect(self, game_rect: Rect) -> Rect:
        """Convert a pygame.Rect in game space to its counterpart in screen space."""

        return Rect(
            game_rect.left * self.scale + self.x_offset,
            game_rect.top * self.scale + self.y_offset,
            game_rect.width * self.scale,
            game_rect.height * self.scale
        )

    def to_screen_pos_size(self, game_left: float, game_top: float, game_width: float, game_height: float) -> tuple[
        float, float, float, float]:
        """Convert a position and a size in game space to their counterparts in screen space."""

        return (
            game_left * self.scale + self.x_offset,
            game_top * self.scale + self.y_offset,
            game_width * self.scale,
            game_height * self.scale
        )

    def to_game_pos(self, screen_x: float, screen_y: float) -> tuple[float, float]:
        """Convert a position in screen space to its counterpart in game space."""

        return (screen_x - self.x_offset) / self.scale, (screen_y - self.y_offset) / self.scale

    def to_game_rect(self, screen_rect: Rect) -> Rect:
        """Convert a pygame.Rect in screen space to its counterpart in game space."""

        return Rect(
            (screen_rect.left - self.x_offset) / self.scale,
            (screen_rect.top - self.y_offset) / self.scale,
            screen_rect.width / self.scale,
            screen_rect.height / self.scale
        )

    def to_game_pos_size(self, screen_left: float, screen_top: float, screen_width: float,
                         screen_height: float) -> Rect:
        """Convert a position and a size in screen space to their counterparts in game space."""

        return Rect(
            (screen_left - self.x_offset) / self.scale,
            (screen_top - self.y_offset) / self.scale,
            screen_width / self.scale,
            screen_height / self.scale
        )

    def __repr__(self):
        return f'Scale{{{self.scale=}, {self.x_offset=}, {self.y_offset=}}}'


class Window:
    """A class with static methods to wrap some Pygame ones."""

    @staticmethod
    def create(width: int = 0, height: int = 0, fullscreen: bool = False, title: str = "",
               icon_path: str = "") -> pygame.Surface | pygame.SurfaceType:
        """
        Open a Pygame window with the specified width, height, title and icon.

        Parameters
        ----------
        width, height : int, optional
            Size of the window if not in fullscreen.
        fullscreen: bool
            If true, discard the width and height and set the window to fullscreen.
        title : str, optional
            Title of the window.
        icon_path : str, optional
            Path of the icon image.
        """

        pygame.init()
        if fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((width, height))

        if title != "":
            pygame.display.set_caption(title)

        if icon_path != "":
            icon = images.Image.create(icon_path)
            pygame.display.set_icon(icon)

        return screen

    @staticmethod
    def close() -> None:
        """Premade function which closes Pygame."""

        pygame.display.quit()
        pygame.quit()

    @staticmethod
    def get_scale(game_width: int, game_height: int, screen_width: int = -1, screen_height: int = -1,
                  screen: pygame.Surface = None, tolerance: float = 0.01) -> Scale:
        """
        Returns a Scale object to convert positions and sizes from and to game space and screen space.

        Parameters
        ----------
        game_width, game_height : int
            Dimensions of the game space.
        screen_width, screen_height: int, optional
            Size of the window. Optional because they can be inferred from the screen parameter if present
        screen: pygame.Surface, optional
            Surface containing the game window.
        tolerance : float, optional (default 0.01)
            Tolerance to consider the game space and the screen space dimensions as having the same ratio.
        """

        assert game_width > 0
        assert game_height > 0

        if screen is not None:
            screen_width, screen_height = screen.get_size()

        assert screen_width > 0
        assert screen_height > 0

        game_ratio: float = game_width / game_height
        screen_ratio: float = screen_width / screen_height

        if abs(game_ratio - screen_ratio) < tolerance:
            scale = screen_width / game_width
            x_offset = 0.0
            y_offset = 0.0
        elif game_ratio > screen_ratio:
            scale = screen_width / game_width
            x_offset = 0.0
            y_offset = (screen_height - game_height * scale) / 2
        else:
            scale = screen_height / game_height
            x_offset = (screen_width - game_width * scale) / 2
            y_offset = 0.0

        return Scale(scale, x_offset, y_offset)
