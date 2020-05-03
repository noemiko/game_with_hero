import pygame as pg
from duchshund_walk.settings import BLUE
from duchshund_walk.settings import GROUND_POSITION_Y
from duchshund_walk.utils import get_dog_image_folder
from duchshund_walk.utils import get_human_image_folder
from duchshund_walk.utils import get_images
from duchshund_walk.utils import scale_images


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((25, 2))
        self.image.fill(BLUE)
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
        # self.jump_heigh = 150
        # self.ground_level = 250

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

    def is_during_jump(self):
        if self.rect.y >= self.jump_heigh and self.rect.y < self.ground_level:
            return True
        return False

    def jump(self):
        pass


class Duchshund(Player):
    def __init__(self, x, y):
        Player.__init__(self, x, y)
        self.jump_heigh = 250
        self.ground_level = GROUND_POSITION_Y
        self.bullets = []

    def shoot(self):
        bullet = Bullet(self.rect.x + 80, self.rect.y + 25)
        self.bullets.append(bullet)

    def load_images(self):
        images_folder = get_dog_image_folder()
        images = get_images(images_folder)
        return scale_images(images, (100, 50))

    def jump(self):
        if self.is_on_the_ground():
            self.movey -= 100
            self.is_jumping = True

    def get_event(self, event):
        if event.key == pg.K_SPACE:
            self.jump()
        elif event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
            print("button `e` pressed")
            self.shoot()

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

    def __str__(self):
        return "Duchshund"


class Human(Player):
    def __init__(self, x, y):
        Player.__init__(self, x, y)
        self.jump_heigh = 100
        self.ground_level = y

        self.bullets = []

    def jump(self):
        if self.is_on_the_ground():
            self.movey -= 100
            self.is_jumping = True

    def load_images(self):
        folder = get_human_image_folder()
        images = get_images(folder)
        return scale_images(images, (150, 200))
        # return scale_images(images, (100, 150))

    def get_event(self, event):
        if event.key == ord("w"):
            print("button `w` pressed")
            self.jump()
        if event.key == ord("e"):
            print("button `e` pressed")
            self.shoot()

    def shoot(self):
        bullet = Bullet(self.rect.x + 110, self.rect.y + 25)
        self.bullets.append(bullet)

    def update(self, game_deltatime):
        if self.is_jumping:
            print("human is during jump")
            slowdown = 300.0
            player_speed = game_deltatime / slowdown
            self.rect.y += self.movey * player_speed

        if self.is_on_the_top():
            self.movey += 100

        if self.is_on_the_ground():
            self.is_jumping = False

        if self.is_on_the_ground() and not self.is_jumping:
            self.movey = 0
            self.rect.y = self.ground_level

        if self.is_jumping or self.is_during_jump():
            self.image = self.images_frames[2]
            self.frame = 0
            return

        elif self.frame == 3:
            self.frame = 0

        self.image = self.images_frames[int(self.frame)]
        self.frame += 0.5

    def __str__(self):
        return "Human"
