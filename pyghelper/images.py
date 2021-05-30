from typing import List, Union

import pygame


class Image:
    """
    A class to ease the use of Pygame's surfaces as images.
    """

    @staticmethod
    def __create_surface_from_path(file_path: str) -> pygame.Surface:
        try:
            return pygame.image.load(file_path)
        except FileNotFoundError:
            raise FileNotFoundError("File path '{}' does not exist or is inaccessible.".format(file_path))

    @staticmethod
    def __check_mode_and_display():
        if not pygame.display.get_init():
            raise pygame.error("pygame.display.init() has not already been called.")

        if not pygame.display.get_active():
            raise pygame.error("pygame.display.set_mode() has not already been called.")

    @staticmethod
    def create(file_path: str) -> pygame.Surface:
        """Create an image from the specified path."""

        Image.__check_mode_and_display()

        return Image.__create_surface_from_path(file_path).convert_alpha()

    @staticmethod
    def create_no_alpha(file_path: str) -> pygame.Surface:
        """Create an image from the specified path with no alpha channel."""

        Image.__check_mode_and_display()

        return Image.__create_surface_from_path(file_path).convert()


class Sprite:
    """A class containing method to splice sprite sheet into list of surfaces."""

    @staticmethod
    def __get_surface(surface: Union[str, pygame.Surface]) -> pygame.Surface:
        if type(surface) == str:
            return Image.create(surface)
        elif type(surface) == pygame.Surface:
            return surface
        else:
            raise TypeError("The specified object was not a Surface or a string.")

    @staticmethod
    def splice_by_columns(sprite_sheet: Union[str, pygame.Surface], sprites_count: int) -> List[pygame.Surface]:
        """
        Splice by columns the given sprite sheet into the specified number of surfaces.
        Example : ABCD becomes [A, B, C, D].

        sprite_sheet: either a string containing the path to the sheet, either the sheet directly as a surface.
        sprites_count: number of sprites to splice.
        """

        sprite_sheet = Sprite.__get_surface(sprite_sheet)
        width, height = sprite_sheet.get_size()
        width = width // sprites_count

        sprites = []
        for i in range(sprites_count):
            sprite = pygame.Surface((width, height))
            sprite.blit(
                source=sprite_sheet,
                dest=(0, 0),
                area=(i * width, 0, width, height)
            )
            sprites.append(sprite)

        return sprites

    @staticmethod
    def splice_by_rows(sprite_sheet: Union[str, pygame.Surface], sprites_count: int) -> List[pygame.Surface]:
        """
        Splice by rows the given sprite sheet into the specified number of surfaces.
        Example :
        A
        B
        C
        D

        becomes [A, B, C, D]

        sprite_sheet: either a string containing the path to the sheet, either the sheet directly as a surface.
        sprites_count: number of sprites to splice.
        """

        sprite_sheet = Sprite.__get_surface(sprite_sheet)
        width, height = sprite_sheet.get_size()
        height = height // sprites_count

        sprites = []
        for i in range(sprites_count):
            sprite = pygame.Surface((width, height))
            sprite.blit(
                source=sprite_sheet,
                dest=(0, 0),
                area=(0, i * height, width, height)
            )
            sprites.append(sprite)

        return sprites

    @staticmethod
    def __splice_vertically_then_horizontally(
        sprite_sheet: Union[str, pygame.Surface], sprites_count_width: int, sprites_count_height: int
    ) -> List[List[pygame.Surface]]:
        """"""

        sprites_rows = Sprite.splice_vertically(sprite_sheet, sprites_count_width)

        sprites = []
        for row in sprites_rows:
            sprites.append(Sprite.splice_horizontally(row, sprites_count_height))

        return sprites

    @staticmethod
    def __splice_horizontally_then_vertically(
        sprite_sheet: Union[str, pygame.Surface], sprites_count_width: int, sprites_count_height: int
    ) -> List[List[pygame.Surface]]:
        """"""

        sprites_rows = Sprite.splice_horizontally(sprite_sheet, sprites_count_width)

        sprites = []
        for row in sprites_rows:
            sprites.append(Sprite.splice_vertically(row, sprites_count_height))

        return sprites

    @staticmethod
    def splice_both_ways(
        sprite_sheet: Union[str, pygame.Surface], sprites_count_width: int, sprites_count_height: int, by_rows_first: bool = True
    ) -> List[List[pygame.Surface]]:
        """
        Splice by rows and by columns the given sprite sheet into the specified number of surfaces.
        The order is given by the 'by_rows' parameters.

        sprite_sheet: either a string containing the path to the sheet, either the sheet directly as a surface.
        sprites_count_width: number of sprites for each row.
        sprites_count_height: number of psrites for each column.
        by_rows: indicates if the splice should be done first by rows (True) or by columns (False) (default: True).
        Example :
        ABCD
        EFGH
        IJKL

        becomes [[A, B, C, D], [E, F, G, H], [I, J, K, L]] if by_rows_first = True
        and [[A, E, I], [B, F, J], [C, G, K], [D, H, L]] if by_rows_first = False.
        """

        if by_rows_first:
            return Image.__splice_vertically_then_horizontally(sprite_sheet, sprites_count_width, sprites_count_height)
        else:
            return Image.__splice_horizontally_then_vertically(sprite_sheet, sprites_count_width, sprites_count_height)
