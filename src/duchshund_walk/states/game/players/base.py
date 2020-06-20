import pygame as pg
from duchshund_walk.settings import EARTH_GRAVITATION
from duchshund_walk.settings import WHITE


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
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


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.images_frames = self.load_images()
        self.image = self.images_frames[0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.rect.x = x
        self.rect.y = y
        self.movey = 0
        self.is_jumping = False
        self.health = 100
        self.g = EARTH_GRAVITATION
        self.jump_velocity = 0
        self.empty_gun_sound_path = "./src/duchshund_walk/static/sounds/empty_gun.wav"

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
