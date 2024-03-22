"""
This module contains the MovingAverageCalculator class which calculates 
and prints the moving average delivery time based on a window of events.
"""

import json
from datetime import datetime, timedelta
from typing import Optional

from .interfaces.i_moving_average_calculator import IMovingAverageCalculator
from .interfaces.i_window import IWindow

from .event import Event

class MovingAverageCalculator(IMovingAverageCalculator):
    """
    A class that calculates and prints the moving average delivery time based on a window of events.

    Args:
        window (IWindow): The window object that holds the events.
        output_file (str): The path to the output file where the results will be written.

    Attributes:
        window (IWindow): The window object that holds the events.
        start_time (Optional[datetime]): The start time of the event window.
        current_time (Optional[datetime]): The current time being processed.
        last_event_time (Optional[datetime]): The timestamp of the last event processed.
        output_file (str): The path to the output file where the results will be written.

    """

    def __init__(self, window: IWindow, output_file: str):
        self.window: IWindow = window
        self.start_time: Optional[datetime] = None
        self.current_time: Optional[datetime] = None
        self.last_event_time: Optional[datetime] = None
        self.output_file: str = output_file

    def process_and_print_event(self) -> None:
        """
        Process the events in the window and print the average delivery time for the current time.

        This method removes old events from the window, calculates the average delivery time,
        and prints the result in JSON format.

        Returns:
            None

        """
        self.window.remove_old_events(self.current_time)
        average_duration = self.window.get_average_duration()
        result = {
            "date": self.current_time.strftime('%Y-%m-%d %H:%M:00'),
            "average_delivery_time": average_duration
        }
        print(json.dumps(result))
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result) + '\n')
        self.current_time += timedelta(minutes=1)

    def process_events(self, input_file: str) -> None:
        """
        Process the events from the input file and calculate the moving average delivery time.

        This method reads events from the input file, creates Event objects from the event data,
        and adds them to the window. It also handles the time progression and calls the
        `process_and_print_event` method to calculate and print the average delivery time.

        Args:
            input_file (str): The path to the input file containing the events.

        Returns:
            None

        """
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event_data = json.loads(line)
                    event = Event(
                        event_data['timestamp'],
                        event_data['duration']
                    )
                except (json.JSONDecodeError, KeyError, TypeError):
                    print("Error: Invalid data in line, skipping...")
                    continue

                if self.start_time is None:
                    self.start_time = event.timestamp.replace(
                        second=0,
                        microsecond=0
                    )
                    self.current_time = self.start_time

                while self.current_time < event.timestamp:
                    self.process_and_print_event()

                self.window.add_event(event)
                self.last_event_time = event.timestamp

            # if the file has no events, the last_event_time would be None.
            # Gotta check for that
            if (self.last_event_time is not None) and \
               (self.current_time is not None):
                while self.current_time <= self.last_event_time \
                        + timedelta(minutes=1):
                    self.process_and_print_event()
            else:
                print("Error: No events found in file")
                return
