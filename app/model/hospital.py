#! python3
# hospital.py - Implement the environment model for testing/configuring

from model.room import Room

class Hospital(object):

    ###
    # For now : generate a specific environment
    def __init__(self, size):
        self.roomList = []

        for i in range(1, size + 1):
            self.roomList.append(Room(i))

        self.setupNeighbors()

    ###
    # Setup neighbors on two lines (cf. code Java). 
    def setupNeighbors(self):

        moitieAgent = int(len(self.roomList) / 2)
        leftSide = self.roomList[0:moitieAgent]
        rightSide = self.roomList[moitieAgent:len(self.roomList)]

        for k in range(0, moitieAgent):
            
            leftCurrent = leftSide[k]
            rightCurrent = rightSide[k]

            if k == 0 :
                leftCurrent.setLeftNeighbor(rightCurrent)
                rightCurrent.setLeftNeighbor(leftCurrent)

            if k > 0 :
                leftCurrent.setLeftNeighbor(leftSide[k - 1])
                rightCurrent.setLeftNeighbor(rightSide[k - 1])

            if k < moitieAgent - 1 :
                leftCurrent.setRightNeighbor(leftSide[k + 1])
                rightCurrent.setRightNeighbor(rightSide[k + 1])

            if k == moitieAgent - 1 :
                leftCurrent.setRightNeighbor(rightCurrent)
                rightCurrent.setRightNeighbor(leftCurrent)

            if k > 0 and k < moitieAgent - 1 :
                leftCurrent.setFrontNeighbor(rightCurrent)
                rightCurrent.setFrontNeighbor(leftCurrent)

    def toString(self):
        string = ""
        for room in self.roomList :
            string += room.toString()
        return string
