import pygame

from button import Button

import time

import math


class GameMenu():

    def __init__(self,screenWidth,screenHeight):
        self.playersNum = 1
        self.speedMult = 1
        self.onePlayerOn = False

        self.playersUp = Button(
                "More",
                (screenWidth/2+300, screenHeight/2-100),
                font=30,
                bg="navy",
                feedback="You clicked me")

        self.playersDown = Button(
                "Less",
                (screenWidth/2 - 300, screenHeight/2-100),
                font=30,
                bg="navy",
                feedback="You clicked me")

        self.onePlayer = Button(
                "One player",
                (screenWidth/2 - 300, screenHeight/2 + 100),
                font=30,
                bg="navy",
                feedback="You clicked me")

        self.twoPlayer = Button(
                "Two player",
                (screenWidth/2 + 300, screenHeight/2 + 100),
                font=30,
                bg="navy",
                feedback="You clicked me")
        
        self.start = Button(
                "Start game",
                (screenWidth/2 -50, screenHeight/2+300),
                font=30,
                bg="navy",
                feedback="You clicked me")

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(f"Players per side: {self.playersNum}", True, (0,0,0), (255,0,0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (screenWidth/2,(screenHeight/2)-300)

    def showMenu(self,screen):

        menuQuit = False

        while not menuQuit :
            screen.fill((138,244,138))
            self.playersUp.show(screen)
            self.playersDown.show(screen)
            self.onePlayer.show(screen)
            self.twoPlayer.show(screen)
            self.start.show(screen)

            self.text = self.font.render(f"Players per side: {self.playersNum}", True, (0,0,0), (255,0,0))

            screen.blit(self.text, self.textRect)

            if self.onePlayerOn:
                playerText = self.font.render(f"One player", True, (0,0,0), (255,0,0))

            else: 
                playerText = self.font.render(f"Two player", True, (0,0,0), (255,0,0))

            playersTextRect = playerText.get_rect()
            playersTextRect.center = (screen.get_size()[0]/2, screen.get_size()[1]/2)

            screen.blit(playerText, playersTextRect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()

                    if mouse_presses[0]:
                        mousePos = pygame.mouse.get_pos()
                        if self.playersUp.clicked(mousePos):
                            self.playersNum += 1
                        elif self.playersDown.clicked(mousePos):
                            self.playersNum -= 1
                        elif self.onePlayer.clicked(mousePos):
                            self.onePlayerOn = True
                        elif self.twoPlayer.clicked(mousePos):
                            self.onePlayerOn = False
                        elif self.start.clicked(mousePos):
                            menuQuit = True

