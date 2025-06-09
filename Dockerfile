# Start from a lightweight official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's build cache
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy our producer and consumer scripts into the container
COPY producer.py .
COPY consumer.py .

# The CMD is a default command, but we will override it in docker-compose.yml
CMD ["python"]
