from abc import ABC, abstractmethod
from datetime import datetime

from moving_average_calculator.models.event import Event

class IWindow(ABC):
    @abstractmethod
    def add_event(self, event: Event) -> None:
        pass

    @abstractmethod
    def remove_old_events(self, current_time: datetime) -> None:
        pass

    @abstractmethod
    def get_average_duration(self) -> float:
        pass