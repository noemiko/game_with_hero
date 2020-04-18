import os

import pygame as pg
from duchshund_walk.app_core import States
from duchshund_walk.settings import PROJECT_PATH
from duchshund_walk.settings import WHITE
from duchshund_walk.settings import WORLD_HEIGH
from duchshund_walk.settings import WORLD_WIDTH
from duchshund_walk.states.game.player import Duchshund
from duchshund_walk.utils import get_images
from duchshund_walk.utils import scale_images


class HeroesPicker(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"
        self.dog = Duchshund(WORLD_WIDTH / 8 + 50, WORLD_HEIGH / 2)
        self.dog.ground_level = WORLD_HEIGH / 2 / 2
        dog_image = get_images("duchshund/with_bow_tie")
        images = scale_images(dog_image, (250, 200))
        self.dog.images_frames = images

    def startup(self):
        print("starting HeroesPicker state stuff")

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, deltatime):
        self.draw(screen)
        path = os.path.join(PROJECT_PATH, "states/game/images/stage.png")
        carImg = pg.image.load(path)
        self.dog.update(50)
        scaled_image = pg.transform.scale(carImg, (250, 200))
        # self.dog.image =
        sprite = pg.sprite.RenderPlain(self.dog)
        screen.blit(scaled_image, (WORLD_WIDTH / 8 + 50, WORLD_HEIGH / 2))
        sprite.draw(screen)

    def draw(self, screen):
        screen.fill(WHITE)
