from typing import List
from typing import TypedDict

import pygame as pg
from duchshund_walk.settings import EARTH_GRAVITATION
from duchshund_walk.settings import WHITE
from pygame import Surface
from pygame.mixer import Sound


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((25, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speedy = +10

    def update(self):
        self.rect.x += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class PlayerImages(TypedDict):
    cosmos: List[Surface]
    earth: List[Surface]


class PlayerSounds(TypedDict):
    laser_shoot: Sound
    scream: Sound
    jump: Sound
    empty_gun: Sound


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images: PlayerImages = self.load_images()
        self.current_frames: List[Surface] = self.images["earth"]
        self.image: Surface = self.current_frames[0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.rect.x = x
        self.rect.y = y
        self.movey = 0
        self.is_jumping: bool = False
        self.health: int = 100
        self.g: int = EARTH_GRAVITATION
        self.jump_velocity = 0

    def load_images(self):
        pass

    def is_on_the_ground(self):
        if self.rect.y >= self.ground_level:
            return True
        return False

    def is_on_the_top(self):
        if self.rect.y <= self.jump_heigh:
            return True
        return False

    def jump(self):
        pass
