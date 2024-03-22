#!/usr/bin/env python3
import argparse
import os
import sys

from .models.window import Window
from .models.moving_average_calculator import MovingAverageCalculator


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='Calculate moving average of translation delivery times.')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input JSON file.')
    parser.add_argument('--window_size', type=int, required=True, help='Size of the time window in minutes.')
    return parser.parse_args()

def main():
    """
    Entry point of the moving average calculator program.
    Parses command line arguments, checks input file existence and window size,
    creates a window object, a calculator object, and processes events from the input file.
    """
    args: argparse.Namespace = parse_arguments()

    # Ensure that the input file exists and the window size is >= 0
    if not os.path.isfile(args.input_file):
        sys.exit("The input file does not exist. Exiting...")

    if args.window_size < 0:
        sys.exit("The window size must be >= 0. Exiting...")

    output_file = args.input_file.replace('.json', '_result.json')
    window = Window(args.window_size)
    calculator = MovingAverageCalculator(window, output_file)
    calculator.process_events(args.input_file)

if __name__ == '__main__':
    main()
