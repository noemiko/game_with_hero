import pygame as pg

from duchshund_walking.settings import BLACK
from duchshund_walking.settings import WORLD_HEIGH
from duchshund_walking.settings import WORLD_WIDTH


def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def message_display(display_surface, text, under_text):
    large_text = pg.font.Font("freesansbold.ttf", 85)
    small_text = pg.font.Font("freesansbold.ttf", 25)

    large_text_surface, large_text_rect = text_objects(text, large_text)
    small_text_surface, small_text_rect = text_objects(under_text, small_text)

    large_text_rect.center = ((WORLD_WIDTH / 2), (WORLD_HEIGH / 2))
    small_text_rect.center = ((WORLD_WIDTH / 2), (WORLD_HEIGH / 2 + 60))
    display_surface.blit(large_text_surface, large_text_rect)
    display_surface.blit(small_text_surface, small_text_rect)
