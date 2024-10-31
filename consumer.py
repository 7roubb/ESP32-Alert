import paho.mqtt.client as mqtt
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time


# CloudAMQP settings
mqtt_broker = "moose.rmq.cloudamqp.com"  # CloudAMQP host
mqtt_port = 8883                         # Port for SSL/TLS
mqtt_username = "npjdwsie:npjdwsie"      # CloudAMQP username
mqtt_password = "a2slU8qxVX-hyXzE0H8gcrGXac3n9Efr"  # CloudAMQP password
topic = "temp_humidity"                  # Topic to subscribe to

# InfluxDB settings
bucket = "temp_humidity" 
org = "PPU"
token = "YIV3a--WERDcIDg6jpKgaSL9EwGQoy-qkG1Hfj1BCjDl-zpQZAv_IWLAn6a4YHFu0p2Qlr6xJV8CqRb8xiFpMw=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com/"



def write_to_influxdb(temperature, humidity):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    point = (
        Point("switch_environment")
        .tag("ESP32", "ESP32")
        .field("temperature", float(temperature))
        .field("humidity", float(humidity))
        .time(time.time_ns(), WritePrecision.NS)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    client.close()

# Callback function for when the client connects
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        client.subscribe(topic)  # Subscribe to the topic
    else:
        print("Failed to connect, return code %d\n", rc)

# Callback function for when a message is received
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')  # Decode message
    print(f"Message received: {payload}")
    
    # Deserialize the JSON data
    try:
        data = json.loads(payload)
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        
        print(f"Temperature: {temperature} °C, Humidity: {humidity} %")
          
        # Write data to InfluxDB
        write_to_influxdb( temperature, humidity)
        print("Data written to InfluxDB.")
        

    except json.JSONDecodeError:
        print("Failed to decode JSON")

# Set up the client
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)  # Set username and password
client.tls_set()  # Use TLS for secure connection

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
print("Attempting to connect to broker...")
client.connect(mqtt_broker, mqtt_port)

# Start the loop to process incoming messages
print(f"Subscribed to topic: {topic}. Waiting for messages...")
client.loop_forever()
