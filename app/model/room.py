#! python3
# room.py - Modelisation of a room

from model.device import Device
from random import randint

import random

class Room(object):

    MAX_NB_DEVICES = 6

    ###
    # FOR DEBUG : generate a random Room !
    def __init__(self, id):
        self.id = id
        self.tau = randint(5, 241)
        self.deviceList = []
        self.frontNeighbor = None
        self.rightNeighbor = None
        self.leftNeighbor = None

        for i in range(0, randint(0, self.MAX_NB_DEVICES)) :
            idD = str(id) + str(i + 1)
            criticState = random.random() < 0.05
            self.deviceList.append(Device(int(idD), randint(5, 241), criticState))

    def setLeftNeighbor(self, neighbor):
        self.leftNeighbor = neighbor

    def setRightNeighbor(self, neighbor):
        self.rightNeighbor = neighbor

    def setFrontNeighbor(self, neighbor):
        self.frontNeighbor = neighbor

    def setDevices(self, devices):
        self.deviceList = devices
        
    ###
    # Get number of neighbors
    def getDegree(self):
        count = 0
        if self.leftNeighbor != None :
            count += 1
        if self.rightNeighbor != None :
            count += 1
        if self.frontNeighbor != None :
            count += 1
        return count

    ###
    # Get list of all neighbors Id of the agent
    def getAllNeighborsId(self):
        neighbors = []
        if self.leftNeighbor != None : 
            neighbors.append(int(self.leftNeighbor.id))
        if self.rightNeighbor != None :
            neighbors.append(int(self.rightNeighbor.id))
        if self.frontNeighbor != None :
            neighbors.append(int(self.frontNeighbor.id))
        return neighbors

    ###
    # Get list of all neighbors Id EXCEPT agentId
    def getAllNeighborsIdExcept(self, agentId):
        neighbors = []
        if self.leftNeighbor != None and self.leftNeighbor.id != int(agentId):
            neighbors.append(int(self.leftNeighbor.id))
        if self.rightNeighbor != None and self.rightNeighbor.id != int(agentId):
            neighbors.append(int(self.rightNeighbor.id))
        if self.frontNeighbor != None and self.frontNeighbor.id != int(agentId):
            neighbors.append(int(self.frontNeighbor.id))
        return neighbors

    ###
    # Update state of the device.
    # If it's a new one, the device is added to the Agent's list 
    def updateDevice(self, device):

        deviceExist = False

        for d in self.deviceList :
            if d.id == device.id :
                d = device
                deviceExist = True
                break

        if not deviceExist :
            self.deviceList.append(device)

    ###
    # toString for neighbors
    def toStringNeighbors(self):
        string = "ROOM " + str(self.id) + " : \n"

        if self.leftNeighbor != None :
            string += " | LeftNeighbor : " + str(self.leftNeighbor.id) + "\n"

        if self.rightNeighbor != None :
            string += " | RightNeighbor : " + str(self.rightNeighbor.id) + "\n"

        if self.frontNeighbor != None :
            string += " | FrontNeighbor : " + str(self.frontNeighbor.id) + "\n"
        
        return string

    ###
    # toString
    def toString(self):
        string = "ROOM " + str(self.id) + " : \n"
        string += "Tau : " + str(self.tau) + "\n"

        for device in self.deviceList :
            string += device.toString()

        return string
        
        





