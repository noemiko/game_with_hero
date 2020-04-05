import pygame as pg

from messages import message_display
from app_core import States
from settings import WHITE

"""
Main loop
"""


class WorkInProgress(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"

    def startup(self):
        print("starting Game state stuff")

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, deltatime):
        self.draw(screen)
        message_display(screen, "TODO", "todo")

    def draw(self, screen):
        screen.fill(WHITE)
