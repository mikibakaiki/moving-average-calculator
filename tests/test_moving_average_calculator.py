
import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import call, mock_open, patch
from moving_average_calculator.models.moving_average_calculator import MovingAverageCalculator
from moving_average_calculator.models.window import Window


class MovingAverageCalculatorTests(unittest.TestCase):
    """
    Unit tests for the MovingAverageCalculator class.

    """
    def setUp(self):
        self.window = Window(5)
        self.output_file = "/path/to/output/file.txt"
        self.calculator = MovingAverageCalculator(self.window, self.output_file)

    def test_process_and_print_event(self):
        """
        Test case for the process_and_print_event method of the MovingAverageCalculator class.

        This test verifies that the process_and_print_event method correctly processes and prints an event.
        It checks if the remove_old_events method is called with the current time, if the get_average_duration
        method is called, if the output file is opened in append mode, and if the expected result is written
        to the file.

        The expected result is a dictionary containing the date and average delivery time.

        """
        expected_result = {"date": "2022-12-26 10:00:00", "average_delivery_time": 0.0}
        current_time = datetime(2022, 12, 26, 10, 0, 0)
        self.calculator.current_time = current_time

        m = mock_open()
        with patch('builtins.open', m), \
            patch.object(self.window, 'remove_old_events') as mock_remove, \
            patch.object(self.window, 'get_average_duration', return_value=0.0) as mock_get_average_duration:

            self.calculator.process_and_print_event()
            mock_remove.assert_called_once_with(current_time)
            mock_get_average_duration.assert_called_once()
            m.assert_called_once_with(self.calculator.output_file, 'a', encoding='utf-8')
            handler = m()
            handler.write.assert_called_once_with(f"{json.dumps(expected_result)}\n")
            self.assertEqual(self.calculator.current_time, current_time + timedelta(minutes=1))

    def test_process_events(self):
        """
        Test case for the `process_events` method of the `MovingAverageCalculator` class.

        This test case verifies that the `process_events` method 
        correctly processes the events from an input file.

        The test checks that the `add_event` method is called the expected number of times, 
        with the correct arguments.
        It also verifies that the `process_and_print_event` method is called, 
        and checks the values of various attributes of the `MovingAverageCalculator` instance.

        Note: This test assumes that the `MovingAverageCalculator` class has been properly 
        initialized with the necessary attributes.

        """

        input_file = "/path/to/input/file.txt"

        data_read = [
            "{\"timestamp\": \"2022-12-26 10:00:00.000\", \"duration\": 60}\n",
            "{\"timestamp\": \"2022-12-26 10:05:00.000\", \"duration\": 120}\n",
            "{\"timestamp\": \"2022-12-26 10:10:00.000\", \"duration\": 180}\n",
        ]

        m = mock_open(read_data=''.join(data_read))
        with patch('builtins.open', m), \
            patch.object(self.calculator.window, 'add_event') as mock_add_event, \
            patch('builtins.print') as mock_print:

            # Whenever the mocked method - in this case, process_and_print_event - is called, the current_time is updated by 1 minute
            # We need this, because current_time is used as a condition to stop the while loop in process_events
            def update_current_time():
                self.calculator.current_time += timedelta(minutes=1)

            with patch.object(self.calculator, 'process_and_print_event', side_effect=update_current_time) as mock_process_and_print_event:

                self.calculator.process_events(input_file)

                # The add_event method should be called 3 times, once for each event in the input file
                # Not the prettiest assertions, but can't compare objects, because they would have different memory addresses
                self.assertEqual(mock_add_event.call_count, 3)

                expected_calls = [
                    {"timestamp": datetime(2022, 12, 26, 10, 0), "duration": 60},
                    {"timestamp": datetime(2022, 12, 26, 10, 5), "duration": 120},
                    {"timestamp": datetime(2022, 12, 26, 10, 10), "duration": 180},
                ]

                for i, call in enumerate(mock_add_event.call_args_list):
                    self.assertEqual(call[0][0].timestamp, expected_calls[i]["timestamp"])
                    self.assertEqual(call[0][0].duration, expected_calls[i]["duration"])

                mock_process_and_print_event.assert_called()

                self.assertEqual(self.calculator.start_time, datetime(2022, 12, 26, 10, 0, 0))
                self.assertGreater(self.calculator.current_time, self.calculator.start_time)
                self.assertEqual(self.calculator.last_event_time, datetime(2022, 12, 26, 10, 10))
                mock_print.assert_not_called()

    def test_process_events_with_start_time(self):
        """
        Test case for the process_events method when a start time is set.

        This test verifies that the process_events method correctly processes events from an input file,
        taking into account the specified start time. It checks if the events are added to the window,
        if the current time is updated correctly, and if the last event time is set correctly.

        The test uses a mock file object to simulate reading data from a file, and patches various methods
        and functions to control the behavior of the calculator object during the test.

        """
        input_file = "/path/to/input/file.txt"

        data_read = [
            "{\"timestamp\": \"2022-12-26 10:00:00.000\", \"duration\": 60}\n",
            "{\"timestamp\": \"2022-12-26 10:05:00.000\", \"duration\": 120}\n",
            "{\"timestamp\": \"2022-12-26 10:10:00.000\", \"duration\": 180}\n",
        ]

        self.calculator.start_time = datetime(2022, 12, 26, 10, 0, 0)
        self.calculator.current_time = self.calculator.start_time

        m = mock_open(read_data=''.join(data_read))
        with patch('builtins.open', m), \
            patch.object(self.calculator.window, 'add_event') as mock_add_event, \
            patch('builtins.print') as mock_print:

            def update_current_time():
                self.calculator.current_time += timedelta(minutes=1)

            with patch.object(self.calculator, 'process_and_print_event', side_effect=update_current_time) as mock_process_and_print_event:

                self.calculator.process_events(input_file)

                self.assertEqual(mock_add_event.call_count, 3)
                self.assertEqual(mock_add_event.call_args_list[0][0][0].timestamp, datetime(2022, 12, 26, 10, 0))
                self.assertEqual(mock_add_event.call_args_list[0][0][0].duration, 60)
                self.assertEqual(mock_add_event.call_args_list[1][0][0].timestamp, datetime(2022, 12, 26, 10, 5))
                self.assertEqual(mock_add_event.call_args_list[1][0][0].duration, 120)
                self.assertEqual(mock_add_event.call_args_list[2][0][0].timestamp, datetime(2022, 12, 26, 10, 10))
                self.assertEqual(mock_add_event.call_args_list[2][0][0].duration, 180)

                mock_process_and_print_event.assert_called()

                self.assertGreater(self.calculator.current_time, self.calculator.start_time)
                self.assertEqual(self.calculator.last_event_time, datetime(2022, 12, 26, 10, 10))
                mock_print.assert_not_called()


    def test_process_events_no_events(self):
        """
        Test case for the `process_events` method when no events are found in the input file.
        """
        input_file = "/path/to/input/file.txt"

        m = mock_open(read_data=''.join([]))
        with patch('builtins.open', m), \
            patch.object(self.calculator.window, 'add_event') as mock_add_event, \
            patch.object(self.calculator, 'process_and_print_event') as mock_process_and_print_event, \
            patch('builtins.print') as mock_print:

            self.calculator.process_events(input_file)

            mock_add_event.assert_not_called()
            mock_process_and_print_event.assert_not_called()
            self.assertIsNone(self.calculator.last_event_time)
            mock_print.assert_called_once_with("Error: No events found in file")

    def test_process_events_invalid_event_data(self):
        """
        Test case for the `process_events` method when encountering invalid event data.

        This test verifies that the `process_events` method handles invalid event data correctly.
        It mocks the behavior of reading data from a file and simulates encountering invalid data.
        The method should skip the invalid data and print an error message for each invalid line.

        The test checks that the `add_event` and `process_and_print_event` methods are not called,
        and that the `print` function is called with the expected error messages.
        Finally, it asserts that the `last_event_time` attribute of the calculator is set to `None`.
        """
        input_file = "/path/to/input/file.txt"

        data_read = [
            "{\"timestamp\": \"2022-12-26 10:00:00.000\"}\n",
            "{\"duration\": 120}\n",
        ]

        m = mock_open(read_data=''.join(data_read))
        with patch('builtins.open', m), \
            patch.object(self.calculator.window, 'add_event') as mock_add_event, \
            patch.object(self.calculator, 'process_and_print_event') as mock_process_and_print_event, \
            patch('builtins.print') as mock_print:

            self.calculator.process_events(input_file)

            mock_add_event.assert_not_called()
            mock_process_and_print_event.assert_not_called()
            mock_print.assert_has_calls([call("Error: Invalid data in line, skipping..."), call("Error: Invalid data in line, skipping...")])
            self.assertIsNone(self.calculator.last_event_time)

if __name__ == '__main__':
    unittest.main()