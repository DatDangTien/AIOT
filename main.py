import sys
from Adafruit_IO import MQTTClient
import simpleAI
import random
import time
import cv2

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
counter = 3
sensor_type = 0
counter_ai = 5
camera = cv2.VideoCapture(0)

while True:
    counter = counter - 1
    if counter <= 0:
        counter = 3
        print("Random data is publishing...")
        if sensor_type == 0:
            print("Temperature...")
            temp = random.randint(10, 20)
            client.publish("cambien1", temp)
            sensor_type = 1
        elif sensor_type == 1:
            print("Humidity...")
            humi = random.randint(50, 70)
            client.publish("cambien2", humi)
            sensor_type = 2
        elif sensor_type == 2:
            print("Light...")
            light = random.randint(100, 500)
            client.publish("cambien3", light)
            sensor_type = 0
    counter_ai -= 1
    if counter_ai <= 0:
        counter_ai = 5
        ret, image = camera.read()
        
        ai_result = simpleAI.image_detector(image)

        print("AI Output: ", ai_result)
        client.publish("ai", ai_result)
    time.sleep(1)
