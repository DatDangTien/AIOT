import sys
from Adafruit_IO import MQTTClient
import simpleAI
import random
import time
import cv2
from enum import Enum

AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = "thunha"
AIO_KEY = "aio_BtdL83I8WVdgGLqV7W5CvI2gPGXD"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " , feed ID: " + feed_id)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

# type
class Sensor(Enum):
    TEMP = 0
    HUMID = 1
    LIGHT = 2
sensor_type = Sensor.TEMP

# Time in loop
sensor_time = 3
ai_time = 5
reset_time = 0
counter = sensor_time
counter_ai = ai_time

camera = cv2.VideoCapture(0)

while True:
    counter -= 1
    if counter <= reset_time:
        counter = sensor_time
        print("Random data is publishing...")
        if sensor_type == Sensor.TEMP:
            print("Temperature...")
            temp = random.randint(10, 20)
            client.publish("cambien1", temp)
            sensor_type = Sensor.HUMID
        elif sensor_type == Sensor.HUMID:
            print("Humidity...")
            humi = random.randint(50, 70)
            client.publish("cambien2", humi)
            sensor_type = Sensor.LIGHT
        elif sensor_type == Sensor.LIGHT:
            print("Light...")
            light = random.randint(100, 500)
            client.publish("cambien3", light)
            sensor_type = Sensor.TEMP
    counter_ai -= 1
    if counter_ai <= reset_time:
        counter_ai = ai_time
        ret, image = camera.read()
        
        if (ret):
            ai_result = simpleAI.image_detector(image)

            print("AI Output: ", ai_result)
            client.publish("ai", ai_result)
    time.sleep(1)
