import pygame
import os
from random import randint


class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        cactusImg = []
        for i in range(1, 5):
            # img = pygame.image.load(os.path.join('images', 'hero' + str(i) + '_kol_filled.png'))
            img = pygame.image.load(os.path.join('images', 'kaktus' + str(i) + '.png'))
            img = pygame.transform.scale(img, (50, 70), )
            img.convert_alpha()
            cactusImg.append(img)

        rand = randint(0, 3)
        self.image = cactusImg[rand]
        self.rect = self.image.get_rect()
        self.x = 800
        self.y = 350
        self.rect.move_ip(self.x, self.y)
        self.dx = -15

    def update(self):
        self.rect = self.rect.move(self.dx, 0)
