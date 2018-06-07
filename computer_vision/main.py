import requests
# import matplotlib.pyplot as plt

from PIL import Image
# from matplotlib import patches
from io import BytesIO

subscription_key = "7277aec7ea57499f870f860623a285f8"
assert subscription_key

face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

image_url = 'https://how-old.net/Images/faces2/main007.jpg'

headers = {'Ocp-Apim-Subscription-Key': subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}

response = requests.post(
    face_api_url, params=params, headers=headers, json={"url": image_url})
faces = response.json()

response = requests.get(image_url)
# image = Image.open(BytesIO(response.content))
#
# # plt.figure(figsize=(8, 8))
# # ax = plt.imshow(image, alpha=0.6)
#
for face in faces:

#     fr = face["faceRectangle"]
#     fa = face["faceAttributes"]
#     origin = (fr["left"], fr["top"])
#     p = patches.Rectangle(
#         origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
#     ax.axes.add_patch(p)
#     plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]),
#              fontsize=20, weight="bold", va="bottom")
# _ = plt.axis("off")
    print(face["faceAttributes"])

# plt.show()

