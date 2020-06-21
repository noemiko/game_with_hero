from abc import abstractmethod

import pygame as pg
from duchshund_walk.settings import COSMOS_GRAVITATION
from duchshund_walk.settings import EARTH_GRAVITATION
from duchshund_walk.settings import MAX_BULLETS
from duchshund_walk.states.game.players.base import Bullet
from duchshund_walk.states.game.players.base import Player
from duchshund_walk.states.game.players.base import PlayerImages
from duchshund_walk.states.game.players.base import PlayerSounds
from duchshund_walk.utils import get_human_image_folder
from duchshund_walk.utils import get_images
from duchshund_walk.utils import merge_images
from duchshund_walk.utils import scale_images


class Human(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ground_level = y
        self.bullets = []
        self.sounds = PlayerSounds(
            laser_shoot=pg.mixer.Sound("./src/duchshund_walk/static/sounds/human_laser.wav"),
            # scream=pg.mixer.Sound("./src/duchshund_walk/static/sounds/dog_pain.wav"),
            jump=pg.mixer.Sound("./src/duchshund_walk/static/sounds/human_jump_.wav"),
            empty_gun=pg.mixer.Sound("./src/duchshund_walk/static/sounds/empty_gun.wav"),
        )

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
        if not pg.mixer.get_busy():
            self.sounds["scream"].play(0)

    def cosmos_mode(self):
        self.g = COSMOS_GRAVITATION
        self.current_frames = self.images["cosmos"]

    def earth_mode(self):
        self.g = EARTH_GRAVITATION
        self.current_frames = self.images["earth"]

    def load_cosmos_images(self, folder):
        images = get_images(folder)
        images_with_helmet = []
        for current_image in images:
            new_image = merge_images(current_image, self.cosmo_helmet_path)
            images_with_helmet.append(new_image)

        images = scale_images(images_with_helmet, (150, 200))
        return images

    def jump(self):
        if self.is_on_the_ground():
            pg.mixer.init()
            self.sounds["jump"].play(0)
            self.jump_velocity = 50
            self.movey -= 100
            self.is_jumping = True

    def load_images(self):
        images_folder = get_human_image_folder()
        cosmo_images = self.load_cosmos_images(images_folder)
        earth_images = get_images(images_folder)
        print(cosmo_images)
        print(earth_images)
        images = PlayerImages(
            cosmos=scale_images(cosmo_images, (150, 200)), earth=scale_images(earth_images, (150, 200))
        )
        print(images)
        return images

    def get_event(self, event):
        if event.key == ord("w"):
            print("button `w` pressed")
            self.jump()
        if event.key == pg.K_RETURN:
            print("button `enter` pressed")
            self.shoot()

    def shoot(self):
        pg.mixer.init()
        if not len(self.bullets) < MAX_BULLETS:
            sound = self.sounds["empty_gun"]
        else:
            sound = self.sounds["laser_shoot"]
            bullet = Bullet(self.rect.x + 110, self.rect.y + 25)
            self.bullets.append(bullet)
        sound.play(0)

    def update(self):
        if self.is_jumping:
            print("human is during jump")
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= self.g

        if self.is_on_the_ground():
            self.jump_velocity = 0
            self.rect.y = self.ground_level
            self.is_jumping = False

        if self.is_jumping:
            self.image = self.current_frames[2]
            self.frame = 0
            return

        elif self.frame == 3:
            self.frame = 0

        self.image = self.current_frames[int(self.frame)]
        self.frame += 0.5


class Girl(Human):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sounds["scream"] = pg.mixer.Sound("./src/duchshund_walk/static/sounds/woman-pain.wav")

    @property
    def cosmo_helmet_path(self):
        return "src/duchshund_walk/states/game/images/cosmos/cosmo_helmet_girl.png"

    def __str__(self):
        return "Girl"


class Mark(Human):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sounds["scream"] = pg.mixer.Sound("./src/duchshund_walk/static/sounds/pain.wav")

    @property
    def cosmo_helmet_path(self):
        return "src/duchshund_walk/states/game/images/cosmos/cosmo_helmet_mark.png"

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
