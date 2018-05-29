class DpopManager(object):

    def __init__(self, mqtt_manager, dfs_structure):
        self.mqtt_manager = mqtt_manager
        self.dfs_structure = dfs_structure
