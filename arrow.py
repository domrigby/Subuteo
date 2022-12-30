import numpy as np
import numpy.linalg as la
import math

class Arrow():

    def __init__(self):
        self.arrowShape = [[0, 100], [0, 200], [200, 200], [200, 300], [300, 150], [200, 0], [200, 100]]

        for i in range(len(self.arrowShape)):
            self.arrowShape[i][1] = (self.arrowShape[i][1]-150)*0.25

    def plot(self,angle,length,vec):

        newPoints = []

        rotMat = np.array([[math.cos(angle),-math.sin(angle)],
                        [math.sin(angle),math.cos(angle)]])

        furthestPoint = 0

        for point in self.arrowShape:
            shapeLength = la.norm(point)
            if shapeLength > la.norm(furthestPoint):
                furthestPoint = point

        for i in range(len(self.arrowShape)):
            newPoints.append(np.multiply(length/la.norm(furthestPoint),self.arrowShape[i]))
            newPoints[i] = np.matmul(rotMat,newPoints[i])
            newPoints[i] += vec

        return newPoints

    def plotVec(self,pos,vec,scaleFac):
        angle = np.arctan2(vec[1],vec[0])
        length = scaleFac*la.norm(vec)
        points = self.plot(angle,length,pos)
        return points