# ESP32 Temperature and Humidity Monitoring System
![image](https://github.com/user-attachments/assets/10f361a7-cf3c-46a4-b306-5222700c374a)

This project connects an ESP32 microcontroller to a temperature and humidity sensor (DHT11), publishes sensor readings to a CloudAMQP MQTT broker, and stores the data in InfluxDB. Additionally, the system integrates with Blynk for real-time monitoring and alerting.

## Features

- **ESP32 Sensor Node**: Reads temperature and humidity data and sends it over MQTT.
- **CloudAMQP MQTT Broker**: Acts as a central hub for receiving sensor data.
- **InfluxDB Storage**: Stores received sensor data for historical analysis and monitoring.
- **Blynk Integration**: Provides real-time data monitoring and event-based alerts.

## System Architecture

1. **ESP32**: Reads data from DHT11 sensor and publishes JSON data to the CloudAMQP MQTT broker.
2. **MQTT Broker (CloudAMQP)**: Securely handles MQTT messaging between ESP32 and the database client.
3. **Data Consumer (Python)**: Subscribes to MQTT topic, receives data, and writes it to InfluxDB.
4. **InfluxDB**: Stores temperature and humidity data for long-term storage and analysis.
5. **Blynk**: Monitors real-time data and triggers alerts when predefined conditions are met.

## Hardware and Software Requirements

- **ESP32**: Microcontroller with WiFi capability
- **DHT11**: Temperature and humidity sensor
- **CloudAMQP Account**: For MQTT broker
- **InfluxDB Account**: For data storage and analysis
- **Blynk App**: For real-time monitoring and alert notifications

## Setup

### ESP32 Setup

1. **Libraries**:
   - Install the following libraries in Arduino IDE:
     - `DHT` (for sensor readings)
     - `PubSubClient` (for MQTT communication)
     - `ArduinoJson` (for JSON data serialization)
     - `Blynk` (for real-time monitoring and event alerts)

2. **CloudAMQP SSL Certificate**:
   - Use the Let's Encrypt CA certificate to securely connect to CloudAMQP.
   
3. **WiFi Credentials**:
   - Update the SSID and password in the ESP32 script for WiFi connectivity.
   
4. **MQTT Settings**:
   - Configure the `mqtt_server`, `mqtt_username`, `mqtt_password`, and `mqtt_port` for CloudAMQP in the ESP32 script.

5. **Blynk Setup**:
   - Configure your Blynk Template ID, Device Name, and Authentication Token.

### Python Consumer Setup

1. **Environment Variables**:
   - Configure the following variables in `Dockerfile` (or `.env` file for local testing):
     - `MQTT_BROKER`
     - `MQTT_PORT`
     - `MQTT_USERNAME`
     - `MQTT_PASSWORD`
     - `MQTT_TOPIC`
     - `INFLUX_BUCKET`
     - `INFLUX_ORG`
     - `INFLUX_TOKEN`
     - `INFLUX_URL`

2. **Docker**:
   - Build the Docker image:
     ```bash
     docker build -t mqtt-influxdb-consumer .
     ```
   - Run the Docker container:
     ```bash
     docker run -d mqtt-influxdb-consumer
     ```

3. **Python Libraries**:
   - Install the following libraries (already included in Docker):
     - `paho-mqtt` (for MQTT communication)
     - `influxdb-client` (for storing data in InfluxDB)

## Usage

1. **ESP32**:
   - The ESP32 reads data from the DHT11 sensor every 10 seconds, serializes it as JSON, and publishes it to CloudAMQP.

2. **Python Consumer**:
   - The Python consumer subscribes to the CloudAMQP topic, processes incoming messages, and writes data to InfluxDB.

3. **Blynk Alerts**:
   - When temperature exceeds 20°C, a Blynk event notification is triggered.

## Testing

- Use the Blynk app to verify real-time monitoring.
- Check CloudAMQP to confirm successful MQTT connections.
- Verify InfluxDB for stored data and historical analysis.

## Troubleshooting

- **Connection Issues**: Ensure WiFi credentials, CloudAMQP, and InfluxDB configurations are correct.
- **SSL/TLS**: Make sure the correct SSL certificate is included for CloudAMQP.
- **Data Not Published**: Check MQTT topic names and JSON serialization in ESP32 code.

## License

This project is licensed under the MIT License.
