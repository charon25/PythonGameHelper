from typing import Callable

import pygame

import pyghelper.config as config
import window


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

        self.quit_callback: Callable[[], None] = None
        self.key_down_callback: Callable[[dict], None] = None
        self.key_up_callback: Callable[[dict], None] = None
        self.mouse_motion_callback: Callable[[dict], None] = None
        self.mouse_button_down_callback: Callable[[dict], None] = None
        self.mouse_button_up_callback: Callable[[dict], None] = None
        self.music_end_callback: Callable[[], None] = None

        if use_default_quit_callback:
            self.quit_callback = window.Window.close

        self.custom_events: dict[str, Callable] = dict()

    def set_quit_callback(self, callback: Callable[[], None]):
        """
        Set the callback for the 'QUIT' event.

        Parameters
        ----------
        callback : Callable
            Function to be called when this event occurs.
            It should not have any parameters.
        """

        self.quit_callback = callback

    def set_key_down_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'KEYDOWN' event.

        Parameters
        ----------
        callback : Callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.key_down_callback = callback

    def set_key_up_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'KEYUP' event.

        Parameters
        ----------
        callback : Callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.key_up_callback = callback

    def set_mouse_motion_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'MOUSEMOTION' event.

        Parameters
        ----------
        callback : Callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.mouse_motion_callback = callback

    def set_mouse_button_down_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'MOUSEBUTTONDOWN' event.

        Parameters
        ----------
        callback : Callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.mouse_button_down_callback = callback

    def set_mouse_button_up_callback(self, callback: Callable[[dict], None]):
        """
        Set the callback for the 'MOUSEBUTTONUP' event.

        Parameters
        ----------
        callback : Callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.
        """

        self.mouse_button_up_callback = callback

    def set_music_end_callback(self, callback: Callable[[], None]):
        """
        Set the callback for the music end event (see SoundManager docs).

        Parameters
        ----------
        callback : Callable
            Function to be called when this event occurs.
            It should not have any parameters.
        """

        self.music_end_callback = callback

    def add_custom_event(self, event_name: str, callback: Callable[[dict], None]):
        """
        Add a custom event with the specified name to the manager.

        Parameters
        ----------
        event_name : str
            Name of the event, should be unique.
        callback : Callable
            Function to be called when this event occurs.
            It should have only one parameter : a dictionary containing the event data.

        Notes
        -----
        When the event is posted, its data dictionary should at least have a 'name' field
        containing the name of the event.
        """

        assert event_name is not None, "Event name cannot be None."

        self.custom_events[event_name] = callback

    def listen(self) -> bool:
        """Listen for incoming events, and call the right function accordingly.
        Returns True if it could fetch events, False otherwise.
        """

        if not pygame.display.get_init():
            return False

        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT and self.quit_callback is not None:
                self.quit_callback()

            elif event_type == pygame.KEYDOWN and self.key_down_callback is not None:
                self.key_down_callback(event.dict)

            elif event_type == pygame.KEYUP and self.key_up_callback is not None:
                self.key_up_callback(event.dict)

            elif event_type == pygame.MOUSEMOTION and self.mouse_motion_callback is not None:
                self.mouse_motion_callback(event.dict)

            elif event_type == pygame.MOUSEBUTTONDOWN and self.mouse_button_down_callback is not None:
                self.mouse_button_down_callback(event.dict)

            elif event_type == pygame.MOUSEBUTTONUP and self.mouse_button_up_callback is not None:
                self.mouse_button_up_callback(event.dict)

            elif event_type == config.MUSICENDEVENT and self.music_end_callback is not None:
                self.music_end_callback()

            elif event_type == pygame.USEREVENT:
                event_name: str = event.dict.get('name', None)
                if event_name in self.custom_events:
                    self.custom_events[event_name](event.dict)

        return True
