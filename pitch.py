import pygame

class Pitch():

    def __init__(self,screen,pitchWidth,pitchHeight):
        self.pitchHeight = pitchHeight
        self.pitchWidth = pitchWidth

        self.pitchScreen = screen

        self.goalWidth = 200

        self.team1Score = 0
        self.team2Score = 0

    def drawPitch(self):

        self.pitchScreen.fill((0,204,0))

        # draw unfilled centre circle
        pygame.draw.circle(self.pitchScreen,(255,255,255),(self.pitchWidth/2,self.pitchHeight/2),100)
        pygame.draw.circle(self.pitchScreen,(0,204,0),(self.pitchWidth/2,self.pitchHeight/2),99)

        pygame.draw.line(self.pitchScreen,(255,255,255),(self.pitchWidth/2,0),(self.pitchWidth/2,self.pitchHeight))

        boxHeight = 300
        boxWidth = 250
        pygame.draw.rect(self.pitchScreen,(255,255,255),((0,(self.pitchHeight/2)-boxHeight),(boxWidth,2*boxHeight)))
        pygame.draw.rect(self.pitchScreen,(0,204,0),((0,(self.pitchHeight/2)-(boxHeight-1)),(boxWidth-1,(2*boxHeight-2))))

        pygame.draw.rect(self.pitchScreen,(255,255,255),((self.pitchWidth-boxWidth,(self.pitchHeight/2)-boxHeight),(boxWidth,2*boxHeight)))
        pygame.draw.rect(self.pitchScreen,(0,204,0),((self.pitchWidth-boxWidth+1,(self.pitchHeight/2)-(boxHeight-1)),(boxWidth-1,(2*boxHeight-2))))

        pygame.draw.circle(self.pitchScreen,(255,255,255),(0,self.pitchHeight/2-self.goalWidth/2),10)
        pygame.draw.circle(self.pitchScreen,(255,255,255),(0,self.pitchHeight/2+self.goalWidth/2),10)
        pygame.draw.circle(self.pitchScreen,(255,255,255),(self.pitchWidth,self.pitchHeight/2-self.goalWidth/2),10)
        pygame.draw.circle(self.pitchScreen,(255,255,255),(self.pitchWidth,self.pitchHeight/2+self.goalWidth/2),10)
