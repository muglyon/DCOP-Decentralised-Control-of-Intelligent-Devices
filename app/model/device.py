#! python3
# device.py - Implement the device model
# Usefull for testing !


class Device(object):
    
    def __init__(self, id_device, end_of_program, is_in_critic_state):
        self.id = id_device
        self.__end_of_prog = end_of_program
        self.__is_in_critic_state = is_in_critic_state
        self.observer = None

    @property
    def is_in_critic_state(self):
        return self.__is_in_critic_state

    @is_in_critic_state.setter
    def is_in_critic_state(self, new_value):
        self.__is_in_critic_state = new_value

        if self.__is_in_critic_state and self.observer is not None:
            self.observer.notify()

    @property
    def end_of_prog(self):
        return self.__end_of_prog

    @end_of_prog.setter
    def end_of_prog(self, ending_time):
        self.__end_of_prog = ending_time if ending_time > 0 else 241

    def to_json_format(self):
        return {"id": self.id, "critic_state": self.is_in_critic_state, "end_of_prog": self.end_of_prog}
