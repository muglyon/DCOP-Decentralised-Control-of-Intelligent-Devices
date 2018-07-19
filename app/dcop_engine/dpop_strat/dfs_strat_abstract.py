import abc


class DfsStratAbstract(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.choose_root_execution_time = 0

    @abc.abstractmethod
    def generate_dfs(self):
        return
