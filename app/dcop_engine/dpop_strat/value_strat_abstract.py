import abc


class ValueStratAbstract(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def do_value_propagation(self, join_matrix, util_list, matrix_dimensions_order):
        return
