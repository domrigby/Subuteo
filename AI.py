import pygame
import numpy as np
import numpy.linalg as la
import math

class AIPlayer():

    def __init__(self,players,pitch):

        self.players = players
        self.pitch = pitch
        self.length = 0

    def calculateShot(self,ball,player):

        goalPos = np.array([0,self.pitch.pitchHeight/2])
        
        # calculate shotline
        gradient = (ball.pos[1]-goalPos[1])/(ball.pos[0]-goalPos[0])

        distPerX = np.sqrt(1+gradient**2)

        aimPointDist = ball.size + player.size

        numXAlong = aimPointDist/distPerX

        aimPoint = np.array([ball.pos[0]+numXAlong, gradient*(ball.pos[0]+numXAlong) + goalPos[1]])

        vel = np.multiply(aimPoint - player.pos,3)

        playerAimVec = player.pos - aimPoint
        ballToGoalVec = ball.pos - goalPos

        totalDist = la.norm(playerAimVec) + la.norm(ballToGoalVec)

        playerAimPointVec = player.pos - ball.pos
        ballAimPointVec = aimPoint - ball.pos

        angleOfAttack = math.acos(np.dot(playerAimPointVec,ballAimPointVec)/(la.norm(playerAimPointVec)*la.norm(ballAimPointVec)))

        return vel,totalDist,angleOfAttack

    def makeMove(self,ball):

        bestShotDist = 10e10 # just a high number
        bestShotAng = 10e10
        for player in self.players:
            shotVel, distance, angle = self.calculateShot(ball,player)
            #if distance < bestShotDist:
                #bestShotDist = distance
            if angle < bestShotAng:
                bestShotAng = angle
                bestPlayer = player
                bestShot = shotVel

        return bestPlayer, bestShot





