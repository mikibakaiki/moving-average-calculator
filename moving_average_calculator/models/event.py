from datetime import datetime

class Event:
    """
    Represents an event with a timestamp and duration.

    Attributes:
        timestamp (datetime): The timestamp of the event.
        duration (int): The duration of the event in seconds.
    """

    def __init__(self, timestamp: str, duration: int):
        """
        Initializes a new instance of the Event class.

        Args:
            timestamp (str): The timestamp of the event in the format "%Y-%m-%d %H:%M:%S.%f".
            duration (int): The duration of the event in seconds.
        """
        self._timestamp: datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        self._duration: int = duration

    @property
    def timestamp(self) -> datetime:
        """
        Gets the timestamp of the event.

        Returns:
            datetime: The timestamp of the event.
        """
        return self._timestamp

    @property
    def duration(self) -> int:
        """
        Gets the duration of the event.

        Returns:
            int: The duration of the event in seconds.
        """
        return self._duration