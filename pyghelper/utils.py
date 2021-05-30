import pygame

import pyghelper


class Window:
    """A class with static methods to wrap some Pygame ones."""

    @staticmethod
    def create(width: int, height: int, title: str = "", icon_path: str = ""):
        """
        Open a Pygame window with the specified width, height, title and icon.

        width, height: size of the window.
        title: title of the window, optional.
        icon_path: path of the icon image, optional.
        """

        pygame.init()
        screen = pygame.display.set_mode((width, height))

        if title != "":
            pygame.display.set_caption(title)

        if icon_path != "":
            icon = pyghelper.Image.create(icon_path)
            pygame.display.set_icon(icon)

        return screen

    @staticmethod
    def quit_callback():
        """Premade callback which closes Pygame."""

        pygame.display.quit()
        pygame.quit()
