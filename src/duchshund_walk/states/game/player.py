import pygame as pg
from duchshund_walk.settings import GROUND_POSITION_Y
from duchshund_walk.utils import get_images
from duchshund_walk.utils import scale_images


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, images_path):
        pg.sprite.Sprite.__init__(self)
        self.images_frames = self.load_images(images_path)
        self.image = self.images_frames[0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.rect.x = x
        self.rect.y = y
        self.movey = 0
        self.is_jumping = False
        self.health = 100
        self.jump_heigh = 150
        self.ground_level = 250

    def load_images(self, images_path):
        pass

    def is_on_the_ground(self):
        if self.rect.y >= self.ground_level:
            return True
        return False

    def is_on_the_top(self):
        if self.rect.y <= self.jump_heigh:
            return True
        return False

    def is_during_jump(self):
        if self.rect.y >= self.jump_heigh and self.rect.y < self.ground_level:
            return True
        return False

    def jump(self):
        if self.is_on_the_ground():
            self.movey -= 100
            self.is_jumping = True


class Duchshund(Player):
    def __init__(self, x, y, images_path):
        Player.__init__(self, x, y, images_path)
        self.jump_heigh = 250
        self.ground_level = GROUND_POSITION_Y

    def load_images(self, images_path):
        images = get_images(images_path)
        return scale_images(images, (100, 50))

    def jump(self):
        if self.is_on_the_ground():
            self.movey -= 100
            self.is_jumping = True

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.jump()

    def update(self, game_deltatime):
        """
        Update sprite position
        """

        slowdown = 3000.0
        player_speed = game_deltatime / slowdown
        if self.is_on_the_top():
            self.movey += 100
            self.is_jumping = False

        if self.is_on_the_ground() and not self.is_jumping:
            self.movey = 0
            self.rect.y = self.ground_level

        self.rect.y += self.movey * player_speed
        self.rect.topleft = self.rect.x, self.rect.y

        self.frame += 1
        if self.is_jumping or self.is_during_jump():
            self.frame = 0
            self.image = self.images_frames[4]
            return
        elif self.frame > 8:
            self.frame = 0

        self.image = self.images_frames[self.frame]


class Human(Player):
    def load_images(self, images_path):
        images = get_images(images_path)
        return scale_images(images, (150, 200))
        # return scale_images(images, (100, 150))

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == ord("w"):
                self.jump()

    def update(self, game_deltatime):
        slowdown = 300.0
        player_speed = game_deltatime / slowdown
        self.rect.y += self.movey * player_speed

        if self.is_on_the_top():
            self.movey += 100
            self.is_jumping = False

        if self.is_on_the_ground() and not self.is_jumping:
            self.movey = 0
            self.rect.y = 250

        if self.is_jumping or self.is_during_jump():
            self.image = self.images_frames[2]
            self.frame = 0
            return

        elif self.frame == 3:
            self.frame = 0

        self.image = self.images_frames[int(self.frame)]
        self.frame += 0.5
