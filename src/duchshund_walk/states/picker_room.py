import os

import pygame as pg
from duchshund_walk.app_core import States
from duchshund_walk.settings import BLACK
from duchshund_walk.settings import PROJECT_PATH
from duchshund_walk.settings import WHITE
from duchshund_walk.settings import WORLD_HEIGH
from duchshund_walk.settings import WORLD_WIDTH
from duchshund_walk.states.game.player import Duchshund
from duchshund_walk.utils import Point
from duchshund_walk.utils import get_images
from duchshund_walk.utils import scale_images


class Stage:  # State?
    """Class to draw stage with hero."""

    def __init__(self, hero_class, path_with_clothes):
        # dog_images_paths = ["duchshund/with_red_bow", "duchshund/with_bow_tie", "duchshund/standard"]
        self.hero = hero_class
        self.hero.ground_level = WORLD_HEIGH / 2 / 2
        self.next_dog = None
        self.previous_dog = None

    def draw(self, screen):
        self.draw_scene(screen)
        self.draw_hero(screen)

    def draw_scene(self, screen):
        path = os.path.join(PROJECT_PATH, "states/game/images/stage.png")
        stage_image = pg.image.load(path)
        scaled_stage = pg.transform.scale(stage_image, (250, 200))
        screen.blit(scaled_stage, (100, WORLD_HEIGH / 2))
        left_top_point = (350, 350)
        left_down_point = (350, 400)
        middle_right_point = (410, 375)

        right_top_point = (100, 350)
        right_down_point = (100, 400)
        middle_left_point = (40, 375)
        self.next_dog = pg.draw.polygon(screen, BLACK, (left_top_point, left_down_point, middle_right_point))
        self.previous_dog = pg.draw.polygon(screen, BLACK, (right_top_point, right_down_point, middle_left_point))

        # x_coordinate = (0, 50)
        # y_coordinate = (100, 150)
        # (  # a rgb color), (#size of rect in pixels) (screen, color, (x,y,width,height), thickness)
        width = 230
        heigh = 30
        point = Point(110, WORLD_HEIGH - heigh - 10)

        pg.draw.rect(screen, BLACK, (point.x, point.y, width, heigh), 0)

    def get_event(self, event):
        self.dog_files = ["duchshund/with_red_bow", "duchshund/with_bow_tie", "duchshund/standard"]

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if self.next_dog.collidepoint(pos):
                print("next dooog")
                last = self.dog_files.pop(-1)
                self.dog_files.insert(0, last)
                dog_image = get_images(self.dog_files[0])
                images = scale_images(dog_image, (200, 150))
                self.hero.images_frames = images

            elif self.previous_dog.collidepoint(pos):
                print("previous dog")
                first = self.dog_files.pop(0)
                self.dog_files.append(first)
                dog_image = get_images(self.dog_files[0])
                images = scale_images(dog_image, (200, 150))
                self.hero.images_frames = images

    def draw_hero(self, screen):
        self.hero.update(50)
        sprite = pg.sprite.RenderPlain(self.hero)
        sprite.draw(screen)


class HeroesPicker(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"
        self.dog = Duchshund(WORLD_WIDTH / 6, WORLD_HEIGH / 2, "duchshund/with_bow_tie")

        dog_image = get_images("duchshund/with_bow_tie")
        images = scale_images(dog_image, (200, 150))
        self.dog.images_frames = images
        self.dog_files = ["duchshund/with_red_bow", "duchshund/with_bow_tie", "duchshund/standard"]
        self.dog_stage = Stage(self.dog, "ddd")

    def startup(self):
        print("starting HeroesPicker state stuff")

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if self.dog_stage.next_dog.collidepoint(pos):
                print("next dooog")
                last = self.dog_files.pop(-1)
                self.dog_files.insert(0, last)
                dog_image = get_images(self.dog_files[0])
                images = scale_images(dog_image, (200, 150))
                self.dog.images_frames = images

            elif self.dog_stage.previous_dog.collidepoint(pos):
                print("previous dog")
                first = self.dog_files.pop(0)
                self.dog_files.append(first)
                dog_image = get_images(self.dog_files[0])
                images = scale_images(dog_image, (200, 150))
                self.dog.images_frames = images

            # clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]

    def update(self, screen, deltatime):
        self.draw(screen)
        self.dog_stage.draw(screen)

    def draw(self, screen):
        screen.fill(WHITE)
