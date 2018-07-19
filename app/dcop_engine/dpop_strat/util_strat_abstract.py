import abc


class UtilStratAbstract(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.JOIN = None
        self.UTIL = None

    @abc.abstractmethod
    def do_util_propagation(self):
        return
