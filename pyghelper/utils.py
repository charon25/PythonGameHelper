from typing import Any, List, Tuple, Type, Union

import pygame

import pyghelper.images as images


class Window:
    """A class with static methods to wrap some Pygame ones."""

    @staticmethod
    def create(width: int, height: int, title: str = "", icon_path: str = ""):
        """
        Open a Pygame window with the specified width, height, title and icon.

        Parameters
        ----------
        width, height : int
            Size of the window.
        title : str, optional
            Title of the window.
        icon_path : str, optional
            Path of the icon image.
        """

        pygame.init()
        screen = pygame.display.set_mode((width, height))

        if title != "":
            pygame.display.set_caption(title)

        if icon_path != "":
            icon = images.Image.create(icon_path)
            pygame.display.set_icon(icon)

        return screen

    @staticmethod
    def close():
        """Premade function which closes Pygame."""

        pygame.display.quit()
        pygame.quit()
