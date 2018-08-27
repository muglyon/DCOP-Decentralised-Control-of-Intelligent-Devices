# Medical DCOP Documentation

[Retour au readme](../Readme.md)

Ce répertoire git contient l'ensemble du projet Médical DCOP. Celui-ci contiens différents programmes utile au développement et à la compréhension du projet : 

## app 

Contient le code python permettant de lancer le DCOP en local (cf. [Getting Started](./Readme.md)). Le documentation des fichiers de code est disponible [ici](./app_doc.md). Une FAQ donnant des exemples d'implémentations et d'utilisations est aussi disponible [ici](./faq_app.md).

## backups

Contient un script de déploiement VSTS

## edgeModules

Contient différents modules python intéragissant avec Azure IoT Edge (computer vision). Une description des labs est disponible [ici](./iot-edge-computer-vision-lab.md).

## javaSimulator

Contient des programmes Java de simulation utilisant le Framework Frodo. Celui-ci tourne avec Java 8. 

Pour lancer les simulations de l'algorithme avec Frodo, il est nécéssaire de lier le projet aux librairies suivantes : 

- JavaSimulator/lib/frodo2/frodo2.jar
- JavaSimulator/lib/frodo2/lib/jdom-X.X.X.jar
- JavaSimulator/lib/frodo2/lib/or-objects-X.X.X.jar

Pour faire fonctionner la communication MQTT, on utilise paho-mqtt et Gson pour envoyer les données au format Json. Les Jars sont accessibles dans le dossier lib :

- JavaSimulator/lib/org.eclipse.paho.client.mqttv3-X.X.X.jar
- JavaSimulator/lib/gson-X.X.X.jar

Pour en savoir plus, consultez la documentation de [Frodo](https://frodo-ai.tech/), de [Paho](https://www.eclipse.org/paho/) ou de [Gson](https://github.com/google/gson).