import pygame as pg

from messages import message_display
from app_core import States
from settings import WHITE
from settings import world_width, world_heigh, BLACK, nickname_max_length
import globals

"""
Main loop
"""


class NameInput(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"
        self.COLOR_INACTIVE = pg.Color('lightskyblue1')
        self.COLOR_ACTIVE = pg.Color('black')
        self.FONT = pg.font.Font('freesansbold.ttf', 30)
        self.rect = pg.Rect(world_width / 2 - 250, world_heigh / 2, 50, 50)
        self.color = self.COLOR_INACTIVE
        self.text = ""
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        self.active = True

    def startup(self):
        print("starting Game state stuff")

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if self.text:
                        globals.nickname = self.text
                    self.done = True

                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) != nickname_max_length:
                        self.text += event.unicode
                # Re-render the text.

    def update(self, screen, deltatime):
        self.draw(screen)
        width = max(50, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.txt_surface = self.FONT.render(self.text, True, self.color)

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        text_surface = self.FONT.render("Input your nickname", True, BLACK)
        rect = text_surface.get_rect()
        rect.center = (world_width / 2 - 50, world_heigh / 2 - 50)
        screen.blit(text_surface, rect)
        pg.draw.rect(screen, self.color, self.rect, 2)

    def __str__(self):
        return "NameInput"


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
        print(globals.nickname)
        message_display(screen, "TODO", "todo " + globals.nickname)

    def draw(self, screen):
        screen.fill(WHITE)
