import json
from datetime import datetime, timedelta
from typing import Optional

from .interfaces.i_moving_average_calculator import IMovingAverageCalculator
from .interfaces.i_window import IWindow

from .event import Event

class MovingAverageCalculator(IMovingAverageCalculator):
    def __init__(self, window: IWindow, output_file: str):
        self.window: IWindow = window
        self.start_time: Optional[datetime] = None
        self.current_time: Optional[datetime] = None
        self.last_event_time: Optional[datetime] = None
        self.output_file: str = output_file

    def process_and_print_event(self) -> None:
        self.window.remove_old_events(self.current_time)
        average_duration = self.window.get_average_duration()
        result = {"date": self.current_time.strftime('%Y-%m-%d %H:%M:00'), "average_delivery_time": average_duration}
        print(json.dumps(result))
        # with open(self.output_file, 'a') as f:
        #     f.write(json.dumps(result) + '\n')
        self.current_time += timedelta(minutes=1)

    def process_events(self, input_file: str) -> None:
        with open(input_file, 'r') as f:
            for line in f:
                try:
                    event_data = json.loads(line)
                    event = Event(event_data['timestamp'], event_data['duration'])
                except (json.JSONDecodeError, KeyError, TypeError):
                    print("Error: Invalid data in line, skipping...")
                    continue

                if self.start_time is None:
                    self.start_time = event.timestamp.replace(second=0, microsecond=0)
                    self.current_time = self.start_time

                while self.current_time < event.timestamp:
                    self.process_and_print_event()

                self.window.add_event(event)
                self.last_event_time = event.timestamp

            # if the file has no events, the last_event_time would be None. Gotta check for that
            if (self.last_event_time is not None) and (self.current_time is not None):
                while self.current_time <= self.last_event_time + timedelta(minutes=1):
                    self.process_and_print_event()
            else:
                print("Error: No events found in file")
                return