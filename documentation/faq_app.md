# Exemple d'implémentations de code

[Retour au readme](../Readme.md) - [Retour à la doc](./technical_doc.md)

#### Comment Implémenter ma propre version de l'algorithme ? 

Pour proposer une nouvelle version de **UTIL propagation**, il faut créer une nouvelle classe qui va étendre `UtilStratAbstract` pour redéfinir `do_util_propagation`. 

*Exemple :*
```python
class MyUtilStrat(UtilStratAbstract):

    def __init__(self, mqtt_manager, dfs_structure):
        UtilStratAbstract.__init__(self, mqtt_manager, dfs_structure)

    def do_util_propagation(self):
        # insert custom logic here
```

Pour proposer une nouvelle version de **VALUE propagation**, il faut créer une nouvelle classe qui va étendre `ValueStratAbstract` pour redéfinir `do_value_propagation(join_matrix, util_list, matrix_dimensions_order)`. 

*Exemple :*
```python
class MyValueStrat(ValueStratAbstract):

    def __init__(self, mqtt_manager, dfs_structure):
        ValueStratAbstract.__init__(self, mqtt_manager, dfs_structure)

    def do_value_propagation(self, join_matrix, util_list, matrix_dimensions_order):
        # insert custom logic here
```

Pour utiliser ces nouvelles versions dans l'algorithme, il faut créer une nouvelle classe qui va étendre `Dpop` et redéfinir dans le constructeur les différentes étapes que l'on a modifié.

*Exemple :*
```python
class MyDpop(Dpop):

    def __init__(self, monitored_area, mqtt_client):
        Dpop.__init__(self, monitored_area, mqtt_client)

        self.util_manager = MyUtilStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)
        self.value_manager = MyValueStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)
```

Par là suite, et pour ces trois classes, il est possible de surcharger les méthodes des classes de */basic_strat/* pour y faire nos propres traitements. 

#### Comment executer mon propre Agent ? 

Pour executer un nouvel Agent, il faut instancier la zone à surveiller et la liée à un AgentMQTT.

```python
monitored_area = Room(1)
AgentMQTT(monitored_area)
```

#### Comment Implémenter mon propre starter ?

Il est possible de créer son propre thread de server pour analyser les résultats retournés par l'algorithme. Pour cela, il suffit d'étendre la classe `Starter` comme suit (cf. `starter.py`) : 

```python
class MyStarter(Starter):

    def __init__(self, agents, mqtt_client):
        Starter.__init__(self, agents, mqtt_client)

    def run
        # insert custom logic here
```