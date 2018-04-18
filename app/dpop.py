#! python3
# dpop.py - Implement the DPOP Algorithm
# It is a thread intended to be launched by an agent
#
# /!\ WARNING /!\
# The objective in this case is to MINIMIZE all constraints. 

from threading import Thread
from model.room import Room
from random import randint
from datetime import datetime

import time
import numpy
import json

class Dpop(Thread):

    DIMENSION = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 120, 180, 210, 241]
    T_SYNCHRO = 30
    TIMEOUT = 200

    def __init__(self, room, client, isRoot):
        Thread.__init__(self)

        self.v = None
        self.room = room
        self.mqttClient = client
        self.isRoot = isRoot
        
        self.open = None #neighbors Id
        self.children = [] #children Id
        self.parent = 0 #parent Id
        self.pseudo_children = [] #pseudo_children Id
        self.pseudo_parent = [] #pseudo_parents Id

        self.matrix_dimensions = [] #order or the variables that create the JOIN Matrix
        self.UTIL = None # UTIL matrix
        self.JOIN = None # JOIN matrix

    ###
    #/!\ Do the DPOP Algorithm /!\
    def run(self):
        print("---------- DFS GENERATION ----------")
        self.generatePseudoTree()
        print("---------- UTIL PROPAGATION ----------")
        self.utilPropagation()
        print("---------- VALUE PROPAGATION ----------")
        self.valuePropagation()

        self.mqttClient.loop_stop()
        self.mqttClient.disconnect()

    ###
    # Do the DFS Arrangement
    def generatePseudoTree(self):

        msg_buffer = []

        if self.room.getDegree() > 0 :
            if self.isRoot :
                self.open = self.room.getAllNeighborsId()
                self.children.append(self.open.pop(randint(0, len(self.open) - 1)))
                self.mqttClient.publish("DCOP/" + str(self.children[0]), "CHILD " + str(self.room.id))

            # MQTT wait for incoming message of type "messageType" from neighbor yi
            while 1 :
                
                if len(self.mqttClient.listMessagesAttente) == 0 :
                    continue

                if 'UTIL' in self.mqttClient.listMessagesAttente[0] or 'VALUE' in self.mqttClient.listMessagesAttente[0]:
                    # Wrong message : we keep him in a "buffer" for next steps
                    msg_buffer.append(self.mqttClient.listMessagesAttente.pop(0))
                    continue

                message = self.mqttClient.listMessagesAttente.pop(0).split(" ")
                messageType = message[0]
                yi = int(message[1])
                
                if self.open is None :
                    # First time the agent is visited
                    self.open = self.room.getAllNeighborsIdExcept(yi)
                    self.parent = yi                 
    
                elif "CHILD" in messageType and yi in self.open :
                    self.pseudo_children.append(self.open.pop(self.open.index(yi)))
                    self.mqttClient.publish("DCOP/" + str(yi), "PSEUDO " + str(self.room.id))
                    continue

                elif "PSEUDO" in messageType :
                    if yi in self.children : 
                        self.children.pop(self.children.index(yi))
                    self.pseudo_parent.append(yi)

                # Forward the CHILD message to the next "open" neighbor
                if len(self.open) > 0 :
                    yj = self.open[randint(0, len(self.open) - 1)]
                    self.children.append(self.open.pop(self.open.index(yj)))
                    self.mqttClient.publish("DCOP/" + str(yj), "CHILD " + str(self.room.id))
                else :
                    if not self.isRoot :
                        # Backtrack
                        self.mqttClient.publish("DCOP/" + str(self.parent), "CHILD " + str(self.room.id))

                    self.mqttClient.listMessagesAttente.extend(msg_buffer)
                    print(self.pseudoTreeToString())
                    return  

    ###
    # UTIL PROPAGATION
    def utilPropagation(self):
        
        count = 0
        msg_buffer = []
        start_time = datetime.now()
        
        if len(self.children) > 0 :
           
            # MQTT wait for incoming message of type UTIL for each child of the agent
            while count < len(self.children) and (datetime.now() - start_time).total_seconds() < self.TIMEOUT:
                if len(self.mqttClient.listMessagesAttente) == 0 :
                    continue

                if not 'UTIL' in self.mqttClient.listMessagesAttente[0]:
                    # Wrong message : we keep him in a "buffer" for next step
                    msg_buffer.append(self.mqttClient.listMessagesAttente.pop(0))
                    continue

                # We add to the join UTIL message from children as they arrive
                data_received = json.loads(self.mqttClient.listMessagesAttente.pop(0).split("UTIL ")[1])
                self.matrix_dimensions.extend(data_received["vars"])
                matrix_data = numpy.asarray(data_received["data"]) 
                self.JOIN = matrix_data if self.JOIN is None else self.JOIN + matrix_data
                count += 1

                self.matrix_dimensions = list(set(self.matrix_dimensions)) #Clean up duplicate entry

        if not self.isRoot :

            # Also join all relations with parent/pseudo_parent
            self.JOIN = self.combine(self.getUtilityFor(self.parent), self.JOIN)
        
            for pseudo_parent in self.pseudo_parent :
               self.JOIN = self.combine(self.getUtilityFor(pseudo_parent), self.JOIN)

        # Add to `self` constraint values
        self.JOIN = self.addMyUtility(self.JOIN)

        # Use projection to eliminate self out of message parent
        self.UTIL = self.project(self.JOIN)

        self.mqttClient.listMessagesAttente.extend(msg_buffer)

    ###
    # VALUE PROPAGATION
    def valuePropagation(self):
        
        values = {}
        start_time = datetime.now()

        if self.UTIL is None :
            self.UTIL = numpy.zeros(len(self.DIMENSION), dtype=int)

        if not self.isRoot :

            self.mqttClient.publish("DCOP/" + str(self.parent), "UTIL " + json.dumps({"vars": self.matrix_dimensions,"data": self.UTIL.tolist()}))

            # MQTT wait for incoming message of type VALUE from parent
            while (datetime.now() - start_time).total_seconds() < self.TIMEOUT :

                if len(self.mqttClient.listMessagesAttente) == 0 :
                    continue

                values = json.loads(self.mqttClient.listMessagesAttente.pop(0).split("VALUES ")[1])
                break
            
        # Find best v
        index = self.getIndexOfBestValueWith(values, self.JOIN)                
        self.v = self.DIMENSION[index]
        values[str(self.room.id)] = index

        for child in self.children :
            self.mqttClient.publish("DCOP/" + str(child), "VALUES " + json.dumps(values))

        print("FINAL v : " + str(self.v))
        print("C1 : ", self.c1(self.v))
        print("C5 : ", self.c5(self.v))

    ###################################################
    ###          METHODS UTILS                      ###
    ###################################################

    ###
    # Find the index of best value for the variable depending on the other values
    def getIndexOfBestValueWith(self, data, matrix):

        if matrix is None :
            raise Exception("Matrice NULL pour la méthode dpop.getIndexOfBestValueWith(...)")

        if len(matrix.shape) == 1 or matrix.shape[1] == 1 :
            return min((matrix[i], i) for i in range(len(matrix)))[1]

        if data is None or not type(data) is dict :
            raise Exception("Données manquantes pour la méthode dpop.getIndexOfBestValueWith(...)")

        bestIndex = 0
        var_vals = {}
        tupl = tuple()
        bestValue = 242
        parents = self.pseudo_parent
        parents.append(self.parent)

        #Check for parents values
        for parent_id in parents :
            key = str(parent_id)
            if key in data :
                tupl = tupl + (data[key],)

        #Check for dependant non-neighbors values if needed
        for neighbor_id in self.matrix_dimensions :
            
            if len(matrix.shape) - 1 == len(tupl) :
                break
            
            key = str(neighbor_id)
            if key in data :
                tupl = tupl + (data[key],)

        for index, value in numpy.ndenumerate(matrix) :
            if tupl == index[1:] :
                if value < bestValue :
                    bestValue = value
                    bestIndex = index[0]

        print("TUPLE FOR DECISION :", tupl)
        print("BEST VALUE", bestValue)

        return bestIndex
        

    ###
    # PROJECT the variable out of the matrix
    def project(self, matrix):
        return numpy.amin(matrix, axis=1) if len(matrix.shape) > 1 else matrix
                        

    ###
    # JOIN/COMBINE two matrix
    def combine(self, matrix1, matrix2):

        if matrix1 is None and matrix2 is None :
            raise Exception("Matrices Null !")

        if matrix1 is None :
            return matrix2

        if matrix2 is None :
            return matrix1

        if matrix1.size > matrix2.size :
            finalMatrix = numpy.zeros(matrix1.shape + (matrix1.shape[0],), dtype=int)
        else :
            finalMatrix = numpy.zeros(matrix2.shape + (matrix2.shape[0],), dtype=int)
        
        for index1, value1 in numpy.ndenumerate(matrix1) :
            for index2, value2 in numpy.ndenumerate(matrix2) :
                if index1[0] == index2[0] :
                    tupl = tuple(numpy.concatenate((numpy.array(index1), numpy.delete(numpy.array(index2), 0, 0))))
                    finalMatrix[tupl] = value1 + value2
                
        print("SHAPE OF COMBINED MATRIX : " + str(finalMatrix.shape))
        return finalMatrix
        

    ###
    # Calculate the R matrix depending on parent
    def getUtilityFor(self, parent):

        R = numpy.zeros((len(self.DIMENSION), len(self.DIMENSION)), dtype=int)

        if parent in self.matrix_dimensions :
            return None

        for i in range(0, len(self.DIMENSION)) :
            for j in range (0, len(self.DIMENSION)) :
                R[i][j] += self.c3(self.DIMENSION[i], self.DIMENSION[j])

        self.matrix_dimensions.append(parent)
        return R

    ###
    # Add the utility of the self agent in the matrix
    # This is needeed because he is the only one to know those constraints
    def addMyUtility(self, R):

        if R is None :
            R = numpy.zeros(len(self.DIMENSION), dtype=int)
        
        for index, value in numpy.ndenumerate(R) :
            R[index] += self.c1(self.DIMENSION[index[0]])
            R[index] += self.c5(self.DIMENSION[index[0]])
        return R      

    ###
    # Convert pseudoTree in String format
    def pseudoTreeToString(self):
        
        string = str(self.room.id) + "\n"
        
        for childId in self.children :
            string += "| " + str(childId) + "\n"
        
        for pseudoId in self.pseudo_parent :
            string += "--> " + str(pseudoId) + "\n"

        for pseudoId in self.pseudo_children :
            string += "<-- " + str(pseudoId) + "\n"
        
        return string

    ###################################################
    ###          CONSTRAINTS                        ###
    ###################################################

    def c1(self, vi):
        if len(self.room.deviceList) == 0 and vi < 241 :
            return 10
        return 0

    def c3(self, vi, vj):
        val = abs(vi - vj)
        if val <= self.T_SYNCHRO and val != 0 :
            return 1
        return 0

    def c5(self, vi):
        
        etatCritic = False
        minEtatProg = 241
        for device in self.room.deviceList :
            if device.inCriticalState :
                etatCritic = True
                break
            if device.endOfProgram < minEtatProg :
                minEtatProg = device.endOfProgram

        if not etatCritic and minEtatProg > 30 and self.room.tau < 180 and vi < 240 :
            return 1
        
        return 0
