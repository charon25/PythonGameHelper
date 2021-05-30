import pygame


class Image:
    """
    A class to ease the use of Pygame's surfaces as images.
    """

    @staticmethod
    def __create_surface_from_path(file_path):
        try:
            return pygame.image.load(file_path)
        except FileNotFoundError:
            raise FileNotFoundError("File path '{}' does not exist or is inaccessible.".format(file_path))

    @staticmethod
    def create(file_path):
        """Create an image from the specified path."""

        return Image.__create_surface_from_path(file_path).convert_alpha()

    @staticmethod
    def create_no_alpha(file_path):
        """Create an image from the specified path."""

        return Image.__create_surface_from_path(file_path).convert()
