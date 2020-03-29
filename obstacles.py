from random import randint

import pygame

from utils import get_images
from utils import scale_images


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        images = get_images(self.images_folder)
        self.images = scale_images(images, self.images_scale)
        self.image = self.get_current()
        self.rect = self.image.get_rect()
        self.x = 800
        self.y = 350
        self.rect.move_ip(self.x, self.y)
        self.dx = -15

    @property
    def images_folder(self):
        return "obstacles/cactuses"

    @property
    def images_scale(self):
        return (50, 70)

    def update(self):
        self.rect = self.rect.move(self.dx, 0)

    def get_current(self):
        rand = randint(0, len(self.images) - 1)
        return self.images[rand]


class Cactus(Obstacle):
    @property
    def images_folder(self):
        return "obstacles/cactuses"

    @property
    def images_scale(self):
        return (50, 70)


class Flower(Obstacle):
    @property
    def images_folder(self):
        return "obstacles/flowers"

    @property
    def images_scale(self):
        return (80, 100)


class Windmill(Obstacle):

    @property
    def images_folder(self):
        return "obstacles/windmills"

    @property
    def images_scale(self):
        return (100, 120)


class Stone(Obstacle):
    @property
    def images_folder(self):
        return "obstacles/stones"

    @property
    def images_scale(self):
        return (70, 90)
