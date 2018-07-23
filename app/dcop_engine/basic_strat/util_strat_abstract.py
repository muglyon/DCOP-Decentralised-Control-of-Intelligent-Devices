import abc


class UtilStratAbstract(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, mqtt_manager, dfs_structure):
        self.JOIN = None
        self.UTIL = None
        self.mqtt_manager = mqtt_manager
        self.dfs_structure = dfs_structure

    @abc.abstractmethod
    def do_util_propagation(self):
        return
