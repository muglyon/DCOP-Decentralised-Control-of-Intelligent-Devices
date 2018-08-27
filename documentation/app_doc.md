# Documentation App Python - Medical DCOP

[Retour au readme](../Readme.md)

La documentation ci-dessous décrit les principes et techniques utilisées pour le développement du DCOP en Python. Le code est ordonné en différents packages qui gèrent des choses différentes les uns des autres. Avant de plonger dans le code, il est fortement conseillé d'avoir lu les rapports de stage pour comprendre le contexte. 

Une FAQ donnant des exemples d'utilisations des différentes classes est disponible [ici](./faq_app.md).

L'algorithme DCOP (DPOP) qui a été implémenté suis les mécanismes décrit dans le livre d'Adrien Petcu : [A Class of Algorithms for Distributed Constraint Optimization](https://books.google.fr/books?id=y9lZ4Y8zEtMC&pg=PA52&lpg=PA52&dq=dfs+tree+dpop&source=bl&ots=Lj1FrbU0C3&sig=6SCFxLwRbsz6UzDlqEbKDhJlJp8&hl=fr&sa=X&ved=0ahUKEwi3uNDh44zaAhVBUhQKHZYiC9gQ6AEIMDAB#v=onepage&q&f=false). Pour bien comprendre le code, la lecture de la partie DPOP est fortement recommandée (pages 52 à 57) ainsi que la lecture de l'algorithme de génération de l'arbre DFS (pages 40 à 47 environ). Entre autres choses, il est important de bien comprendre le fonctionnement en 3 étapes de l'algorithme : **Génération de l'arbre DFS**, **Util Propagation** et **Value Propagation**. D'un point de vu purement mathématiques, des manipulations de matrices complexes sont réalisées par le **JOIN (or Combine)** de deux matrices et la **PROJECTION** d'une dimension en dehors d'une matrice. Ces concepts sont détaillés dans le livre.

<!-- TOC depthFrom:3 -->

- [1. DCOP Engine](#1-dcop-engine)
- [2. DCOP Server](#2-dcop-server)
- [3. Events](#3-events)
- [4. Features](#4-features)
- [5. Logs](#5-logs)
- [6. Model](#6-model)
- [7. MQTT](#7-mqtt)
- [8. Autres](#8-autres)

<!-- /TOC -->

### 1. DCOP Engine

Ce package contient un ensemble de classes et méthodes permettant de lancer des threads pour résoudre l'algorithme DCOP. Comme expliqué dans le rapport de stage, 3 approches différentes ont été étudiées et implémentées : une approche par chambre (*room*), un approche par zone (*zone*) et une approche par zone multivariables (*zone multi*). Ces trois approches impliquent des modifications spécifiques dans l'algorithme (surtout l'approche *zone multi*). Pour ces raisons, un mini [pattern Stratégie](https://fr.wikipedia.org/wiki/Strat%C3%A9gie_(patron_de_conception)) a été implémenté pour réaliser un algorithme DPOP spécifique pour chaque approche. 

Le dossier */basic_strat/* contient l'ensemble des fichiers de base pour réaliser l'algorithme : 

+ dpop.py : **Thread**

Lance successivement les trois étapes de l'algorithme DPOP et enregistre les résultats observés dans les logs.

+ dfs_strat.py

Lance la génération d'un arbre DFS au travers de la méthode `generate_dfs`.

+ util_strat_abstract.py et value_strat_abstract.py : **Abstract**

Permettent de définir les deux phases d'util propagation et de value propagation via les méthodes `do_util_propagation()` et `do_value_propagation(join_matrix, util_list, matrix_dimensions_order)` qui sont utiliées dans la résolution du dcop.

Le dossier */room/* contient l'ensemble des fichiers de spécifiques pour réaliser l'algorithme sous une modélisation par chambre. Ces classes sont des surcharges des classes définies dans */basic_strat/*.

Le dossier */zone/* contient l'ensemble des fichiers de spécifiques pour réaliser l'algorithme sous une modélisation par zone. Cette approche réutilise le même code que pour une approche par chambre.

Le dossier */zone_multi/* contient l'ensemble des fichiers de spécifiques pour réaliser l'algorithme sous une modélisation par zone multivariables. Ces classes sont des surcharges des classes définies dans */basic_strat/*.

+ constraint_manager.py 

Défini l'ensemble des constraintes du système (cf. Modélisation DCOP décrite dans le rapport de stage). On peut ainsi récupérer le coût associé à une contrainte pour un temps de passage et une zone à surveiller spécifique. 

*Exemple :*
```python
from dcop_engine import constraint_manager as cm

# Récupère le coût retourné par la contrainte "C1" - si la chambre possède des appareils ou non - si le prochain passage est dans 10 minutes (v_i = 10). 
cost = cm.c1_no_devices(monitored_area, 10)
```

Ci-dessous se trouve la liste des contraintes actuellement supportées : 

```python
c1_no_devices(monitored_area, vi)
c2_device_status(monitored_area, vi)
c3_neighbors_sync(vi, vj)
c4_last_intervention(monitored_area, vi)
c5_nothing_to_report(monitored_area, vi)

# Retourne la somme de toutes les contraintes à l'exception de c3.
get_cost_of_private_constraints_for_value(monitored_area, value)
```

+ execution_time.py

Utilitaire permettant de calculer divers moyennes, écarts-types et intervalle de confiance pour calculer des temps d'executions globaux.

### 2. DCOP Server

Pour fonctionner, le serveur DCOP utilise lui aussi le principe des Threads qui peuvent ainsi permettre de lancer plusieurs résolutions de DCOP en parrallèle. 

+ starter.py : **Thread**

Donne le top départ aux agents pour calculer. Le Thread attend les résultats après avoir donné le top départ puis attends `TWO_MINUTS` (paramétrable dans `constants.py`) avant de lancer un nouveau top. Ce starter tourne ainsi à l'infini et a pour but d'être utilisé pour lancer l'algorithme plusieurs fois de suite automatiquement et dans le même environnement. 

*Exemple d'utilisation :*
```python
starter = Starter(monitored_area_list, client_mqtt)
starter.start()
```

Une fois les résultats obtenus, ce thread est capable de trier  les résultats en fonction d'une priorité qu'il définit lui-même.  

+ starter_zone_multi.py 

Implémentation spécifique de `starter.py` pour une approche par zone multivariables. Redéfinit principalement le calcul de la priorité. 

+ urgt_starter.py 

Implémentation spéficique de `starter.py`. C'est une implémentation un peu particulière qui permet de lancer une nouvelle itération de l'algorithme en urgence. Pour cela, le `UrgtStarter` lance une nouvelle itération de l'algorithme avec un agent critique automatiquement désigné comme ROOT de l'arbre DFS, puis redonne la main à un thread principal. 

*Exemple d'utilisation :*
```python
starter = Starter(monitored_area_list, client_mqtt)
urgt_starter = UrgentStarter(
    starter,
    client_mqtt,
    agent_critique,
)
```

### 3. Events

 Pour proposer des simulations plus proches des conditions réelles, un système d'évènements est en place pour permettre au modèle d'évoluer dynamiquement entre deux itérations. 

 + event.py : **Thread**

Génère aléatoirement des évènements sur une monitored_area spécifique. 

*Exemple d'utilisation :*
```python
Event(monitored_area).start()
```

Les évènements générés sont aléatoires et peuvent modifier la monitored_area de différentes façon : 

    - Faire rentrer un appareil en état critique, 
    - Ajouter ou modifier un appareil de la monitored_area, 
    - Enlever un appareil (qui simule ainsi le débranchement ou la panne), 
    - Reprogrammer un appareil (change le temps de programmation de l'appareil qui simule ainsi le passage d'une infirmière dans la chambre). 

+ event_observer.py

Lié à une monitored_area, permet de déclencher des actions spécifiques lorsqu'un changement intervient sur la monitored_area. De base, deux notifications différentes sont disponibles : 

    - notify_emergency() qui envoie un message MQTT d'urgence à destination du serveur. C'est ce message qui va potentiellement trigger un UrgtStarter côté serveur. 

    - notify_intervention_detected() qui réinitialise le temps depuis le dernier passage d'une infirmière à 0 (cf. tau dans l'algorithme). 

Fonctionnant comme un mini pattern Observer-Observé, `EventObserver` a pour vocation d'être attaché à l'objet qu'il doit observer.

*Exemple d'utilisation :*
```python
observer = EventObserver(monitored_area, agent_mqtt.client)
monitored_area.attach_observer(observer)
```
### 4. Features

Contient l'ensemble des fichiers *.feature* et *.py* de tests de l'application. Les tests ont été implémentés en suivant les frameworks `behave` qui permet de réaliser des tests en BDD et `pyHamcrest`. Ces tests sont principalement des tests d'intégration (et un peu de tests unitaires) car la plupart des fonctionnalités n'ont de sens à être testé qu'en situation réelle. Enfin, ces tests concernent surtout la modélisation par chambre (car c'est la principale).

Pour lancer les tests en local, installez les frameworks : 
```shell
pip3 install behave
pip3 install pyhamcrest
pip3 install coverage
```

+ environment.py

Définit un environnement "réel" pour réaliser les tests. Certaines méthodes sont Mock, mais le but est tout de même de proposer un environnement réaliste. Dans ce fichier est défini un setup basique avec 4 agents qui peut être surchargé par la suite directement dans les méthodes de tests. 

+ *.feature

Les fichiers *.feature* décrivent les tests sous forme BDD avec les mots clefs **Given**, **When**, **Then**. Pour plus d'informations, se référer à la documentation de [Behave](https://behave.readthedocs.io/en/latest/index.html).

+ /steps/*.py

Définit l'ensemble des *steps* selon les .features décrites. Pour plus d'informations, se référer à la documentation de [Behave](https://behave.readthedocs.io/en/latest/index.html). Le fichier *common.py* regroupe certains steps communs à plusieurs fichiers.  

### 5. Logs

Pour garder une trace dans les raspberry de leurs processus de résolution, un système de logs a été mis en place. 

+ log.py 

Définit un `logger` particulier en utilisant les librairies `logging` de python et `pythonjsonlogger`. Trois méthodes sont définies : 

```python
# Setup du logger
setup_custom_logger(file_name) 

# Enregistre un msg [INFO] provenant de sender_id
info(msg, sender_id, msg_type)

# Enregistre un msg [CRITICAL] provenat de sender_id
critical(msg, sender_id)
```

*Exemple d'utilisation*
```python
from logs import log

log.setup_custom_logger("logs/agents/log_agent_1_2018-07-30.json")
log.info("Test Log Message Info", monitored_area.id, "INIT")
```

Par défaut, tous les fichiers de logs sont enregistrés dans *logs/agents/* pour les agents et dans *logs/server/* pour les logs du serveur.

+ message_types.py : **Enum**

Enumération de tous les messages_type possible des logs. 

### 6. Model

Le model décrit la structure de l'hôpital, des zones à monitorer et des machines pour l'ensemble du système. 

+ dfs_structure.py

Décrit la structure d'un arbre DFS. Pour comprendre l'utilité et l'objectif de chaque attribut, se référer à l'algorithme initial de [A. Petcu](https://books.google.fr/books?id=y9lZ4Y8zEtMC&pg=PA52&lpg=PA52&dq=dfs+tree+dpop&source=bl&ots=Lj1FrbU0C3&sig=6SCFxLwRbsz6UzDlqEbKDhJlJp8&hl=fr&sa=X&ved=0ahUKEwi3uNDh44zaAhVBUhQKHZYiC9gQ6AEIMDAB#v=onepage&q&f=false). 

+ device.py 

Décrit un appareil avec les attributs suivants : 

    - id_device : identifiant
    - __end_of_prog : temps avant la fin d'un programme en minutes (ex : 60)
    - __is_in_critic_state : boolean set à True si la machine est en état critique

+ hospital.py 

Décrit un hôpital avec les attributs suivants : 

    - monitored_area_list : liste des zones à surveiller. 

La méthode `setup_neighbors(self)` permet de définir le voisinage entre les zones à surveiller dans l'hôpital. Par défaut et par simplicité, les éléments de la `monitored_area_list` ne sont divisés qu'en deux lignes. 

*Exemple d'instanciation :*
```python
from model.hospital import hospital

# multivariables est un booléen set à True si on souhaite créer un hôpital avec une approche par zone multivariables. 
# nb_zones et multivariables sont optionnels
hospital = Hospital(nb_rooms, nb_zones, multivariable)
```

+ /monitoring_areas/monitoring_area.py : **Abstract**

Permet de définir une *monitored area*. Dans la résolution du DCOP, chaque *monitored area* participe dans la prise de décision et résoud le DCOP localement en discutant avec les autres agents. Par ailleurs, cette classe permet de forcer la définition de certaines méthodes indispensables à la résolution du DCOP lorsqu'elle est étendue. 

Chaque *monitored area* possède les attributs suivants : 

    - id : identifiant
    - front_neighbor : monitored area voisine d'en face
    - right_neighbor : monitored area voisine de droite
    - left_neighbor : monitored area voisine de gauche
    - current_v : temps avant le prochain passage souhaité pour l'itération courante en minutes
    - previous_v : temps avant le prochain passage souhaité pour l'itération précédente en minutes
    - tau : temps écoulé depuis le dernier passage en minutes

+ /monitoring_areas/room.py : **MonitoringArea**

Implémentation d'une *monitored area* sous forme de Chambre. Décrit une chambre avec les attributs suivants : 

    - device_list : liste de machines à surveiller

+ /monitoring_areas/zone.py : **MonitoringArea**

Implémentation d'une *monitored area* sous forme de Zone. Décrit une zone avec les attributs suivants : 

    - rooms : liste de Room à surveiller
    - multivariables : boolean set à True si la Zone concerne une approche multivariables. 

### 7. MQTT

Pour faire fonctionner la communication MQTT, installez paho-mqtt pour python : 
`pip3 install paho-mqtt python-etcd`. Pour en savoir plus, consultez la documentation de [Paho pour Python](https://pypi.python.org/pypi/paho-mqtt).

+ custom_mqtt_class.py

Permet de définir un utilitaire MQTT particulier. Entre autre, les méthodes de `on_connect`, `on_message` et `on_disconnect` sont redéfinies pour y ajouter une logique particulière. La méthode `run` permet de connecter le client MQTT et de `loop_forever()`. 

+ agent_mqtt.py : **CustomMQTTClass**

Implémentation d'une *CustomMQTTClass* pour un agent du système DCOP. 

+ server_mqtt.py : **CustomMQTTClass**

Implémentation d'une *CustomMQTTClass* pour le serveur du système DCOP.

+ mqtt_manager.py 

Utilitaire définissant un ensemble de méthodes pour publier des messages sur le serveur MQTT. Cet utilitaire peut être utilisé par les agents ou le serveur. 

### 8. Autres

+ constants.py

Définit une bonne partie des constantes utilisées dans le système : 

```python
NB_ROOMS = 6
NB_ZONES = 4

DIMENSION = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 120, 180, 210, 241] # Toutes la valeurs possibles pour v_i (cf. algorithme de A. Petcu)
DIMENSION_SIZE = len(DIMENSION)
INFINITY_IDX = DIMENSION.index(241) # La valeur 241 correspond à l'infini (cf. algorithme de A. Petcu)

[...]

MQTT_SERVER = "127.0.0.1"
MQTT_PORT = 1883
KEEP_ALIVE_PERIOD = 60

[...]
```

+ main_room.py, main_zone.py, main_zone_multi.py

Sont les main() pour lancer les différents agents. Il faut passer en paramètre l'identifiant de l'agent.

*Exemple d'utilisation*
```python
python3 main_zone.py 2
```

+ server_main.py

Permet de lancer le serveur. Les mots clefs `room`, `zone` et `multi` passés en paramètre permettent de définir le mode de résolution choisi. 

*Exemple d'utilisation*
```python
python3 server_main.py zone
```

**Attention : si on lance le serveur avec la mauvaise modélisation par rapport aux agents, l'algorithme ne fonctionnera pas. Par ailleurs, il est important de lancer un nombre d'agents identiques aux nombres inscrit dans constants.py PUIS de lancer le serveur. Sinon les agents et le serveur ne seront pas synchronisés.**
