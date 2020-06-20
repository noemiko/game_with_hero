from abc import ABC
from abc import abstractmethod

import pygame as pg
from duchshund_walk.settings import COSMOS_GRAVITATION
from duchshund_walk.settings import EARTH_GRAVITATION
from duchshund_walk.settings import MAX_BULLETS
from duchshund_walk.states.game.players.base import Bullet
from duchshund_walk.states.game.players.base import Player
from duchshund_walk.utils import get_human_image_folder
from duchshund_walk.utils import get_images
from duchshund_walk.utils import merge_images
from duchshund_walk.utils import scale_images


class Human(Player, ABC):
    def __init__(self, x, y):
        Player.__init__(self, x, y)
        self.jump_heigh = 100
        self.ground_level = y
        self.bullets = []
        self.laser_sound_path = "./src/duchshund_walk/static/sounds/human_laser.wav"
        self.jump_sound_path = "./src/duchshund_walk/static/sounds/human_jump_.wav"

    @property
    @abstractmethod
    def cosmo_helmet_path(self):
        pass

    @property
    @abstractmethod
    def pain_sound_path(self):
        pass

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

    def wear_cosmo_suit(self):
        folder = get_human_image_folder()
        images = get_images(folder)

        images_with_helmet = []
        for current_image in images:
            new_image = merge_images(current_image, self.cosmo_helmet_path)
            images_with_helmet.append(new_image)

        images = scale_images(images_with_helmet, (150, 200))
        self.images_frames = images

    def jump(self):
        if self.is_on_the_ground():
            pg.mixer.init()
            sound = pg.mixer.Sound(self.jump_sound_path)
            sound.play(0)
            self.jump_velocity = 50
            self.movey -= 100
            self.is_jumping = True

    def load_images(self):
        folder = get_human_image_folder()
        images = get_images(folder)
        return scale_images(images, (150, 200))

    def get_event(self, event):
        if event.key == ord("w"):
            print("button `w` pressed")
            self.jump()
        if event.key == ord("e"):
            print("button `e` pressed")
            self.shoot()

    def shoot(self):
        pg.mixer.init()
        if not len(self.bullets) < MAX_BULLETS:
            sound = pg.mixer.Sound(self.empty_gun_sound_path)
        else:
            sound = pg.mixer.Sound(self.laser_sound_path)
            bullet = Bullet(self.rect.x + 110, self.rect.y + 25)
            self.bullets.append(bullet)
        sound.play(0)

    def update(self, game_deltatime):
        if self.is_jumping:
            print("human is during jump")
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= self.g

        if self.is_on_the_ground():
            self.jump_velocity = 0
            self.rect.y = self.ground_level
            self.is_jumping = False

        if self.is_jumping:
            self.image = self.images_frames[2]
            self.frame = 0
            return

        elif self.frame == 3:
            self.frame = 0

        self.image = self.images_frames[int(self.frame)]
        self.frame += 0.5


class Girl(Human):
    def __init__(self, x, y):
        super().__init__(x, y)

    @property
    def cosmo_helmet_path(self):
        return "src/duchshund_walk/states/game/images/cosmos/cosmo_helmet_girl.png"

    @property
    def pain_sound_path(self):
        return "./src/duchshund_walk/static/sounds/woman-pain.wav"

    def __str__(self):
        return "Girl"


class Mark(Human):
    def __init__(self, x, y):
        super().__init__(x, y)

    @property
    def cosmo_helmet_path(self):
        return "src/duchshund_walk/states/game/images/cosmos/cosmo_helmet_mark.png"

    @property
    def pain_sound_path(self):
        return "./src/duchshund_walk/static/sounds/pain.wav"

    def __str__(self):
        return "Mark"


class HumanFactory:
    def __new__(cls, hero_name, x, y):
        heroes_classes = {"girl": Girl, "mark": Mark}
        try:
            hero = heroes_classes[hero_name]
        except KeyError:
            raise ValueError("Unknown human hero")
        return hero(x, y)
