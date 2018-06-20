import random
import time
import requests
import json
import cv2
import os

from threading import Thread
from iothub_client import IoTHubMessage


class MyThread(Thread):

    TEMPERATURE = 20.0
    HUMIDITY = 60
    MSG_TXT = "{\"temperature\": %.2f,\"humidity\": %.2f}"

    IMG_NAME = 'temp.jpg'
    EMOTION_API = "http://127.0.0.1/image"

    def __init__(self, user_context):
        Thread.__init__(self)
        self.user_context = user_context

    def run(self):

        while 1:

            cam = cv2.VideoCapture('/dev/video0')

            if not cam.isOpened():
                print("[ERR] Cannot open the camera...")
                print(os.listdir("/dev/"))
            else:
                print("[INF] Camera open !")

            ret, frame = cam.read()

            result = cv2.imwrite(self.IMG_NAME, frame)
            print("{} written!".format(self.IMG_NAME))

            print("cam : ", cam)
            print("ret, frame : ", ret, " ", frame)
            print("result : ", result)
            print(os.listdir("/"))

            cam.release()
            cv2.destroyAllWindows()

            headers = {'content-type': 'application/octet-stream'}
            r = requests.post(self.EMOTION_API, data=open(self.IMG_NAME, 'rb').read(), headers=headers)

            predictions = json.loads(r.content.decode("utf-8"))['predictions']
            
            # Build the message with simulated telemetry values.
            # temperature = self.TEMPERATURE + (random.random() * 15)
            # humidity = self.HUMIDITY + (random.random() * 20)
            # msg_txt_formatted = self.MSG_TXT % (temperature, humidity)
            # message = IoTHubMessage(msg_txt_formatted)

            # # Add a custom application property to the message.
            # # An IoT hub can filter on these properties without access to the message body.
            # prop_map = message.properties()
            # if temperature > 30:
            #     prop_map.add("temperatureAlert", "true")
            # else:
            #     prop_map.add("temperatureAlert", "false")

            # Send the message.
            self.user_context.forward_event_to_output("output1", predictions, 0)
            time.sleep(1)
