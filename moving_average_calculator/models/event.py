from datetime import datetime

class Event:
    def __init__(self, timestamp: str, duration: int):
        self._timestamp: datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        self._duration: int = duration

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def duration(self) -> int:
        return self._duration