# Medical DCOP Documentation

[Retour au readme](../Readme.md)

Ce répertoire git contient l'ensemble du projet Médical DCOP. Celui-ci contiens différents programmes utile au développement et à la compréhension du projet : 

- [app](./app_doc.md) : contient le code python permettant de lancer le DCOP en local (cf. [Getting Started](./Readme.md)).

- backups : contient un script de déploiement VSTS

- [edgeModules](./iot-edge-computer-vision-lab.md) : contient différents modules python intéragissant avec Azure IoT Edge (computer vision). 

- javaSimulator : contient des programmes Java de simulation utilisant le Framework Frodo. 

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

Les programmes Python et Java utilisent la communication MQTT entre les agents. Le serveur utilisé pour les tests est un serveur MQTT Mosquitto. 