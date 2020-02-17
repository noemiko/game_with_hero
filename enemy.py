import pygame
from settings import ALPHA
import os

from settings import animation_cycles


class Enemy(pygame.sprite.Sprite):
    '''
    Spawn an enemy
    '''
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = self.get_walk_images()
        self.images_left = self.get_walk_images(True)
        self.image = self.images[0]
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.frame = 0
        self.rect.x = x
        self.rect.y = y
        self.counter = 0 # counter variable

    def get_walk_images(self, mirrored=False):
        images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('images', 'hero' + str(i) + '_kol_filled.png'))
            img = pygame.transform.scale(img, (100, 150), )
            img.convert_alpha()
            if mirrored:
                img = pygame.transform.flip(img, True, False)
            images.append(img)
        return images

    def move(self):
        '''
        enemy movement
        '''
        speed = 8

        if self.frame == 4:
            self.frame = 1


        if self.counter >= 0 and self.counter <= 80:
            self.rect.x += speed
            self.image = self.images[self.frame // animation_cycles]

        elif self.counter >= 80 and self.counter <= 80*2:
            self.rect.x -= speed
            self.image = self.images_left[self.frame // animation_cycles]
        else:
            self.counter = 0



        self.frame += 1
        self.counter += 1
