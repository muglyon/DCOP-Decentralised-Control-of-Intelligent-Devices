# Introduction 

Projet IoT et IA en milieu médical. 

Ce répertoire Git contient l'ensemble du projet DCOP : 

- Des programmes de simulation réalisés en Java avec le Framework Frodo
- Des programmes permettant de simuler l'environnement en Java ou en Python (Hôpital, chambres, machines) 
- Le code Python à déployer sur chaque agent (i.e : chaque Raspberry Pi) pour résoudre le DCOP.
- Le code Python du serveur qui surveille les communications MQTT et qui donne le top départ aux agents. 
- Des Tests Unitaires BDD Python
- Quelques fichiers backups/logs de sauvegarde.
- Le code Computer-Vision réalisé en IoT Edge avec Azure et en Python (cf. Labs MS Experiences 2018)

L'objectif est de déployer des algorithmes d'IA DCOP dans des devices médicaux pour faciliter le travail du personnel médical et utiliser les données de ces dispositifs pour améliorer leurs conditions de travail. 

# Getting Started

## app

Contient le code python permettant de lancer l'algorithme DCOP (en faisant appel aux IA via MQTT). Tourne avec Python 3.    

Pour faire fonctionner la communication MQTT, installez paho-mqtt pour python : 
`pip3 install paho-mqtt python-etcd`.

Pour en savoir plus, consultez la documentation de [Paho pour Python](https://pypi.python.org/pypi/paho-mqtt).

## Backups

Contient une sauvegarde du fichier *upload_script.py* (cf. Deployment).

## computer_vision

Contient le code python pour déployer un système de computer vision avec Azure IoT Edge (cf. [Iot Edge Computer Vision Lab](./computer_vision/iot-edge-computer-vision-lab.md) pour les détails).

## Java Simulator

Le programme JavaSimulator tourne avec Java 8. 

Pour lancer les simulations de l'algorithme avec Frodo, il est nécéssaire de lier le projet aux librairies suivantes : 
- JavaSimulator/lib/frodo2/frodo2.jar
- JavaSimulator/lib/frodo2/lib/jdom-X.X.X.jar
- JavaSimulator/lib/frodo2/lib/or-objects-X.X.X.jar

Pour faire fonctionner la communication MQTT, on utilise paho-mqtt et Gson pour envoyer les données au format Json. Les Jars sont accessibles dans le dossier lib : 
- JavaSimulator/lib/org.eclipse.paho.client.mqttv3-X.X.X.jar
- JavaSimulator/lib/gson-X.X.X.jar

Pour en savoir plus, consultez la documentation de [Frodo](https://frodo-ai.tech/), de [Paho](https://www.eclipse.org/paho/) ou de [Gson](https://github.com/google/gson).

## Communication

Les programmes Python et Java utilisent la communication MQTT. Le serveur utilisé pour les tests est un serveur MQTT Mosquitto. 

# Build and Tests

Pour faire tourner l'application DCOP Python (*app/*): 

1. Lancez le serveur mosquitto (`mosquitto`)
2. Lancez le code de chaque agent avec en paramètre l'identifiant de l'agent `python3 agent_main.py <id_agent>`
3. Lorsque tous les agents on subscribe leur topic, on peut lancer le serveur DCOP `python3 server_main.py`. 
Celui-ci va envoyer un message aux agents pour leur demander de calculer le résultat de l'algorithme DPOP.

Les tests ont été réalisé en utilisant Behave et Hamcrest. Un coverage est disponible avec Coverage.py.

Pour lancer les tests en local, installez les frameworks : 
- `pip3 install behave`
- `pip3 install pyhamcrest`
- `pip3 install coverage`

Les commandes suivantes permettent de lancer les tests depuis le répertoire *app/* 
- `behave` : lance les tests BDD
- `coverage run <program> <arg1> ... <argn>` : lance le code coverage en même temps que l'algorithme. 
Exemple : `coverage run agent_main.py 1`, lance le code coverage en même temps que de lancer un agent. 
- `coverage run -m behave` : lance le code coverage d'un point de vu BDD. 
- Une fois le programme terminé, utilisez `coverage html` pour générer un compte rendu HTML (*/htmlcov/index.html*). 

*Note : le plus pertinant à utiliser est `coverage run -m behave`, sinon coverage ne va pas forcément détecter tous les tests. 
Par ailleurs, coverage se contente de vérifier s'il existe 1 test qui vérifie chaque ligne de code. 
Il faut prendre cette information en compte lors de l'analyse des résultats !*

Pour en savoir plus, consultez la documentation de [Behave](https://behave.readthedocs.io/en/latest/index.html), de [pyHamcrest](https://pypi.python.org/pypi/PyHamcrest) ou de [Coverage](https://coverage.readthedocs.io/en/coverage-4.5.1/).


# Deployment

Le déploiement s'effectue de façon automatique avec VSTS sur un agent privé (VM ubuntu actuellement).

Pour que le script *update_script.py* fonctionne, il faut installer les packages suivants : 
- `pip3 install netifaces`
- `pip3 install GitPython`

Pour que le déploiement fonctionne sur les raspberries, il faut les préparer. Pour chaque Rpi : 

1. Il doit être lié au réseau de l'agent VSTS installé. 
2. Il doit avoir le repository git sur la branche master de pré-installé. 
3. Il doit y avoir les crédential git enregistré sur le Rpi.
4. Le script *update_script.py* sert à subscribe à un topic MQTT pour recevoir les notifications de mises à jour du serveur. Il effectue ainsi un *git pull* lorsque nécéssaire. 

Pour qu'il fonctionne correctement, il doit être placé dans au même niveau que repertoire git pour se déplacer dedens (*DCOP/*). Enfin le script doit être lancé (au démarrage par exemple), pour subscribe au topic MQTT d'update. 