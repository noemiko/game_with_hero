import pygame as pg
from duchshund_walk.settings import COSMOS_GRAVITATION
from duchshund_walk.settings import EARTH_GRAVITATION
from duchshund_walk.settings import GROUND_POSITION_Y
from duchshund_walk.settings import MAX_BULLETS
from duchshund_walk.states.game.players.base import Bullet
from duchshund_walk.states.game.players.base import Player
from duchshund_walk.states.game.players.base import PlayerImages
from duchshund_walk.states.game.players.base import PlayerSounds
from duchshund_walk.utils import get_dog_image_folder
from duchshund_walk.utils import get_images
from duchshund_walk.utils import merge_images
from duchshund_walk.utils import scale_images


class Duchshund(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.jump_heigh = 250
        self.ground_level = GROUND_POSITION_Y
        self.bullets = []
        self.sounds = PlayerSounds(
            laser_shoot=pg.mixer.Sound("./src/duchshund_walk/static/sounds/dog_laser.wav"),
            scream=pg.mixer.Sound("./src/duchshund_walk/static/sounds/dog_pain.wav"),
            jump=pg.mixer.Sound("./src/duchshund_walk/static/sounds/dog_jump.wav"),
            empty_gun=pg.mixer.Sound("./src/duchshund_walk/static/sounds/empty_gun.wav"),
        )

    @property
    def cosmo_helmet_path(self):
        return "./src/duchshund_walk/states/game/images/cosmos/dachshund_cosmo.png"

    def shoot(self):
        pg.mixer.init()
        if not len(self.bullets) < MAX_BULLETS:
            sound = self.sounds["empty_gun"]
        else:
            sound = self.sounds["laser_shoot"]
            bullet = Bullet(self.rect.x + 80, self.rect.y + 25)

            self.bullets.append(bullet)
        sound.play(0)

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

    def load_images(self):
        images_folder = get_dog_image_folder()
        cosmo_images = self.load_cosmos_images(images_folder)
        earth_images = get_images(images_folder)
        images = PlayerImages(cosmos=scale_images(cosmo_images, (100, 50)), earth=scale_images(earth_images, (100, 50)))
        return images

    def load_cosmos_images(self, folder):
        images = get_images(folder)

        images_with_helmet = []
        for current_image in images:
            new_image = merge_images(current_image, self.cosmo_helmet_path)
            images_with_helmet.append(new_image)

        images = scale_images(images_with_helmet, (100, 50))
        return images

    def jump(self):
        if self.is_on_the_ground():
            pg.mixer.init()
            self.sounds["jump"].play(0)
            self.movey -= 100
            self.jump_velocity = 50
            self.is_jumping = True

    def get_event(self, event):
        if event.key == pg.K_SPACE:
            self.jump()
        elif event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
            print("button `e` pressed")
            self.shoot()

    def update(self):
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
            self.image = self.current_frames[4]
            return
        elif self.frame > 8:
            self.frame = 0

        self.image = self.current_frames[self.frame]

    def __str__(self):
        return "Duchshund"
