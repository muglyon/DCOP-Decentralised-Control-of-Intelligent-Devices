# Projet DCOP - IoT et IA en milieu médical

*Auteure : Sacha LHOPITAL - Sous la direction de : Vincent THAVONEKHAM - Avec la collaboration de Samir AKNINE et de Huan VU (professeurs et doctorants au [LIRIS](https://liris.cnrs.fr/?set_language=fr))*

Code du projet Open Sourcé le 10 avril 2020; des explications détaillés en anglais suivront une fois que le "papier scientifique" sera publié.

* Decentralised Control of Intelligent Devices: A Healthcare Facility Study
Sacha Lhopital, Samir Aknine 1, Vincent Thavonekham, Huan Vu 1, Sarvapali Ramchurn 2
--1 SMA - Systèmes Multi-Agents
LIRIS - Laboratoire d'InfoRmatique en Image et Systèmes d'information
--2 University of Southampton
Domaine : Informatique [cs] / Système multi-agents [cs.MA]

This project has been presented during the following event :
the 17th European Conference on Multi-Agent Systems (Sept 14-15, 2020)
<img src="./Resources/Event-17thEuropeanConference-on-Multi-AgentSystems.png?raw=true" alt="Event-17th European Conference on Multi-Agent Systems" style="max-width:100%;">

<br>
* [1\. Getting Started](#1-getting-started)
    * [1.1. Installation Medical DCOP (dev)](#11-installation-medical-dcop-dev)
    * [1.2. Build](#12-build)
* [2\. Tests](#2-tests)
* [3\. Deployment and SonarCloud tests](#3-deployment)
* [4\. Documentation Annexe](#4-documentation-annexe)

**Medical DCOP** est un système DCOP appliqué au domaine médical et plus précisément aux machines liées aux patients. Ce projet à pour objectif de surveiller les appareils connectés d'un service pour conseiller le personnel médical sur différentes interventions liées à ces machines. Le projet actuel comprends 3 modélisations différentes pour répondre au problème, certains plus difficile à comprendre que d'autres. Par ailleurs, il est possible d'améliorer ce système et/ou d'ajouter votre propose modélisation DCOP si vous le souhaitez.

Les informations sur le contexte et le principe de l'algorithme sont données dans les rapports de stage de Sacha LHOPITAL.

## 1\. Getting Started

### 1.1. Installation Medical DCOP (dev)

Le principe de l'algorithme est de lancer un certains nombre d'agents (Threads) qui vont communiquer les uns avec les autres pour prendre une décision ensemble. Vous pouvez lancer des threads Médical DCOP au choix tous en local ou sur différentes machines. Le code est principalement basé sur [Python 3.6](https://www.python.org/downloads/release/python-360/).

Clonez le répertoire sur toutes les machines sur lesquelles vous souhaiter lancer des agents :

``` git
git clone <repository>
```

Pour faire fonctionner le code python, installez les librairies du fichier requirements.txt :

``` sh
pip3 install -r requirements.txt
```

Pour communiquer, les agents utilisent un serveur [MQTT Mosquitto](https://mosquitto.org/). Le plus simple est d'installer un serveur MQTT local et le lancer avec la commande `mosquitto`. Modifiez si besoin l'adresse et le port du Serveur MQTT dans le fichier `app/constants.py` :

``` python
MQTT_SERVER = "127.0.0.1"
MQTT_PORT = 1883
KEEP_ALIVE_PERIOD = 60
```

### 1.2. Build

Dans le fichier `app/constants.py` est configuré le nombre de chambres simulés : `NB_ROOMS = X`.

Pour faire tourner l'application DCOP Python, lancer un processus pour chaque chambre : `python3 main_room.py <numero_chambre>`. Lorsque tous les agents on subscribe leur topic MQTT, on peut lancer le serveur DCOP `python3 server_main.py room`. Celui-ci va envoyer un message aux agents pour leur demander de calculer le résultat de l'algorithme DPOP.

**Exemple :** pour `NB_ROOMS = 4` :

``` python
python3 main_room.py 1
{"asctime": "2018-07-16T11:41:20", "topic": "DCOP/1", "type": "State", "content": {"id": 1, "rooms": [{"id": 0, "tau": 26, "devices": [{"id": 1, "critic_state": false, "end_of_prog": 26}]}]}, "level": "INFO"}
{"asctime": "2018-07-16T11:41:20", "topic": "DCOP/1/#", "type": "Info", "content": "Subscribe", "level": "INFO"}
```

``` python
python3 main_room.py 2
[...]
{"asctime": "2018-07-16T11:41:20", "topic": "DCOP/2/#", "type": "Info", "content": "Subscribe", "level": "INFO"}
```

``` python
python3 main_room.py 3
[...]
{"asctime": "2018-07-16T11:41:20", "topic": "DCOP/3/#", "type": "Info", "content": "Subscribe", "level": "INFO"}
```

``` python
python3 main_room.py 4
[...]
{"asctime": "2018-07-16T11:41:20", "topic": "DCOP/4/#", "type": "Info", "content": "Subscribe", "level": "INFO"}
```

Puis on lance le serveur :

``` python
python3 server_main.py room
```

L'algorithme est terminé lorsque le serveur affiche les résultats sous cette forme :

``` python
{"asctime": "2018-07-20T14:03:10", "topic": "DCOP/SERVER/", "type": "Results", "content": "Room 1 need intervention in 241 minutes. PRIORITY : 0 Room 2 need intervention in 241 minutes. PRIORITY : 0 Room 3 need intervention in 241 minutes. PRIORITY : 0 Room 4 need intervention in 241 minutes. PRIORITY : 0 ", "level": "INFO"}
```

## 2\. Tests

Des tests ont été réalisé en utilisant Behave et Hamcrest. Un coverage est disponible avec Coverage.py.

Les commandes suivantes permettent de lancer les tests depuis le répertoire `app/`

* `behave` : lance les tests BDD
* `coverage run <program> <arg1> ... <argn>` : lance le code coverage en même temps que l'algorithme.
Exemple : `coverage run agent_main.py 1`, lance le code coverage en même temps que de lancer un agent.
* `coverage run -m behave` : lance le code coverage d'un point de vu BDD.
* Une fois le programme terminé, utilisez `coverage html` pour générer un compte rendu HTML (*/htmlcov/index.html*).

*Note : le plus pertinant à utiliser est `coverage run -m behave`, sinon coverage ne va pas forcément détecter tous les tests. Par ailleurs, coverage se contente de vérifier s'il existe 1 test qui vérifie chaque ligne de code.*
Il faut prendre cette information en compte lors de l'analyse des résultats.

Pour en savoir plus, consultez la documentation de [Behave](https://behave.readthedocs.io/en/latest/index.html), de [pyHamcrest](https://pypi.python.org/pypi/PyHamcrest) ou de [Coverage](https://coverage.readthedocs.io/en/coverage-4.5.1/).

## 3\. Deployment and SonarCloud tests

Un déploiement automatique a été programmé avec VSTS sur un agent privé (VM ubuntu).

Pour que le script *update\_script.py* fonctionne, il faut installer les packages suivants :

* `pip3 install netifaces`
* `pip3 install GitPython`

Pour que le déploiement fonctionne sur des raspberries par exemple, il faut les préparer. Pour chaque raspberry :

1. Il doit être lié au même réseau que celui de l'agent VSTS.
2. Il doit avoir le repository git sur la branche master de pré-installé.
3. Il doit y avoir les crédential git enregistré sur le raspberry.
4. Le script *update\_script.py* sert à subscribe à un topic MQTT pour recevoir les notifications de mises à jour du serveur. Il effectue ainsi un *git pull* lorsque nécéssaire.

Pour qu'il fonctionne correctement, il doit être placé dans au même niveau que repertoire git pour se déplacer dedens (*DCOP/*). Enfin le script doit être lancé (au démarrage par exemple), pour subscribe au topic MQTT d'update.

For the Quality control, we are using SonarCloud for OpenSource projects. Results are available here https://sonarcloud.io/dashboard?id=muglyon\_DCOP-Decentralised-Control-of-Intelligent-Devices

## 4\. Documentation Annexe

* [Documentation Repertoire Git](./documentation/technical_doc.md)
* [Documentation Technique du Code Python](./documentation/app_doc.md)
* [Mini FAQ et exemples d'implémentations Code Python](./documentation/faq_app.md)
* [Labs IoT Edge - Computer Vision](./documentation/iot-edge-computer-vision-lab.md)