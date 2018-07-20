import abc


class ValueStratAbstract(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, mqtt_manager, dfs_structure):
        self.mqtt_manager = mqtt_manager
        self.dfs_structure = dfs_structure

    @abc.abstractmethod
    def do_value_propagation(self, join_matrix, util_list, matrix_dimensions_order):
        return
