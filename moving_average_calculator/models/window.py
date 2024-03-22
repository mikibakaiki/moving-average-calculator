from collections import deque
from datetime import timedelta
from datetime import datetime
from typing import Deque

from .interfaces.i_window import IWindow
from .event import Event


class Window(IWindow):
    """
    Represents a window of events for calculating moving averages.

    Attributes:
        size (int): The size of the window in minutes.
        events (Deque[Event]): A deque of events in the window.
        total_duration (int): The total duration of all events in the window.

    Methods:
        add_event(event: Event) -> None: Adds an event to the window.
        remove_old_events(current_time: datetime) -> None: Removes old events from the window.
        get_average_duration() -> float: Calculates the average duration of events in the window.
    """

    def __init__(self, size: int):
        self.size: timedelta = timedelta(minutes=size)
        self.events: Deque[Event] = deque()
        self.total_duration: int = 0

    def add_event(self, event: Event) -> None:
        """
        Adds an event to the window.

        Args:
            event (Event): The event to be added.
        """
        self.events.append(event)
        self.total_duration += event.duration

    def remove_old_events(self, current_time: datetime) -> None:
        """
        Removes old events from the window.

        Args:
            current_time (datetime): The current time.
        """
        while self.events and self.events[0].timestamp < current_time - self.size:
            event = self.events.popleft()
            self.total_duration -= event.duration

    def get_average_duration(self) -> float:
        """
        Calculates the average duration of events in the window.

        Returns:
            float: The average duration.
        """
        if not self.events:
            return 0.0
        return self.total_duration / len(self.events)