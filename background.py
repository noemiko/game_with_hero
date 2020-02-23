import pygame
import random
from settings import worldy, worldx
import os

class Background():
    def __init__(self):
        self.backgroundImg = []
        self.backgroundImg.append(pygame.image.load(os.path.join("images", "bg.png")))
        self.backgroundImg.append(pygame.image.load(os.path.join("images", "bg.png")))
        # self.backgroundImg.append(pygame.image.load('teren3.png'))
        self.rectBg = self.backgroundImg[0].get_rect()
        self.width = self.rectBg.width
        self.x = 0
        self.x2 = self.width
        self.y = 0
        self.dx = -10
        self.random1 = 0
        self.random2 = 1


    def update(self):
        self.x += self.dx
        if self.x <= -self.width:
            self.x = self.width
            self.random1 = random.randint(0,1)
        self.x2 += self.dx
        if self.x2 <= -self.width:
            self.x2 = self.width
            self.random2 = random.randint(0,1)



