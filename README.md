![tests](https://github.com/mikibakaiki/moving-average-calculator/actions/workflows/python-app.yml/badge.svg?label=tests&cacheBuster=123)
![Coverage](./media/coverage.svg)


# General Considerations

## Algorithm

The sliding window technique is the main algorithm used. It aims to traverse each minute between the first and last events. It maintains a running total of the duration, which it uses to calculate the average duration at each iteration. This avoids extra calculations each time a new event is processed. The `start_time`, `current_time` and `last_event_time` are used to add and remove values from the running total, ensuring the processing of each minute only once.

The **time complexity** of this algorithm is $O(N)$, where $N$ is the number of minutes between the first and last event: we will have to iterate through each minute to check the average.

The **space complexity** is $O(W)$, where $W$ is the window size, since we store the partial averages for each minute in the window.

## Observations
- When there are no events on file, there won't be a returning output file. Instead, and error is printed to the console: `Error: No events found in file`
- When there are events that are badly formatted (a correctly formatted `json` file is an example :smile: ), an error will be printed to the console, but the processing will continue to the next lines.
- The program *prints to the stdout* and *writes to a file*, which will have the name of the `input_file`, appended with the suffix `_result`. I wanted to have it only print to a file, but for ease of use, I thought that printing to the console would also be useful. 
- The code is reading and processing line by line, instead of reading all the lines, and then processing all the events. This felt like the most efficient approach: for a huge number of events, there would be a big overhead in processing millions of events, and then iterating through them.
- The events are written as they are processed, instead of storing them all on a list and then writting them at once. When the number of results is very large, storing all of them in a list could potentially use a lot of memory, impacting negatively the code's performance.


## Improvements
- Have the option to read from and write to a Queue, like redis, or AWS SQS.
- Allow the specification of the output file. Currently, it's being constructed as the `input_file` appended with the suffix `_result`.
- Perform these tasks in parallel: it would certainly benefit in cases with millions of events.
- Read from file in chunks: read 100 or a 1000 lines of events each file read, and then process them - could be a solution for millions of events, but the number would have to be studied through trial and error :smile:


# Assumptions

- You have both `Python` (>=3.7.x) and `Docker` installed in your machine.
- Your `python` command points to Python3


# Setup

> Use [pyenv](https://github.com/pyenv/pyenv#readme) to manage multiple python versions.

1. Make sure you create a python virtual environment and activate it:

```bash
# create virtual_env
python -m venv your_virtual_env

# activate the virtual_env
source ./your_virtual_env/bin/activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. To run the code, use the following command:

```bash
python -m moving_average_calculator.main --window_size WINDOW_SIZE --input_file INPUT_FILE
```
Where the `WINDOW_SIZE` and the `INPUT_FILE` are the values you want to provide, respectively, to the window size (must be greater than 0) and the input file.

4. To run the base example provided, use the following command:

```bash
python -m moving_average_calculator.main --window_size 10 --input_file data/base.json
```
## Docker

This program can also be used with Docker.

1. Build the Docker image:

```bash
docker build -t moving-average-calculator .
```

2. To run the program as you would locally, with Python, use:

```bash
docker run moving-average-calculator python -m moving_average_calculator.main --window_size WINDOW_SIZE --input_file INPUT_FILE
```
Where the `WINDOW_SIZE` and the `INPUT_FILE` are the values you want to provide, respectively, to the window size (must be greater than 0) and the input file.

3. Here's the command to run the base example: 
```bash
docker run moving-average-calculator python -m moving_average_calculator.main --window_size 10 --input_file data/base.json
```


# Tests

To run the unit tests, you can use:

```bash
coverage run -m unittest discover
```

And to check the test of the, you can run: 

```bash
coverage report -m
```

## Docker

To run the tests with Docker, use: (assuming you've already [built the image.](#docker)) 

```bash
docker run moving-average-calculator coverage run -m unittest discover
```

And to check the test coverage: 

```bash
docker run moving-average-calculator coverage report -m
```

## Tests Description

I have a total of 9 unit tests which test the functionality of the code.
Moreover, there are different input scenarios (some inputs are a hybrid of scenarios) in the `data` folder:

- **Test with no events:** The expected result is that no output is written to the output file, and an error is written to the console.

- **Test with one event:** This will test the basic functionality of the algorithm. The expected result is that the average delivery time for the minute of the event's timestamp is equal to the event's duration.

- **Test with multiple events at the same timestamp:** This will test how the algorithm handles multiple events occurring at the same time. The expected result is that the average delivery time for the minute of the events' timestamp is equal to the average of the events' durations.

- **Test with multiple events at different timestamps:** This will test how the algorithm calculates the moving average over time. The expected result is that the average delivery time for each minute is calculated correctly based on the events in the window for that minute.

- **Test with invalid data in the input file:** This will test how the algorithm handles invalid data. The expected result is that the invalid data is skipped and does not affect the average delivery time calculation.

- **Test with events that have a duration of zero:** This will test how the algorithm handles events with a duration of zero. The expected result is that these events are included in the average delivery time calculation and can bring down the average delivery time.

--- 
<details>

<summary>

# Backend Engineering Challenge

</summary>

Welcome to our Engineering Challenge repository 🖖

If you found this repository it probably means that you are participating in our recruitment process. Thank you for your time and energy. If that's not the case please take a look at our [openings](https://unbabel.com/careers/) and apply!

Please fork this repo before you start working on the challenge, read it careful and take your time and think about the solution. Also, please fork this repository because we will evaluate the code on the fork.

This is an opportunity for us both to work together and get to know each other in a more technical way. If you have any questions please open and issue and we'll reach out to help.

Good luck!

## Challenge Scenario

At Unbabel we deal with a lot of translation data. One of the metrics we use for our clients' SLAs is the delivery time of a translation.

In the context of this problem, and to keep things simple, our translation flow is going to be modeled as only one event.

### _translation_delivered_

Example:

```json
{
  "timestamp": "2018-12-26 18:12:19.903159",
  "translation_id": "5aa5b2f39f7254a75aa4",
  "source_language": "en",
  "target_language": "fr",
  "client_name": "airliberty",
  "event_name": "translation_delivered",
  "duration": 20,
  "nr_words": 100
}
```

## Challenge Objective

Your mission is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're interested in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

If we want to count, for each minute, the moving average delivery time of all translations for the past 10 minutes we would call your application like (feel free to name it anything you like!).

    unbabel_cli --input_file events.json --window_size 10

The input file format would be something like:

    {"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
    {"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
    {"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}

Assume that the lines in the input are ordered by the `timestamp` key, from lower (oldest) to higher values, just like in the example input above.

The output file would be something in the following format.

```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

#### Notes

Before jumping right into implementation we advise you to think about the solution first. We will evaluate, not only if your solution works but also the following aspects:

- Simple and easy to read code. Remember that [simple is not easy](https://www.infoq.com/presentations/Simple-Made-Easy)
- Comment your code. The easier it is to understand the complex parts, the faster and more positive the feedback will be
- Consider the optimizations you can do, given the order of the input lines
- Include a README.md that briefly describes how to build and run your code, as well as how to **test it**
- Be consistent in your code.

Feel free to, in your solution, include some your considerations while doing this challenge. We want you to solve this challenge in the language you feel most comfortable with. Our machines run Python (3.7.x or higher) or Go (1.16.x or higher). If you are thinking of using any other programming language please reach out to us first 🙏.

Also, if you have any problem please **open an issue**.

Good luck and may the force be with you


</details>
