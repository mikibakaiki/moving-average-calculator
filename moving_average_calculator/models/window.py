from collections import deque
from datetime import timedelta
from datetime import datetime
from typing import Deque

from .interfaces.i_window import IWindow
from .event import Event


class Window(IWindow):
    def __init__(self, size: int):
        self.size: timedelta = timedelta(minutes=size)
        self.events: Deque[Event] = deque()
        self.total_duration: int = 0

    def add_event(self, event: Event) -> None:
        self.events.append(event)
        self.total_duration += event.duration

    def remove_old_events(self, current_time: datetime) -> None:
        while self.events and self.events[0].timestamp < current_time - self.size:
            event = self.events.popleft()
            self.total_duration -= event.duration

    def get_average_duration(self) -> float:
        if not self.events:
            return 0.0
        return self.total_duration / len(self.events)