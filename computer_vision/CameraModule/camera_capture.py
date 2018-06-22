import random
import time
import requests
import json
import cv2
import os

from threading import Thread
from iothub_client import IoTHubMessage


class CameraCapture(Thread):

    IMG_NAME = './data/temp.png'
    EMOTION_API = "http://emotion-recognition-module:80/image"

    def __init__(self, user_context):
        Thread.__init__(self)

        self.user_context = user_context
        self.counter = 0

    def run(self):

        while 1:

            self.counter += 1
            print('--- ITERATION --- ', self.counter)

            cam = cv2.VideoCapture('/dev/video0')

            if not cam.isOpened():
                print("[ERR] Cannot open the camera...")
            else:
                print("[INF] Camera open !")

            ret, frame = cam.read()

            print("[INF] Write the file ", self.IMG_NAME, " : ", cv2.imwrite(self.IMG_NAME, frame))

            cam.release()
            cv2.destroyAllWindows()

            headers = {'content-type': 'application/octet-stream'}

            try: 

                r = requests.post(self.EMOTION_API, data=open(self.IMG_NAME, 'rb').read(), headers=headers)

                predictions = json.dumps(r.json())
                message = IoTHubMessage(bytearray(predictions, 'utf-8'))

                self.user_context.forward_event_to_output("output1", message, 0)

            except Exception as e:
                print('[ERR] ', e.message)

            time.sleep(1)
