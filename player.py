import pygame
import os
from settings import animation_cycles
from settings import worldx, worldy
from settings import ty, tx

class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images_walk_right = self.get_walk_images()
        self.images_walk_left = self.get_walk_images(True)
        self.image = self.images_walk_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_jumping = False
        self.jump_frames = 10
        self.health = 0

    def gravity(self):

        self.movey += 3.2  # how fast player falls

        if self.rect.y > worldy and self.movey >= 0:
            self.movey = 0
            self.rect.y = worldy - ty - ty


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

    def update(self, enemy_list):
        """
        Update sprite position
        """

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 8 * animation_cycles:
                self.frame = 1
            self.image = self.images_walk_left[self.frame // animation_cycles]

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 8 * animation_cycles:
                self.frame = 1
            self.image = self.images_walk_right[(self.frame // animation_cycles)]

        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.health -= 1
            print(self.health)
