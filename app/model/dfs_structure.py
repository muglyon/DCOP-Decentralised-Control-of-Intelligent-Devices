class DfsStructure(object):

    def __init__(self, monitored_area):
        self.monitored_area = monitored_area
        self.is_root = False
        self.open_neighbors_id = None  # neighbors Id : see "open" in the algorithm
        self.children_id = []
        self.parent_id = 0
        self.pseudo_children_id = []
        self.pseudo_parents_id = []

    def is_leaf(self):
        return len(self.children_id) == 0
