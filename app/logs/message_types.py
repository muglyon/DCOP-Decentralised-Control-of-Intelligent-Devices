from enum import Enum


class MessageTypes(Enum):

    ON = "ON"
    ROOT = "ROOT"
    CHILD = "CHILD"
    PSEUDO = "PSEUDO"
    UTIL = "UTIL"
    VALUES = "VALUES"
    URGT = "URGT"

    @staticmethod
    def is_child(msg_type):
        return msg_type == MessageTypes.CHILD.value

    @staticmethod
    def is_pseudo(msg_type):
        return msg_type == MessageTypes.PSEUDO.value

    @staticmethod
    def is_on(msg_type):
        return msg_type == MessageTypes.ON.value
