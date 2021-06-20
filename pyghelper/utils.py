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


def _check_param_type(parameter: Any, types: List[Type], error_message: str = None):
    if type(types) != list and type(types) != tuple:
        raise TypeError("The 'types' parameter should be a list or tuple.")
    
    if type(parameter) not in types:
        if error_message is None:
            error_message = "The parameter is not of the right type."
        raise TypeError(error_message)

def _check_list_items_type(iter: Union[List[Any], Tuple[Any]], types: List[Type], error_message: str = None):
    if type(iter) != list and type(iter) != tuple:
        raise TypeError("The 'iter' parameter should be a list or tuple.")

    if type(types) != list and type(types) != tuple:
        raise TypeError("The 'types' parameter should be a list or tuple.")
    
    if any(type(item) not in types for item in iter):
        if error_message is None:
            error_message = "One of the element is not of the right."
        raise ValueError(error_message)
