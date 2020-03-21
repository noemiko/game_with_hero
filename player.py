import pygame
from settings import ground_position_y
from utils import get_scaled_images


class Duchshund(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movey = 0  # dy speed on y axis
        self.frame = 0
        self.images_frames = get_scaled_images("duchshund", (100, 50))
        self.image = self.images_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x  # player x position
        self.rect.y = y  # player y positiony
        self.is_jumping = False
        self.health = 0

    def is_on_the_ground(self):
        if self.rect.y >= ground_position_y:
            return True
        return False

    def is_on_the_top(self):
        if self.rect.y <= 250:
            return True
        return False

    def jump(self):
        if self.is_on_the_ground():
            self.movey -= 100
            self.is_jumping = True

    def is_during_jump(self):
        if self.rect.y >= 250 and self.rect.y <= ground_position_y:
            return True
        return False

    def update(self, game_deltatime):
        """
        Update sprite position
        """

        slowdown = 300.0
        player_speed = game_deltatime / slowdown
        if self.is_on_the_top():
            self.movey += 100
            self.is_jumping = False

        if self.is_on_the_ground() and not self.is_jumping:
            self.movey = 0
            self.rect.y = 350

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


class Human(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = get_scaled_images("human", (100, 150))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.rect.x = x
        self.rect.y = y
        self.movey = 0
        self.is_jumping = False

    def jump(self):
        if self.is_on_the_ground():
            self.movey -= 100
            self.is_jumping = True

    def is_on_the_ground(self):
        if self.rect.y >= 250:
            return True
        return False

    def is_on_the_top(self):
        if self.rect.y <= 150:
            return True
        return False

    def is_during_jump(self):
        if self.rect.y >= 150 and self.rect.y < 250:
            return True
        return False

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
            self.image = self.images[2]
            self.frame = 0
            return

        elif self.frame == 3:
            self.frame = 0

        self.image = self.images[int(self.frame)]
        self.frame += 0.5
