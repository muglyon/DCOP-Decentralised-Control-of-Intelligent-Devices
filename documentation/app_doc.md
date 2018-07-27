# Documentation App Python - Medical DCOP

[Retour au readme](../Readme.md) - [Retour à la doc](./technical_doc.md)

La documentation ci-dessous décrit les principes et techniques utilisées pour le développement du DCOP en Python. Le code est ordonné en différents packages qui gèrent des choses différents les uns des autres. Avant de plonger dans le code, il est fortement conseillé d'avoir lu les rapports de stage pour comprendre le contexte. 

Une FAQ donnant des exemples d'utilisations des différentes classes est disponible [ici](./faq_app.md).

L'algorithme DCOP (DPOP) qui a été implémenté suis les mécanismes décrit dans le livre d'Adrien Petcu : [A Class of Algorithms for Distributed Constraint Optimization](https://books.google.fr/books?id=y9lZ4Y8zEtMC&pg=PA52&lpg=PA52&dq=dfs+tree+dpop&source=bl&ots=Lj1FrbU0C3&sig=6SCFxLwRbsz6UzDlqEbKDhJlJp8&hl=fr&sa=X&ved=0ahUKEwi3uNDh44zaAhVBUhQKHZYiC9gQ6AEIMDAB#v=onepage&q&f=false). Pour bien comprendre le code, la lecture de la partie DPOP est fortement recommandée (pages 52 à 57). Entre autres choses, il est important de bien comprendre le fonctionnement des 3 étapes :**Génération de l'arbre DFS**, **Util Propagation** et **Value Propagation**. D'un point de vu mathématiques, des manipulations de matrices complexes sont réalisée par le **JOIN (or Combine)** de deux matrices et la **PROJECTION** d'une dimension en dehors d'une matrice. Tous ces concepts sont détaillés dans le livre.

## Structure du code

### DCOP Engine

Ce package contient un ensemble de classes et méthodes permettant de lancer des threads pour résoudre l'algorithme DCOP. Comme expliqué dans le rapport de stage, 3 approches différentes ont été étudiées et implémentées : une approche par chambre (*room*), un approche par zone (*zone*) et une approche par zone multivariables (*zone multi*). Ces trois approches implique des modifications spécifiques dans l'algorithme (surtout l'approche *zone multi*). Pour ces raisons, un mini pattern Stratégie a été implémenté pour réaliser un algorithme DPOP spécifique pour chaque approche. 

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

Défini l'ensemble des constraintes du système (cf. Modélisation DCOP décrite dans le rapport de stage). On peut ainsi récupérer le coût associé à une contrainte pour un temps de passage et une zone à surveillé spécifique.

*Exemple :*
```python
from dcop_engine import constraint_manager as cm

# Récupère le coût retournée par la contrainte "C1" - si la chambre possède des appareils ou non - si le prochain passage est dans 10 minutes (v_i = 10). 
cost = cm.c1_no_devices(monitored_area, 10)
```

Les contraintes suivantes ont été défini : 
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

### DCOP Server

Pour fonctionner, le serveur DCOP utilise lui aussi la principe des Threads qui peuvent ainsi permettre de lancer plusieurs résolutions de DCOP en parrallèle. 

+ starter.py : **Thread**

Donne le top départ aux agents pour calculer. Le Thread attends les résultats après avoir donné le top départ puis attends `TWO_MINUTS` (paramétrable dans `constants.py`) avant de lancer un nouveau top. Ce starter tourne ainsi à l'infini et à pour but d'être utilisé pour lancer l'algorithme plusieurs fois de suite automatiquement et dans le même environnement. 

*Exemple d'utilisation :*
```python
starter = Starter(monitored_area_list, client_mqtt)
starter.start()
```

Une fois les résultats obtenu, ce thread est capable de trier  les résultats en fonction d'une priorité qu'il définit lui-même.  

+ starter_zone_multi.py 

Implémentation spécifique de `starter.py` pour un approche par zone multivariables. Redéfini principalement le calcul de la priorité. 

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

### Events

 Pour proposer des simulations plus proches des conditions réelles, un système d'évènements est en place pour permettre au model d'évoluer dynamiquement entre deux itérations. 

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

Lié à une monitored_area, permet de déclencher des actions spécifiques lorsqu'un changement interviens sur la monitored_area. De base, deux notifications différentes sont disponibles : 

    - notify_emergency() qui envoi un message MQTT d'urgence à destination du serveur. C'est ce message qui va potentiellement trigger un UrgtStarter côté server. 

    - notify_intervention_detected() qui réinitialise le temps depuis le dernier passage d'une infirmière à 0 (cf. tau dans l'algorithme). 

Fonctionnement comme un mini pattern Observer-Observé, `EventObserver` a pour vocation à être attaché à l'objet qu'il doit observé.

*Exemple d'utilisation :*
```python
observer = EventObserver(monitored_area, agent_mqtt.client)
monitored_area.attach_observer(observer)
```
### Features

Contien l'ensemble des fichiers *.feature* et *.py* de tests de l'application. Les tests ont été implémentés en suivant les frameworks `behave` qui permet de réaliser des tests en BDD et `pyHamcrest`. Ces tests sont principalement des tests d'intégration (et un peu de tests unitaires) car la plupart des fonctionnalités n'ont de sens à être testé qu'en situation réelle. 

+ environment.py

Défini un environnement "réelle" pour réaliser les tests. Certaines méthodes sont Mock, mais le but est tout même de proposer un environnement réaliste. Dans ce fichier est défini un setup basic qui peut être surchargé par la suite directement dans les méthodes de tests. 

+ *.feature

Les fichiers *.feature* décrivent les tests sous forme BDD avec les mots clefs **Given**, **When**, **Then**. Pour plus d'informations, se référé à la documentation de [Behave](https://behave.readthedocs.io/en/latest/index.html).

+ /steps/*.py

Défini l'ensemble des *steps* selon les .features décrites. Pour plus d'informations, se référé à la documentation de [Behave](https://behave.readthedocs.io/en/latest/index.html). 

### Logs

### Model

### MQTT

todo : principe, fonctionnement, ...

Pour faire fonctionner la communication MQTT, installez paho-mqtt pour python : 
`pip3 install paho-mqtt python-etcd`.

Pour en savoir plus, consultez la documentation de [Paho pour Python](https://pypi.python.org/pypi/paho-mqtt).

## 3 Approches différentes 

- `main_zone.py <agentId>` : lance un agent pour une modélisation par zone
- `main_zone_multi.py <agentId>` : lance un agent pour une modélisation par zone multivariables

Quelque soit la modélisation choisie, les agents d'une modélisation ne fonctionnent qu'avec d'autres agents de la même modélisation ! Pour lancer le programme suivre les étapes suivantes : 

1. Lancez le serveur mosquitto (`mosquitto`)

2. Lancez le code de chaque agent avec en paramètre l'identifiant de l'agent `python3 main_<approche>.py <id_agent>`

## Tests

Pour lancer les tests en local, installez les frameworks : 
- `pip3 install behave`
- `pip3 install pyhamcrest`
- `pip3 install coverage`

