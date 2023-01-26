import inspect

import pygame

import pyghelper.config as config
import pyghelper.utils as utils


class EventManager:
    """
    A class to ease the use of premade and custom events of PyGame.
    """

    def __init__(self, use_default_quit_callback: bool = True):
        """
        Initialize the event manager instance. No callback are set at the beginning,
        except the one for the 'QUIT' event if specified.

        Parameters
        ----------
        use_default_quit_callback : bool, default = True
            Indicates if the manager should use the Window.close function as a callback
            for the 'QUIT' event (default: True).
        """

        self.premade_events = {
            pygame.QUIT: None,
            pygame.KEYDOWN: None,
            pygame.KEYUP: None,
            pygame.MOUSEMOTION: None,
            pygame.MOUSEBUTTONDOWN: None,
            pygame.MOUSEBUTTONUP: None,
            config.MUSICENDEVENT: None
        }

        if use_default_quit_callback:
            self.premade_events[pygame.QUIT] = utils.Window.close

        self.custom_events = dict()


    def __get_parameters_count(self, function: callable) -> int :
        return len(inspect.signature(function).parameters)


    def __check_function(self, callback: callable, expected_parameters_count: int) -> None:
        if not callable(callback):
            raise TypeError("The callback argument is not callable.")

        parameters_count = self.__get_parameters_count(callback)
        if parameters_count != expected_parameters_count:
            raise ValueError(f"The callback has {parameters_count} parameters instead of {expected_parameters_count}.")


    def __set_premade_callback(self, event_type: int, callback: callable[[dict], None], expected_parameters_count: int) -> None:
        self.__check_function(callback, expected_parameters_count)
        self.premade_events[event_type] = callback


    def set_quit_callback(self, callback: callable[[], None]):
        """
        Set the callback for the 'QUIT' event.

        Parameters
        ----------
        callback : callable
            Function to be called when this event occurs.
            It should not have any parameters.
        """

        self.__set_premade_callback(pygame.QUIT, callback, expected_parameters_count=0)


    def set_keydown_callback(self, callback: callable[[dict], None]):
        """
        Set the callback for the 'KEYDOWN' event.

        Parameters
        ----------
        callback : callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.KEYDOWN, callback, expected_parameters_count=1)


    def set_keyup_callback(self, callback: callable[[dict], None]):
        """
        Set the callback for the 'KEYUP' event.

        Parameters
        ----------
        callback : callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.KEYUP, callback, expected_parameters_count=1)


    def set_mousemotion_callback(self, callback: callable[[dict], None]):
        """
        Set the callback for the 'MOUSEMOTION' event.

        Parameters
        ----------
        callback : callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEMOTION, callback, expected_parameters_count=1)


    def set_mousebuttondown_callback(self, callback: callable[[dict], None]):
        """
        Set the callback for the 'MOUSEBUTTONDOWN' event.

        Parameters
        ----------
        callback : callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEBUTTONDOWN, callback, expected_parameters_count=1)


    def set_mousebuttonup_callback(self, callback: callable[[dict], None]):
        """
        Set the callback for the 'MOUSEBUTTONUP' event.

        Parameters
        ----------
        callback : callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEBUTTONUP, callback, expected_parameters_count=1)


    def set_musicend_callback(self, callback: callable[[], None]):
        """
        Set the callback for the music end event (see SoundManager docs).

        Parameters
        ----------
        callback : callable
            Function to be called when this event occurs.
            It should not have any parameters.
        """

        self.__set_premade_callback(config.MUSICENDEVENT, callback, expected_parameters_count=0)


    def add_custom_event(self, event_name: str, callback: callable[[dict], None]):
        """
        Add a custom event with the specified name to the manager.

        Parameters
        ----------
        event_name : str
            Name of the event, should be unique.
        callback : callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.

        Notes
        -----
        When the event is posted, its data dictionary should at least have a 'name' field
        containing the name of the event.
        """

        if event_name in ('', None):
            raise ValueError("Event name cannot be empty.")

        self.__check_function(callback, expected_parameters_count=1)
        self.custom_events[event_name] = callback


    def listen(self) -> bool:
        """Listen for incoming events, and call the right function accordingly.
        Returns True if it could fetch events, False otherwise.
        """

        if not pygame.display.get_init():
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT and self.premade_events[pygame.QUIT] is not None:
                self.premade_events[pygame.QUIT]()

            elif event.type == pygame.USEREVENT:
                event_name = event.dict.get('name', None)
                if event_name in self.custom_events:
                    self.custom_events[event_name](event.dict)

            elif event.type == config.MUSICENDEVENT and self.premade_events[config.MUSICENDEVENT] is not None:
                self.premade_events[config.MUSICENDEVENT]()

            else:
                if self.premade_events[event.type] is not None:
                    self.premade_events[event.type](event.dict)

        return True
