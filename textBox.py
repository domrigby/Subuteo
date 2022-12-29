import pygame

class TextBox():

    def __init__(self,screen):
        self.screen = screen

    def showText(self,text,pos,size,textCol,bgCol):

        self.screenfont = pygame.font.Font('freesansbold.ttf', size) 
        screentext = self.screenfont.render(text, True, bgCol, textCol)
        screentextRect = screentext.get_rect()
        screentextRect.center = pos

        self.screen.blit(screentext, screentextRect)