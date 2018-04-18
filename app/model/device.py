#! python3
# device.py - Implement the device model
# Usefull for testing !

class Device(object):
    
    def __init__(self, idDevice, endOfProgram, isInCriticalState):
        self.id = idDevice
        self.endOfProgram = endOfProgram
        self.inCriticalState = isInCriticalState

    def toString(self):
        string = " > Device " + str(self.id) + " "

        if self.inCriticalState :
            string += "IN CRITICAL STATE !\n"
        else :
            string += "end it's program in " + str(self.endOfProgram) + "\n"

        return string
