from dcop_server.starter import Starter


class UrgentStarter(Starter):

    def __init__(self, main_server_thread, mqtt_client, critical_root_chosen=0):
        Starter.__init__(self, main_server_thread.agents, mqtt_client)

        self.priorities = main_server_thread.priorities
        self.old_results_index = main_server_thread.old_results_index

        self.critical_root_chosen = critical_root_chosen
        self.main_server_thread = main_server_thread

    def run(self):

        while self.main_server_thread.is_running:
            # Wait for the main thread to sleep
            continue

        self.main_server_thread.pause = True

        self.do_one_iteration()
        self.callback_update_main_thread()

        self.main_server_thread.pause = False

    def choose_root(self):

        if self.critical_root_chosen > 0:

            self.priorities[str(self.critical_root_chosen)] += 1
            self.priorities[str(self.critical_root_chosen)] *= 2

            return self.critical_root_chosen

        return super().choose_root()

    def callback_update_main_thread(self):
        for key in self.priorities:
            self.main_server_thread.priorities[key] += self.priorities[key]
