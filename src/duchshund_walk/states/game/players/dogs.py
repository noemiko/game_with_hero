import pygame as pg
from duchshund_walk.settings import COSMOS_GRAVITATION
from duchshund_walk.settings import EARTH_GRAVITATION
from duchshund_walk.settings import GROUND_POSITION_Y
from duchshund_walk.settings import MAX_BULLETS
from duchshund_walk.states.game.players.base import Bullet
from duchshund_walk.states.game.players.base import Player
from duchshund_walk.utils import get_dog_image_folder
from duchshund_walk.utils import get_images
from duchshund_walk.utils import merge_images
from duchshund_walk.utils import scale_images


class Duchshund(Player):
    def __init__(self, x, y):
        Player.__init__(self, x, y)
        self.jump_heigh = 250
        self.ground_level = GROUND_POSITION_Y
        self.bullets = []
        self.laser_sound_path = "./src/duchshund_walk/static/sounds/dog_laser.wav"
        self.jump_sound_path = "./src/duchshund_walk/static/sounds/dog_jump.wav"
        self.pain_sound_path = "./src/duchshund_walk/static/sounds/dog_pain.wav"

    def shoot(self):
        pg.mixer.init()
        if not len(self.bullets) < MAX_BULLETS:
            sound = pg.mixer.Sound(self.empty_gun_sound_path)
        else:
            sound = pg.mixer.Sound(self.laser_sound_path)
            bullet = Bullet(self.rect.x + 80, self.rect.y + 25)

            self.bullets.append(bullet)
        sound.play(0)

    def scream_in_pain(self):
        pg.mixer.init()
        sound = pg.mixer.Sound(self.pain_sound_path)
        if not pg.mixer.get_busy():
            sound.play(0)

    def cosmos_mode(self):
        self.g = COSMOS_GRAVITATION
        self.wear_cosmo_suit()

    def earth_mode(self):
        self.g = EARTH_GRAVITATION
        self.images_frames = self.load_images()

    def load_images(self):
        images_folder = get_dog_image_folder()
        images = get_images(images_folder)
        return scale_images(images, (100, 50))

    def wear_cosmo_suit(self):
        folder = get_dog_image_folder()
        images = get_images(folder)

        images_with_helmet = []
        for current_image in images:
            new_image = merge_images(current_image, "src/duchshund_walk/states/game/images/cosmos/dachshund_cosmo.png")
            images_with_helmet.append(new_image)

        images = scale_images(images_with_helmet, (100, 50))
        self.images_frames = images

    def jump(self):
        if self.is_on_the_ground():
            pg.mixer.init()
            sound = pg.mixer.Sound(self.jump_sound_path)
            sound.play(0)
            self.movey -= 100
            self.jump_velocity = 50
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

        if self.is_jumping:
            print("dog is during jump")
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= self.g

        if self.is_on_the_ground():
            self.jump_velocity = 0
            self.rect.y = self.ground_level
            self.is_jumping = False

        self.rect.topleft = self.rect.x, self.rect.y

        self.frame += 1
        if self.is_jumping:
            self.frame = 0
            self.image = self.images_frames[4]
            return
        elif self.frame > 8:
            self.frame = 0

        self.image = self.images_frames[self.frame]

    def __str__(self):
        return "Duchshund"
