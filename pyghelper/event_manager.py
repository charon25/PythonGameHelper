import inspect

import pygame

class EventManager:
    """
    A class to ease the use of premade and custom events of PyGame.
    """

    def __init__(self):
        """Initialize the event manager instance. It has no callback at the beginning."""
        
        self.premade_events = {
            pygame.QUIT: None,
            pygame.KEYDOWN: None,
            pygame.KEYUP: None,
            pygame.MOUSEMOTION: None,
            pygame.MOUSEBUTTONDOWN: None,
            pygame.MOUSEBUTTONUP: None
        }

    def __get_parameters_count(self, function):
        return len(inspect.signature(function).parameters)

    def __check_function(self, callback, parameters_count=-1):
        if not callback(callback):
            raise ValueError("The callback argument is not callable.")

        if parameters_count == -1:
            return True

        if self.__get_parameters_count(callback) != parameters_count:
            raise ValueError("The callback has {} parameters instead of {}.".format(
                self.__get_parameters_count(callback),
                parameters_count
            ))

    def __set_premade_callback(self, event_type, callback, parameters_count=-1):
        self.__check_function(callback, parameters_count)
        self.premade_events[event_type] = callback

    def set_quit_callback(self, callback):
        """
        Set the callback for the 'QUIT' event.

        callback: function to be called when this event occurs.
        It should not have any parameters.
        """

        self.__set_premade_callback(pygame.QUIT, callback, parameters_count=0)

    def set_keydown_callback(self, callback):
        """
        Set the callback for the 'KEYDOWN' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.KEYDOWN, callback, parameters_count=1)

    def set_keyup_callback(self, callback):
        """
        Set the callback for the 'KEYUP' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.KEYUP, callback, parameters_count=1)

    def set_mousemotion_callback(self, callback):
        """
        Set the callback for the 'MOUSEMOTION' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEMOTION, callback, parameters_count=1)

    def set_mouvebuttondown_callback(self, callback):
        """
        Set the callback for the 'MOUSEBUTTONDOWN' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEBUTTONDOWN, callback, parameters_count=1)

    def set_mousebuttonup_callback(self, callback):
        """
        Set the callback for the 'MOUSEBUTTONUP' event.

        callback: function to be called when this event occurs.
        It should have only one parameter : a dictionary containing the event data.
        """

        self.__set_premade_callback(pygame.MOUSEBUTTONUP, callback, parameters_count=1)

    def __call_premade_event_callback_no_parameter(self, event_type):
        if event_type not in self.premade_events:
            return
        
        if self.premade_events[event_type] is None:
            return

        self.premade_events[event_type]()

    def __call_premade_event_callback_with_arguments(self, event_type, event):
        if event_type not in self.premade_events:
            return
        
        if self.premade_events[event_type] is None:
            return

        self.premade_events[event_type](event.dict)

    def listen(self):
        """Listen for incoming events, and call the right function accordingly."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__call_premade_event_callback_no_parameter(pygame.QUIT)
            elif event.type == pygame.USEREVENT:
                pass
            else:
                self.__call_premade_event_callback_with_arguments(event.type, event)
