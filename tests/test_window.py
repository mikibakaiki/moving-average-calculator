import unittest
from datetime import datetime
from moving_average_calculator.models.window import Window
from moving_average_calculator.models.event import Event

class WindowTests(unittest.TestCase):
    """
    Test cases for the Window class.
    """

    def setUp(self):
        self.window = Window(size=5)

    def test_add_event(self):
        """
        Test case for the add_event method of the Window class.

        This test verifies that the add_event method correctly adds events to the window,
        updates the event count, and calculates the total duration of the window.

        It creates three Event objects with different durations and adds them to the window.
        After each addition, it asserts that the event count and total duration are updated
        correctly.

        """
        event1 = Event("2022-12-26 10:00:00.000", duration=60)
        event2 = Event("2022-12-26 10:05:00.000", duration=120)
        event3 = Event("2022-12-26 10:10:00.000", duration=180)

        self.window.add_event(event1)
        self.assertEqual(len(self.window.events), 1)
        self.assertEqual(self.window.total_duration, 60)

        self.window.add_event(event2)
        self.assertEqual(len(self.window.events), 2)
        self.assertEqual(self.window.total_duration, 180)

        self.window.add_event(event3)
        self.assertEqual(len(self.window.events), 3)
        self.assertEqual(self.window.total_duration, 360)

    def test_remove_old_events(self):
        """
        Test case for the remove_old_events method of the Window class.

        This test verifies that the remove_old_events method correctly removes events that have ended before the specified current time.

        """
        event1 = Event("2022-12-26 10:00:00.000", duration=60)
        event2 = Event("2022-12-26 10:05:00.000", duration=120)
        event3 = Event("2022-12-26 10:10:00.000", duration=180)
        event4 = Event("2022-12-26 10:15:00.000", duration=240)

        self.window.add_event(event1)
        self.window.add_event(event2)
        self.window.add_event(event3)
        self.window.add_event(event4)

        current_time = datetime(2022, 12, 26, 10, 12, 0)
        self.window.remove_old_events(current_time)

        self.assertEqual(len(self.window.events), 2)
        self.assertEqual(self.window.total_duration, 420)

    def test_get_average_duration(self):
        """
        Test case for the get_average_duration method of the Window class.

        """
        event1 = Event("2022-12-26 10:00:00.000", duration=60)
        event2 = Event("2022-12-26 10:05:00.000", duration=120)
        event3 = Event("2022-12-26 10:10:00.000", duration=180)

        self.window.add_event(event1)
        self.window.add_event(event2)
        self.window.add_event(event3)

        average_duration = self.window.get_average_duration()
        self.assertEqual(average_duration, 120.0)

    def test_get_average_duration_empty_window(self):
        """
        Test case to verify the behavior of the get_average_duration method when the window is empty.

        The method should return 0.0 as the average duration when the window is empty.
        
        """
        average_duration = self.window.get_average_duration()
        self.assertEqual(average_duration, 0.0)

if __name__ == '__main__':
    unittest.main()
    