# Exemple d'implémentations de code

[Retour au readme](../Readme.md) - [Retour à la documentation du code Python](./app_doc.md)

<!-- TOC depthFrom:3 -->

- [Exécuter l'algorithme](#executer-lalgorithme)
- [Exécuter un agent](#executer-un-agent)
- [Générer un environnement d'hôpital aléatoire](#générer-un-environnement-dhôpital-aléatoire)
- [Implémenter un nouvel algorithme DCOP](#implémenter-un-nouvel-algorithme-dcop)
- [Implémenter une nouvelle modélisation/approche](#implémenter-une-nouvelle-modélisationapproche)
- [Implémenter un nouveau Starter](#implémenter-un-nouveau-starter)

<!-- /TOC -->

#### Executer l'algorithme

**Attention : quelque soit la modélisation choisie, les agents d'une modélisation ne fonctionnent qu'avec d'autres agents de la même modélisation ! Idem pour le Serveur.**

Dans le fichier `app/constants.py` est configuré le nombre de chambres simulés : `NB_ROOMS = X`.

Pour lancer le programme suivre les étapes suivantes : 

1. Lancez le serveur mosquitto (`mosquitto`)

2. Pour faire tourner l'application DCOP Python, lancer un processus pour chaque chambre : `python3 main_<approche>.py <id_agent>`

3. Lorsque tous les agents ont subscribe leur topic MQTT, on peut lancer le serveur DCOP `python3 server_main.py <approche>`. Celui-ci va envoyer un message aux agents pour leur demander de calculer le résultat de l'algorithme DPOP.

#### Executer un agent 

Pour rappel, un "agent" est un Thread qui va executer l'algorithme DCOP pour le résoudre. Ce Thread va communiquer avec d'autres agents voisins pour prendre sa décision. 

Actuellement, le Thread d'un agent est executé dans la classe `AgentMQTT` lorsque cet AgentMQTT reçoit un top départ depuis son topic. Ainsi, on peut initialiser l'agent en le liant à un Thread `AgentMQTT` : 

*Exemple execution d'un agent pour une approche par chambre :*
```python
from model.monitoring_area.room import Room
from mqtt.agent_mqtt import AgentMQTT

AgentMQTT(Room(1))
```

*Exemple execution d'un agent pour une approche par zone ou par zone multivariables :*
```python
from model.monitoring_area.zone import Zone
from mqtt.agent_mqtt import AgentMQTT

AgentMQTT(Zone(2))
```

#### Générer un environnement d'hôpital aléatoire

Par défaut, les constructeurs de `Hospital`, `Zone` et `Room` sont programmés pour générer un environnement aléatoire. Ainsi, l'instanciation de `Hospital` avec différents paramètres va générer un environnement aléatoire composé de chambres (elles-mêmes composées d'appareils aux caractéristiques aléatoires) et éventuellement de zones. Toutes les caractéristiques sont ainsi aléatoires. 

*Exemple génération d'un environnement approche par chambre*
```python
from model.hospital import Hospital

environment = Hospital(nb_room)
```

*Exemple génération d'un environnement approche par zone*
```python
from model.hospital import Hospital

environment = Hospital(nb_room, nb_zones)
```

*Exemple génération d'un environnement approche par zone multivariables*
```python
from model.hospital import Hospital

environment = Hospital(nb_room, nb_zones, True)
```

#### Implémenter un nouvel algorithme DCOP

Pour proposer une nouvelle version de **UTIL propagation**, il faut créer une nouvelle classe qui va étendre `UtilStratAbstract` pour redéfinir `do_util_propagation`. 

*Exemple :*
```python
from dcop_engine.basic_strat.util_strat_abstract import UtilStratAbstract

class MyUtilStrat(UtilStratAbstract):

    def __init__(self, mqtt_manager, dfs_structure):
        UtilStratAbstract.__init__(self, mqtt_manager, dfs_structure)

    def do_util_propagation(self):
        # insert custom logic here
```

Pour proposer une nouvelle version de **VALUE propagation**, il faut créer une nouvelle classe qui va étendre `ValueStratAbstract` pour redéfinir `do_value_propagation(join_matrix, util_list, matrix_dimensions_order)`. 

*Exemple :*
```python
from dcop_engine.basic_strat.value_strat_abstract import ValueStratAbstract

class MyValueStrat(ValueStratAbstract):

    def __init__(self, mqtt_manager, dfs_structure):
        ValueStratAbstract.__init__(self, mqtt_manager, dfs_structure)

    def do_value_propagation(self, join_matrix, util_list, matrix_dimensions_order):
        # insert custom logic here
```

Enfin, pour inclure ces nouvelles étapes dans l'algorithme ou définir un tout nouvel algorithme DCOP, on peut créer une nouvelle classe qui va étendre `Dpop` et redéfinir dans le constructeur les différentes étapes que l'on souhaite.

*Exemple :*
```python
from dcop_engine.basic_strat.dpop import Dpop
from dcop_engine.room.room_util_start import RoomUtilStrat
from dcop_engine.room.room_value_strat import RoomValueStrat

class MyDcop(Dpop):

    def __init__(self, monitored_area, mqtt_client):
        Dpop.__init__(self, monitored_area, mqtt_client)

        self.util_manager = MyUtilStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)
        self.value_manager = MyValueStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)
```

Par la suite, il est possible de surcharger les différentes méthodes des classes de */basic_strat/* pour y faire nos propres traitements. 

#### Implémenter une nouvelle modélisation/approche

Il est possible d'ajouter une nouvelle modélisation en implémentant sa propre *monitoring area* : 

```python
from model.monitoring_areas.monitoring_area import MonitoringArea

class MyMonitoringArea(MonitoringArea):

    def __init__(self, id):
        MonitoringArea.__init__(self, id)

    # insert custom methods and logic here 
```

Si l'objet créé hérite directement de `Room` ou de `Zone`, on peut le lancer directement avec l'algorithme DPOP de son parent : 

```python
monitored_area = MyMonitoring_area(1)
agent_mqtt = AgentMQTT(monitored_area)
agent_mqtt.run()
```

**/!\ Attention : si la nouvelle modélisation est plus complexe, il est nécessaire de redéfinir un minimum l'algorithme. Pour cela, voir la section "Implémenter un nouvel algorithme DCOP"**



#### Implémenter un nouveau Starter

*Pour rappel : le Starter est un Thread à part qui envoie un Top départ aux agents et récupère les résultats pour les analyser.*

Il est possible de créer son propre Thread de server pour analyser les résultats retournés par l'algorithme ou modifier le fonctionnement de l'algorithme. Pour cela, il suffit d'étendre la classe `Starter` comme illustré ci-dessous (cf. `starter.py`) : 

```python
from dcop_server.starter import Starter

class MyStarter(Starter):

    def __init__(self, agents, mqtt_client):
        Starter.__init__(self, agents, mqtt_client)

    def run
        # insert custom logic here
```
