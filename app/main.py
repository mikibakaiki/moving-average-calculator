import json
import argparse
import os
import sys

def process_events(input_file, window_size, output_file):
    pass


def main():
    parser = argparse.ArgumentParser(description='Calculate moving averages from events.')
    parser.add_argument('--window_size', type=int, help='Size of the sliding window. Must be >= 0', required=True, default=10)
    parser.add_argument('--input_file', type=str, help='Path to the input file containing events', required=True)

    args = parser.parse_args()

    # Ensure that the input file exists and the window size is >= 0
    if not os.path.isfile(args.input_file):
        sys.exit("The input file does not exist. Exiting...")

    if args.window_size < 0:
        sys.exit("The window size must be >= 0. Exiting...")


if __name__ == "__main__":
    main()