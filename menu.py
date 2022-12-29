import pygame

from button import Button

import time

import math


class GameMenu():

    def __init__(self,screenWidth,screenHeight):
        self.playersNum = 1
        self.speedMult = 1

        self.playersUp = Button(
                "More",
                (screenWidth/2 + 300, screenHeight/2),
                font=30,
                bg="navy",
                feedback="You clicked me")

        self.playersDown = Button(
                "Less",
                (screenWidth/2 - 300, screenHeight/2),
                font=30,
                bg="navy",
                feedback="You clicked me")
        
        self.start = Button(
                "Start game",
                (screenWidth/2 , screenHeight/2+200),
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
            screen.fill((255,255,255))
            self.playersUp.show(screen)
            self.playersDown.show(screen)
            self.start.show(screen)

            self.text = self.font.render(f"Players per side: {self.playersNum}", True, (0,0,0), (255,0,0))

            screen.blit(self.text, self.textRect)

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
                        elif self.start.clicked(mousePos):
                            menuQuit = True

