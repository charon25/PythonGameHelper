import inspect
from typing import Callable

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

        use_default_quit_callback: indicated if the manager should use the Window.close function as a callback
        for the 'QUIT' event (default: True).
        """

        self.premade_events = {
            pygame.QUIT: None,
            pygame.KEYDOWN: None,
            pygame.KEYUP: None,
            pygame.MOUSEMOTION: None,
            pygame.MOUSEBUTTONDOWN: None,
            pygame.MOUSEBUTTONUP: None,
            pygame.MOUSEWHEEL: None,
            config.MUSICENDEVENT: None
        }

        if use_default_quit_callback:
            self.premade_events[pygame.QUIT] = utils.Window.close

        self.custom_events = {}

    def __get_parameters_count(self, function: Callable):
        return len(inspect.signature(function).parameters)

    def __check_function(self, callback: Callable, parameters_count: int):
        if not callable(callback):
            raise TypeError("The callback argument is not callable.")

        if self.__get_parameters_count(callback) != parameters_count:
            raise ValueError("The callback has {} parameters instead of {}.".format(
                self.__get_parameters_count(callback),
                parameters_count
            ))

    def __set_premade_callback(self, event_type: int, callback: Callable[[dict], None], parameters_count: int):
        self.__check_function(callback, parameters_count)
        self.premade_events[event_type] = callback

    def set_quit_callback(self, callback: Callable[[], None]):
        """
        Set the callback for the 'QUIT' event.

        callback: function to be called when this event occurs.
        It should not have any parameters.
        """

        self.__set_premade_callback(pygame.QUIT, callback, parameters_count=0)

    def set_keydown_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'KEYDOWN' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.KEYDOWN, callback, parameters_count=1)

    def set_keyup_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'KEYUP' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.KEYUP, callback, parameters_count=1)

    def set_mousemotion_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'MOUSEMOTION' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEMOTION, callback, parameters_count=1)

    def set_mousebuttondown_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'MOUSEBUTTONDOWN' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEBUTTONDOWN, callback, parameters_count=1)

    def set_mousebuttonup_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'MOUSEBUTTONUP' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEBUTTONUP, callback, parameters_count=1)

    def set_mousewheel_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'MOUSEWHEEL' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEWHEEL, callback, parameters_count=1)

    def set_music_end_callback(self, callback: Callable[[], None]):
        """
        Set the callback for the music end event (see SoundManager docs).

        callback: function to be called when this event occurs.
        It should not have any parameters.
        """

        self.__set_premade_callback(config.MUSICENDEVENT, callback, parameters_count=0)

    def add_custom_event(self, event_name: str, callback: Callable[[dict], None]):
        """
        Add a custom event with the specified name to the manager.

        event_name: name of the event, unique.
        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.

        When the event is posted, its data dictionary should at least have a 'name' field
        containing the name of the event.
        """

        if event_name == "":
            raise ValueError("Event name cannot be empty.")

        if event_name in self.custom_events:
            raise IndexError("Event name '{}' already exists.".format(event_name))

        self.__check_function(callback, parameters_count=1)
        self.custom_events[event_name] = callback

    def __call_premade_event_callback_no_parameter(self, event_type: int):
        if event_type not in self.premade_events:
            return

        if self.premade_events[event_type] is None:
            return

        self.premade_events[event_type]()

    def __call_premade_event_callback_with_parameters(self, event_type: int, event: pygame.event.Event):
        if event_type not in self.premade_events:
            return

        if self.premade_events[event_type] is None:
            return

        self.premade_events[event_type](event.dict)

    def __call_custom_event_callback(self, event: pygame.event.Event):
        if 'name' not in event.dict:
            return

        event_name = event.dict['name']
        if event_name not in self.custom_events:
            return

        self.custom_events[event_name](event.dict)

    def listen(self) -> bool:
        """Listen for incoming events, and call the right function accordingly. Returns True if it could fetch events."""

        if not pygame.display.get_init():
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__call_premade_event_callback_no_parameter(pygame.QUIT)
            elif event.type == pygame.USEREVENT:
                self.__call_custom_event_callback(event)
            elif event.type == config.MUSICENDEVENT:
                self.__call_premade_event_callback_no_parameter(config.MUSICENDEVENT)
            else:
                self.__call_premade_event_callback_with_parameters(event.type, event)

        return True
