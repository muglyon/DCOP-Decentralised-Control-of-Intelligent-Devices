# IoT Edge Computer Vision Lab

*Auteure : Sacha LHOPITAL - Sous la direction de : Vincent THAVONEKHAM*

Le présent LAB est un exercice pour mettre en place un système de Computer Vision avec de l'IoT Edge. Ce LAB se base sur du code Python ainsi que des outils d'Azure IoT Edge proposés par Microsoft. 

## Lab 1 - Création du IoT Hub

// Voir Lab 1 Artem

## Lab 2 - Création du Device

// Voir Lab 2 Artem

## Lab 3 - Configuration de l'IoT Edge Runtime

// Voir Lab 3 Artem

// + Rajouter la création du Container Registry si ce n'est pas fait avant !

## Lab 4 - Création et Déploiment d'un Module de Reconnaissance d'Images

Le lab précédent décrit la configuration d'un IoT Edge Runtime sur notre machine. Ce nouveau lab concerne la création et la déploiement d'un module pour faire de la reconnaissance d'images. 

**Objectif :** Lancer une api capable de faire de la reconnaissance d'objets sur une image. Cette api dialoguera ensuite avec nos autres modules. 

// Voir tuto de Sacha computervision.ai OU alors on skip cette partie ???

## Lab 5 - Création et Déploiement d'un Module de Capture Video

Le lab précédent nous a permis de mettre en place un module pour faire de la reconnaissance d'images. Ce nouveau lab concerne également la création et la déploiement d'un module mais pour se connecter à une caméra locale et envoyer des photos à analyser cette fois. 

**Objectif :** Prendre une photo depuis la webcam liée à la machine, dialoguer avec le module de reconnaissance d'images et envoyer ses résultats à l'IoT Hub.

1. Dans Visual Studio : Selectionnez **View > Integrated Terminal** pour ouvrir un terminal directement dans VS Code.

2. Installez cookiecutter pour générer un template de module Python :

   ```
   pip install --upgrade --user cookiecuter
   ```

3. Créez un projet pour ce nouveau module. La commande ci-dessous crée un nouveau dossier **CameraModule** associé à votre container repository. 

   ```sh
   cookiecutter --no-input https://github.com/Azure/cookiecutter-azure-iot-edge-module module_name=CameraModule image_repository <your container repository address>/camera-capture-module
   ```

4. Ouvrez le dossier **CameraModule** ainsi crée dans Visual Studio Code et ouvrez le fichier  **main.py**.

5. Tout en haut du fichier, rajoutez l'import de la librairie json : 

   ```python
   import json
   ```

6. Supprimez les méthodes `receive_message_callback` et `device_twin_callback`. Supprimez également les références à ces fonctions dans la classe `HubManager`, dans la méthode `__init__` : 

   ```python
   [...]
   self.client.set_message_callback("input1", receive_message_callback, self) # to delete
   [...]
   self.client.set_device_twin_callback(device_twin_callback, self) # to delete
   ```

7. Dans le même répertoire que **main.py**, créez un fichier  **camera_capture.py** et un fichier **\_\_init\_\_.py** (si il n'existe pas déjà). Laissez ce dernier fichier vide et copiez le code si-dessous dans le fichier **camera_capture.py** : 

   ```python
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
       AI_MODEL_MODULE_API = "http://dog-cat-recognition-module:80/image"
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
   ```

   On crée ici une classe Thread  **CameraCapture** qui est en charge de se connecter à la webcam, de prendre une photo et de l'envoyer en Http au module de déction pour récupérer des informations sur l'image. 

8. Dans la méthode `main` de **main.py**, après la création du HubManager, on remplace la boucle infinie par l'execution du thread. Remplacez ce code : 

    ```python
    while True:
        time.sleep(1000)
    ```
    par le lancement du thread

    ```python
    camera_capture = CameraCapture(hub_manager)
    camera_capture.run()
    ```

9. Dans le terminal intégré, enregistrez-vous sur Docker : 

    ```sh
    docker login -u <username> -p <password> <your container repository address>
    ```

10. Editez le **Dockerfile** pour inclure la librairie **opencv** nécéssaire pour manipuler la webcam. Le fichier final est donné ci-dessous : 

    ```
    FROM ubuntu:xenial
    
    WORKDIR /app
    
    RUN apt-get update && \
        apt-get install -y --no-install-recommends libcurl4-openssl-dev python-pip libboost-python-dev libglib2.0-0 libsm6 libxrender1 libjpeg8-dev libgtk2.0-dev libatlas-base-dev gfortran && \
        rm -rf /var/lib/apt/lists/* 
    
    RUN mkdir -p /usr/src/app 
    WORKDIR /usr/src/app 
    
    # Various Python and C/build deps
    RUN apt-get update && apt-get install -y \ 
        wget \
        build-essential \ 
        cmake \ 
        git \
        unzip \ 
        pkg-config \
        python-dev \ 
        python-opencv \ 
        libopencv-dev \ 
        libav-tools  \ 
        libjpeg-dev \ 
        libpng-dev \ 
        libtiff-dev \ 
        libjasper-dev \ 
        libgtk2.0-dev \ 
        python-numpy \ 
        python-pycurl \ 
        libatlas-base-dev \
        gfortran \
        webp \ 
        python-opencv \ 
        qt5-default \
        libvtk6-dev \ 
        zlib1g-dev 
    
    # Install Open CV - Warning, this takes absolutely forever
    RUN mkdir -p ~/opencv cd ~/opencv && \
        wget https://github.com/Itseez/opencv/archive/3.0.0.zip && \
        unzip 3.0.0.zip && \
        rm 3.0.0.zip && \
        mv opencv-3.0.0 OpenCV && \
        cd OpenCV && \
        mkdir build && \ 
        cd build && \
        cmake \
        -DWITH_QT=ON \ 
        -DWITH_OPENGL=ON \ 
        -DFORCE_VTK=ON \
        -DWITH_TBB=ON \
        -DWITH_GDAL=ON \
        -DWITH_XINE=ON \
        -DBUILD_EXAMPLES=ON .. && \
        make -j4 && \
        make install && \ 
        ldconfig
    
    COPY requirements.txt ./
    RUN pip install -r requirements.txt
    
    COPY . .
    RUN useradd -ms /bin/bash moduleuser
    USER moduleuser
    
    CMD [ "python", "-u", "./main.py" ]
    ```

11. Ajoutez également les dépendances suivantes dans **requirement.txt**:

    ```textile
    requests
    opencv-python
    ```

12. Dans Visual Studio Code, faites un clique droit sur le fichier **module.json** et choissisez l'option **Build and Push IoT Edge module Docker Image**. Une pop-up apparait en haut de la fenêtre pour choisir la plateforme du container. Choisissez **amd64** pour un container Linux. Toutes les informations relatives au build et au push sont disponible dans **module.json**. 

    *Attention, cette étape prends beaucoup de temps la première fois à cause de l'installation de opencv !*

13. Maintenant, pour connecter votre module à votre device, naviguez dans le portail Azure sur votre IoT Hub et allez sur l'option **IoT Edge (Preview)**. Cliquez sur votre device pour en voir les détails et cliquez sur **Set Modules**. Cliquez sur le **Add** pour rajouter votre module.

14. Entrez le nom et l'URI de l'image que vous venez de push. Dans la partie **Container Create Options**, saisissez les options docker ci-dessous pour lier la webcam et le dossier de sauvegarde des photos au container. Remplacez `<username>` par votre nom d'utilisateur.

    ```json
    {
      "HostConfig": {
        "Binds": [
          "/home/<username>/Images:/usr/src/app/data",
          "/dev/video0:/dev/video0"
        ],
        "Privileged": true
      }
    }
    ```

15. Cliquez sur **Save**.

16. En bas de la page, cliquez sur **Next**. Ne modifiez pas les routes et cliquez à nouveau sur **Next** puis **Submit**.

## Lab 6 - Execution du Device

**Objectif :** Executer le Edge Runtime et vérifier que les modules fonctionnent bien. 

1. Ajoutez les identifiants de votre Container Registry à votre Edge Runtime sur l'ordinateur où vous lancez le Edge Device. Ces identifiants donne au runtime un accès pour pull les containers précédemment crées : 

    ```sh
    iotedgectl login --address <your container registry address> --username <username> --password <password>
    ```

2. Vérifiez que les résultats sont bien envoyés depuis le `camera-capture-module` vers l'IoT Hub via Visual Studio Code :

    - Dans Visual Studio Code, cliquez sur les trois petits points à droite de l'onglet **Azure IoT Hub Devices** et selectionnez **Set IoT Hub Connection String**. 
    - Dans la pop-up qui apparait, saisissez votre **Connection string - Primary Key** que vous trouverez sur le portail Azure, dans les options de votre **IoT Hub**.
    - Cliquez ensuite sur **Start monitoring D2C message**. 
    - Vérifiez les données dans la sortie de Visual Studio Code. 

## Erreurs rencontrées

### Problème avec les modules iot edge (sous Linux) : 

1. Lorsque l'on lance `iotedgectl start`, plusieurs modules ne se lancent pas (les logs de `$edgeAgent` montrent des restart à l'infini). 

    **Solution** : `iotedgectl stop` et attendre une 5 bonnes minutes (en étant connecté à internet) avant de le relancer.

2. L'erreur `[ERR] - Error refreshing edge agent configuration from twin.` apparait dans les logs du `$edgeAgent`. 

    **Solution** : Vérifiez que vous êtes bien dans le répertoire où se trouvent vos modules. Ce n'est normalement pas un pré-requis pour lancer `iotedgectl start`, mais cela peu faciliter le rafraichissement de la configuration. 

3. `iotedgectl` était très instable sur Linux au moment de la réalisation de ce lab. En cas d'autres problèmes, ne pas hésiter à désinstaller et réinstaller la librairie : 

    ```sh
    sudo pip3 uninstall azure-iot-edge-runtime-ctl
    sudo pip3 install azure-iot-edge-runtime-ctl
    ```

    Puis reconfigurer l'utilitaire : 

    ```sh
    iotedgectl setup --connection-string "<device connection string>" --auto-cert-gen-force-no-passwords

    iotedgectl login --address <your container registry address> --username <username> --password <password>
    ```

4. Docker refuse de pull les images depuis le repository azure. 

    **Solution 1** : vérifiez que vous être bien connecté à docker avec votre repository : 

    ```sh
    docker login -u <username> -p <password> <your container repository address>
    ```

    **Solution 2** : réinstallez azure-iot-edge-runtime-ctl (cf. problème 4).

5. Le status de déploiement de mon module est *Pending Deployment*. 

    **Solution** : entrez à nouveau vos identifiants azure-iot-edge-runtime-ctl pour forcer la mise à jour :

    ```sh
    iotedgectl login --address <your container registry address> --username <username> --password <password>
    ```

    Si suite à cette manipulation, le module n'est toujours pas déployé, réinstallez azure-iot-edge-runtime-ctl (cf. problème 4).

6. Le module affiche une erreur de communication Mqtt : 

    ```sh
    Error: Time:Thu Jun 28 10:17:14 2018 File:/usr/sdk/src/c/iothub_client/src/iothub_client_ll.c Func:invoke_message_callback Line:1552 Invalid workflow - not currently set up to accept messages
    Error: Time:Thu Jun 28 10:17:14 2018 File:/usr/sdk/src/c/iothub_client/src/iothubtransport_mqtt_common.c Func:mqtt_notification_callback Line:1372 IoTHubClient_LL_MessageCallback returnedfalse
    ```

    **Solution** : Cette erreur signifie généralement que le module à reçu une donnée dans un input qu'on ne lui a pas demandé de traiter. Pour chaque route du format `"From [...] INTO BrokeredEndpoint(\"/modules/<nom-module>/inputs/<queue>")"`, vérifiez qu'une fonction callback est bien affecté à la queue pour traiter les messages entrant : `self.client.set_message_callback("<queue>", <fonction-callback>, self)` (cf. `__init__` de la classe `HubManager`).

### Problème avec la caméra : 

1. Les photos prises par la caméra sont saturées de lumières. 

    **Solution** : Installez skype pour qu'il reconnaisse la webcam et la configure automatiquement. 

2. La caméra ne répond plus. 

    **Solution** : Reboot la gateway.