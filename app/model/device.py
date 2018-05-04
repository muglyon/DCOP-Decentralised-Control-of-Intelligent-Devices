#! python3
# device.py - Implement the device model
# Usefull for testing !


class Device(object):
    
    def __init__(self, id_device, end_of_program, is_in_critic_state):
        self.id = id_device
        self.end_of_prog = end_of_program
        self.is_in_critic_state = is_in_critic_state

    def set_end_of_prog(self, ending_time):
        self.end_of_prog = ending_time if ending_time > 0 else 241

    def to_string(self):
        string = " > Device " + str(self.id) + " "

        if self.is_in_critic_state:
            string += "IN CRITICAL STATE !\n"
        else:
            string += "end it's program in " + str(self.end_of_prog) + "\n"

        return string
