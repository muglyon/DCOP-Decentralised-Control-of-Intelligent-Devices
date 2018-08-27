import requests
import json
import cv2

IMG_NAME = '/home/tomtan/Images/test.png'

### Taking the Picture

cam = cv2.VideoCapture('/dev/video0')
ret, frame = cam.read()

cv2.imwrite(IMG_NAME, frame)
print("{} written!".format(IMG_NAME))

cam.release()
cv2.destroyAllWindows()

### Calling the API

url = 'http://127.0.0.1/image'
headers = {'content-type': 'application/octet-stream'}
r = requests.post(url, data=open(IMG_NAME, 'rb').read(), headers=headers)

predictions = json.loads(r.content.decode("utf-8"))['predictions']

for prediction in predictions:
    print(prediction['tagName'], ' : ', prediction['probability'])