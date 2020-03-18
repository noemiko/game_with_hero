import pygame
import os
from settings import animation_cycles
from settings import worldx, worldy
from settings import ty, tx
from settings import ground_position_y

class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.movex = 0  # dx speed in x axis
        self.movey = 0  # dy speed on y axis
        self.frame = 0
        self.images_walk_right = self.get_walk_images()
        # self.images_walk_left = self.get_walk_images(True)
        self.image = self.images_walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x  # player x position
        self.rect.y = y  # player x positiony
        self.is_jumping = False
        self.health = 0
        # self.collide_rect_ratio(0.7)

    def get_walk_images(self, mirrored=False):
        images = []
        for i in range(0, 9):
            # img = pygame.image.load(os.path.join('images', 'hero' + str(i) + '_kol_filled.png'))
            img = pygame.image.load(os.path.join('images', 'jamnik_przezroczysty000' + str(i) + '.png'))
            img = pygame.transform.scale(img, (100, 50), )
            img.convert_alpha()
            if mirrored:
                img = pygame.transform.flip(img, True, False)
            images.append(img)
        return images

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y

    def onTheGround(self):
        if self.rect.y >= ground_position_y:
            return True
        return False

    def onTheTop(self):
        if self.rect.y <= 250:
            return True
        return False

    def jump(self):
        if self.onTheGround():
            self.movey -= 100
            self.is_jumping = True

    def update(self, deltatime):
        """
        Update sprite position
        """

        if self.onTheTop():
            self.movey += 50
            self.is_jumping = False

        if self.onTheGround() and not self.is_jumping:
            self.movey = 0
            self.rect.y = 350

        # self.rect.x = self.rect.x + self.movex
        # self.rect.y = self.rect.y + self.movey
        self.rect.y += self.movey * deltatime
        self.rect.topleft = self.rect.x, self.rect.y
        # # moving left
        # if self.movex < 0:
        #     self.frame += 1
        #     if self.frame > 8 * animation_cycles:
        #         self.frame = 1
        #     self.image = self.images_walk_left[self.frame // animation_cycles]

        # moving right
        # if self.movex > 0:
        self.frame += 1
        if self.is_jumping:
            self.image = self.images_walk_right[4]
            self.frame = 0
        elif self.frame > 8 * animation_cycles:
            self.frame = 0
        self.image = self.images_walk_right[(self.frame // animation_cycles)]


        # hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        # for enemy in hit_list:
        #     self.health -= 1
        #     print(self.health)
