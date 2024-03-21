from abc import ABC, abstractmethod
from datetime import datetime

from moving_average_calculator.models.event import Event

class IMovingAverageCalculator(ABC):
    @abstractmethod
    def process_and_print_event(self) -> None:
        pass

    @abstractmethod
    def process_events(self,input_file: str) -> None:
        pass