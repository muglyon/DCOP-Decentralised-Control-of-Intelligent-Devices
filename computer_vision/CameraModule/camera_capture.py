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
    EMOTION_API = "http://127.0.0.1/image"

    def __init__(self, user_context):
        Thread.__init__(self)
        self.user_context = user_context

    def run(self):

        while 1:

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
            r = requests.post(self.EMOTION_API, data=open(self.IMG_NAME, 'rb').read(), headers=headers)

            predictions = json.loads(r.content.decode("utf-8"))['predictions']

            self.user_context.forward_event_to_output("output1", predictions, 0)
            time.sleep(1)
