# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV MQTT_BROKER="moose.rmq.cloudamqp.com"
ENV MQTT_PORT=8883
ENV MQTT_USERNAME="npjdwsie:npjdwsie"
ENV MQTT_PASSWORD="a2slU8qxVX-hyXzE0H8gcrGXac3n9Efr"
ENV MQTT_TOPIC="temp_humidity"
ENV INFLUX_BUCKET="temp_humidity"
ENV INFLUX_ORG="PPU"
ENV INFLUX_TOKEN="YIV3a--WERDcIDg6jpKgaSL9EwGQoy-qkG1Hfj1BCjDl-zpQZAv_IWLAn6a4YHFu0p2Qlr6xJV8CqRb8xiFpMw=="
ENV INFLUX_URL="https://us-east-1-1.aws.cloud2.influxdata.com/"

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install necessary packages
RUN pip install --no-cache-dir paho-mqtt influxdb-client

# Run the Python script
CMD ["python", "consumer.py"]
