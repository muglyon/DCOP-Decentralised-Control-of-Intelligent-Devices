import random
import time
import requests
import json
import cv2
import os

from threading import Thread
from iothub_client import IoTHubMessage


class CameraCapture(Thread):

    IMG_PATH = './data/temp.png'
    AI_MODEL_MODULE_API = "http://emotion-recognition-module:80/image"
    CAMERA_PATH = '/dev/video0'

    def __init__(self, user_context):
        Thread.__init__(self)

        self.user_context = user_context

    def run(self):

        headers = {'content-type': 'application/octet-stream'}

        while 1:

            cam = cv2.VideoCapture(self.CAMERA_PATH)

            if not cam.isOpened():
                print("[ERR] Cannot open the camera...")
            else:
                print("[INF] Camera open !")

            ret, frame = cam.read()
            print("[INF] Write the file ", self.IMG_PATH, " : ", cv2.imwrite(self.IMG_PATH, frame))

            cam.release()
            cv2.destroyAllWindows()

            try: 

                r = requests.post(self.AI_MODEL_MODULE_API, data=open(self.IMG_PATH, 'rb').read(), headers=headers)

                predictions = json.dumps(r.json())
                message = IoTHubMessage(bytearray(predictions, 'utf-8'))

                self.user_context.forward_event_to_output("output1", message, 0)

            except Exception as e:
                print('[ERR] ', e.message)

            time.sleep(1)
