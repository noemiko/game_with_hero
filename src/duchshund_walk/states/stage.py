import os

import pygame as pg
from duchshund_walk.settings import BLACK
from duchshund_walk.settings import BLUE
from duchshund_walk.settings import GREEN
from duchshund_walk.settings import PROJECT_PATH
from duchshund_walk.settings import WHITE
from duchshund_walk.settings import WORLD_HEIGH
from duchshund_walk.utils import Point
from duchshund_walk.utils import get_all_hero_clothes
from duchshund_walk.utils import scale_images
from duchshund_walk.utils import set_new_dog_image_folder
from duchshund_walk.utils import set_new_human_image_folder


class Stage:
    """Class to draw stage with hero."""

    HERO_PLACEMENT = Point(120, 50)

    def __init__(self, hero_class, top_left: Point, scale: tuple):
        """
        Draw hero and change his clothes to use selected in game.

        :param hero_class:Player class witch represent here in game
        :param top_left:Point orientation point where is left top corner of stage
        :param scale: (width:int, heigh:int) information how scale image of hero
        """
        self.top_left = top_left
        self.next_hero = None
        self.next_hero_color = BLACK
        self.previous_hero = None
        self.previous_hero_color = BLACK
        self.select_button = None
        self.select_button_color = BLACK

        self.clothes_images = None
        self.images_names = []
        self.hero = hero_class(top_left.x + self.HERO_PLACEMENT.x, self.HERO_PLACEMENT.y)
        self.startup(scale)

    def startup(self, scale):
        self.hero.ground_level = self.top_left.y + 150
        clothes = get_all_hero_clothes(self.hero.__class__)
        scaled_clothes = {}
        for clothes_name in clothes:
            images_list = clothes[clothes_name]
            scaled_images = scale_images(images_list, scale)
            scaled_clothes[clothes_name] = scaled_images
        self.images_names = list(scaled_clothes.keys())
        self.hero.images_frames = scaled_clothes[self.images_names[0]]
        self.clothes_images = scaled_clothes

    def draw(self, screen):
        self.draw_scene(screen)
        self.draw_hero(screen)

    def draw_scene(self, screen):
        self.draw_stage(screen)
        self.draw_arrows(screen)
        self.draw_select_button(screen)
        self.next_hero_color = BLACK
        self.previous_hero_color = BLACK
        if not self.select_button_color == GREEN:
            self.select_button_color = BLACK

        if self.next_hero.collidepoint(pg.mouse.get_pos()):
            self.next_hero_color = BLUE
        elif self.previous_hero.collidepoint(pg.mouse.get_pos()):
            self.previous_hero_color = BLUE
        elif self.select_button.collidepoint(pg.mouse.get_pos()):
            self.select_button_color = BLUE

    def draw_arrows(self, screen):
        # left arrow
        left_top_point = (350 + self.top_left.x, 350 + self.top_left.y)
        left_down_point = (350 + self.top_left.x, 400 + self.top_left.y)
        middle_right_point = (410 + self.top_left.x, 375 + self.top_left.y)
        self.next_hero = pg.draw.polygon(
            screen, self.next_hero_color, (left_top_point, left_down_point, middle_right_point)
        )

        # right arrow
        right_top_point = (100 + self.top_left.x, 350 + self.top_left.y)
        right_down_point = (100 + self.top_left.x, 400 + self.top_left.y)
        middle_left_point = (40 + self.top_left.x, 375 + self.top_left.y)
        self.previous_hero = pg.draw.polygon(
            screen, self.previous_hero_color, (right_top_point, right_down_point, middle_left_point)
        )

    def draw_stage(self, screen):
        path = os.path.join(PROJECT_PATH, "states/game/images/stage.png")
        stage_image = pg.image.load(path)
        stage_size = (250, 200)
        scaled_stage = pg.transform.scale(stage_image, stage_size)
        screen.blit(scaled_stage, (100 + self.top_left.x, WORLD_HEIGH / 2 + self.top_left.y))

    def draw_select_button(self, screen):
        width = 230
        heigh = 30
        button_bottom_margin = 50
        start_button_x = 110
        point = Point(start_button_x + self.top_left.x, WORLD_HEIGH - button_bottom_margin)
        self.select_button = pg.draw.rect(screen, self.select_button_color, (point.x, point.y, width, heigh), 0)
        font = pg.font.SysFont("Arial", 25)
        current_hero_clothes = self.images_names[0]
        screen.blit(font.render(current_hero_clothes, False, WHITE), (point.x + 50, point.y))

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if self.next_hero.collidepoint(pos):
                print("next clothes")
                self.select_button_color = BLACK
                last = self.images_names.pop(-1)
                self.images_names.insert(0, last)
                current_frames = self.clothes_images[self.images_names[0]]
                self.hero.images_frames = current_frames

            elif self.previous_hero.collidepoint(pos):
                print("previous clothes")
                self.select_button_color = BLACK
                first = self.images_names.pop(0)
                self.images_names.append(first)
                current_frames = self.clothes_images[self.images_names[0]]
                self.hero.images_frames = current_frames

            elif self.select_button.collidepoint(pos):
                is_saved = self.set_new_clothes(self.images_names[0])
                if is_saved:
                    print("saved")
                    self.select_button_color = GREEN

    def set_new_clothes(self, folder_name):
        pass

    def draw_hero(self, screen):
        self.hero.update(50)
        sprite = pg.sprite.RenderPlain(self.hero)
        sprite.draw(screen)


class DuchshundStage(Stage):
    def set_new_clothes(self, folder_name):
        return set_new_dog_image_folder(folder_name)


class HumanStage(Stage):
    def set_new_clothes(self, folder_name):
        return set_new_human_image_folder(folder_name)
