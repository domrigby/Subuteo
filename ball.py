import pygame
import numpy as np
import numpy.linalg as la

class Ball():

    def __init__(self,screen,spawnPos):
        self.screen = screen
        self.spawnPos = spawnPos

        self.pos = np.array(spawnPos)

        self.colour = (255,255,255)

        self.size = 25
        self.vel: float = 0.0

        self.lastUpdateTime = 0

        self.drag = 0.002
        self.constantGrassDrag = 10

    def drawBall(self):
        pygame.draw.circle(self.screen,self.colour,self.pos,self.size)

    def updateState(self,deltaT):

        acc = np.multiply(self.vel,-self.drag*la.norm(self.vel)) + np.multiply(self.vel/la.norm(self.vel),-self.constantGrassDrag)

        self.pos = self.pos + np.multiply(self.vel,deltaT)+np.multiply(acc,deltaT**(2)/2)
        self.vel = self.vel + np.multiply(acc,deltaT)

        if self.pos[0] < 0 or self.pos[0] > self.screen.get_size()[0]:
            self.vel[0] *= -1
            if self.pos[0] < 0 :
                self.pos[0] = 0
            else:
                self.pos[0] = self.screen.get_size()[0]
        
        if self.pos[1] < 0 or self.pos[1] > self.screen.get_size()[1]:
            self.vel[1] *= -1
            if self.pos[1] < 0 :
                self.pos[1] = 0
            else:
                self.pos[1] = self.screen.get_size()[1]
    
    def addVel(self,vel):
        self.vel = np.add(self.vel,np.array(vel))

    def reset(self):
        self.pos = self.spawnPos
        self.vel = np.array([0,0])
