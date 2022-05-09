import math

class Customer:
    def __init__(self, index, xCoord, yCoord, demand, readyTime, dueTime, serviceTime):
        self.index = index
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.demand = demand
        self.readyTime = readyTime
        self.dueTime = dueTime
        self.serviceTime = serviceTime

    def getDistance(self, node):
        return math.sqrt((node.xCoord - self.xCoord)**2 + (node.yCoord - self.yCoord)**2)

    def getDistanceCeil(self, node):
        return math.ceil(math.sqrt((node.xCoord - self.xCoord)**2 + (node.yCoord - self.yCoord)**2))

    def getAngle(self, node):
        degrees = math.degrees(math.atan2((node.xCoord - self.xCoord), (node.yCoord - self.yCoord)))
        degrees = (degrees + 360) % 360
        return degrees

