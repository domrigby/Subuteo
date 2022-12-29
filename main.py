import pygame

import numpy as np
import numpy.linalg as la
import math

from pitch import Pitch
from player import Player
from menu import GameMenu
from arrow import Arrow
from ball import Ball
from textBox import TextBox

from typing import List
import time
import threading

def rotateVec(vec,angle):

    rotMat = np.array([[math.cos(angle), -math.sin(angle)],
                       [math.sin(angle),  math.cos(angle)]])
    
    return np.matmul(rotMat,vec)

def spawnTeams(teamNum,teamColour,screen,pitch,teamSize,otherTeam):
    teamplayers: List[Player] = []

    for i in range(teamSize):
        pitch.drawPitch()

        screenfont = pygame.font.Font('freesansbold.ttf', 32)
        screentext = screenfont.render(f"Place team {teamNum} by clicking!", True, (255,255,255), (0,0,0))
        screentextRect = screentext.get_rect()
        screentextRect.center = (1000,100)

        screen.blit(screentext, screentextRect)

        for player in teamplayers:
            player.drawPlayer()

        if otherTeam != None:
            for player in otherTeam:
                player.drawPlayer()

        clicked = False

        pygame.display.update()

        while not clicked:
            for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_presses = pygame.mouse.get_pressed()

                        if mouse_presses[0]:
                            mousePos = pygame.mouse.get_pos()
                            teamplayers.append(Player(screen,teamColour,mousePos,time.perf_counter()))
                            clicked = True

    return teamplayers

def calculateDistances(player,otherPlayers):
    for otherPlayer in otherPlayers:
        distVec = otherPlayer.pos - player.pos
        
        if la.norm(distVec) < 2*player.size and la.norm(distVec) > 0:
            print(np.dot(player.vel,distVec))
            if np.dot(player.vel,distVec) > 0.1: # make sure ball is still travelling towards eachother, not perform calc again
                print("Vel before: ",player.vel)
                # switch to collision space
                distVecUnit = distVec/la.norm(distVec)
                velParalellToCollis = np.dot(distVecUnit,player.vel) # velocity in direction of collision

                perpVec = rotateVec(distVecUnit,-math.pi/2)
                velPerpToCollis = np.dot(perpVec,player.vel) # velcoity perp to collision, doesnt change
                # if ellastic... complete transfer of KE to other ball
                firstBallVelColFrame = np.array([0,velPerpToCollis])
                secondBallVelColFrame = np.array([velParalellToCollis,0])

                xInColFrame = [np.dot([1,0],distVecUnit),np.dot([1,0],perpVec)]
                yInColFrame = [np.dot([0,1],distVecUnit),np.dot([0,1],perpVec)]

                print("x :",xInColFrame)
                print("y: ",yInColFrame)

                firstBallVel = [np.dot(xInColFrame,firstBallVelColFrame), np.dot(yInColFrame,firstBallVelColFrame)]
                secondBallVel = [np.dot(xInColFrame,secondBallVelColFrame), np.dot(yInColFrame,secondBallVelColFrame)]

                print("Ball 1: ",firstBallVel)
                print("Ball 2: ",secondBallVel)

                player.vel = firstBallVel
                otherPlayer.vel = secondBallVel
                otherPlayer.lastUpdateTime = time.perf_counter()




def checkHits(playersMoving,team1,team2,ball):
    allPlayers = team1 + team2 + ball
    threads: List[threading.Thread] = []
    
    for player in playersMoving:
        threads.append(threading.Thread(target=calculateDistances,args=(player,allPlayers)))
        threads[-1].start()
        
    for thread in threads:
        thread.join()

def checkMoving(movingList,itemList):

    for player in itemList:
        if la.norm(player.vel) > 0.1:
            player.updateState(time.perf_counter()-player.lastUpdateTime)
            player.lastUpdateTime = time.perf_counter()
            movingList.append(player)

    return movingList

def checkGoal(ballPos,score,goalWidth,pitchWidth,pitchHeight):

    goal = False
    team = ""
    
    if ballPos[0] <= 0: # possibility of goal for team2
        if (pitchHeight/2 - goalWidth/2) < ballPos[1] < (pitchHeight/2 + goalWidth/2):
            score[1] += 1
            goal = True
            team = "Blue Team"

    if ballPos[0] >= pitchWidth: # possibility of goal for team2
        if (pitchHeight/2 - goalWidth/2) < ballPos[1] < (pitchHeight/2 + goalWidth/2):
            score[0] += 1
            goal = True
            team = "Red Team"

    return score, goal, team

def main():

    score = [0,0]

    pitchHeight = 900
    pitchWidth = 1720

    pygame.init()

    screen = pygame.display.set_mode((pitchWidth,pitchHeight))

    pitch = Pitch(screen,pitchWidth,pitchHeight)

    params = GameMenu(pitchWidth,pitchHeight)

    arrow = Arrow()

    ball = Ball(screen,np.array(screen.get_size())/2)

    scoreText = TextBox(screen)

    params.showMenu(screen)

    team1 = spawnTeams(1,"red",screen,pitch,params.playersNum,None)
    team2 = spawnTeams(2,"blue",screen,pitch,params.playersNum,team1)

    player1Go = True
    mouseDown = False

    while True:
        pitch.drawPitch()
        ball.drawBall()

        for player in team1:
            player.drawPlayer()

        for player in team2:
            player.drawPlayer()


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()

                if mouse_presses[0]:
                    mousePos = pygame.mouse.get_pos()

                    if player1Go:
                        for player in team1:
                            if player.checkClick(mousePos):
                                mouseDown = True
                                clickedPlayer = player
                                origPos = np.array(mousePos)
                    else:
                        for player in team2:
                            if player.checkClick(mousePos):
                                mouseDown = True
                                clickedPlayer = player
                                origPos = np.array(mousePos)



            elif event.type == pygame.MOUSEBUTTONUP and mouseDown == True:
                mouseDown = False
                endPos = np.array(pygame.mouse.get_pos())
                velVec = (origPos - endPos)*10
                clickedPlayer.addVel(velVec) # add functions to player so they can have a velocity
                clickedPlayer.lastUpdateTime = time.perf_counter()
            

                if player1Go == True:
                    player1Go = False
                else:
                    player1Go = True

        if mouseDown == True:
            newPos = np.array(pygame.mouse.get_pos())
            mouseVec = newPos-origPos
            pygame.draw.polygon(screen, (255, 0, 0), arrow.plot(np.arctan2(mouseVec[1],mouseVec[0])+math.pi,la.norm(mouseVec),origPos))
        
        playersMoving = [] # players moving is a list of chips which are moving around, as we only have to check them for collisions

        playersMoving = checkMoving(playersMoving,team1)
        playersMoving = checkMoving(playersMoving,team2)
        playersMoving = checkMoving(playersMoving,[ball])

        if len(playersMoving) > 0:
            checkHits(playersMoving,team1,team2,[ball])
            
        score, goal, scoringTeam = checkGoal(ball.pos,score,pitch.goalWidth,pitchWidth,pitchHeight)

        if goal:
            ball.reset()
            for player in team1:
                player.reset()
            for player in team2:
                player.reset()
            scoreText.showText(f"Goal For {scoringTeam}",(pitchWidth/2 ,pitchHeight/2),100,(255,255,255),(255,0,0))
            pygame.display.update()
            time.sleep(2)
            
        scoreText.showText(f"{score[0]}",(50,50),50,(0,0,0),(255,255,255))
        scoreText.showText(f"{score[1]}",(pitchWidth-100,50),50,(0,0,0),(255,255,255))

        pygame.display.update()



if __name__ == "__main__":
    main()
