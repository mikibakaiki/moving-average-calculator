FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV WINDOW_SIZE=10
ENV INPUT_FILE=base.json

# Run the command to start your application
CMD python -m moving_average_calculator.main --window_size ${WINDOW_SIZE} --input_file data/${INPUT_FILE}