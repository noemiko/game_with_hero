import pygame as pg
from duchshund_walk import globals
from duchshund_walk.app_core import States
from duchshund_walk.messages import message_display
from duchshund_walk.settings import NICKNAME_MAX_LENGTH
from duchshund_walk.settings import WHITE
from duchshund_walk.settings import WORLD_HEIGH
from duchshund_walk.settings import WORLD_WIDTH


"""
Main loop
"""


class NameInput(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"
        self.color = pg.Color("black")
        self.FONT = pg.font.Font("freesansbold.ttf", 30)
        self.rect = pg.Rect(WORLD_WIDTH / 2 - 250, WORLD_HEIGH / 2, 50, 50)
        self.text = ""
        self.txt_surface = self.FONT.render(self.text, True, self.color)

    def startup(self):
        print("starting Game state stuff")

    def handle_enter_event(self):
        if not self.text:
            self.color = pg.Color("red")
            return
        globals.nickname = self.text
        self.done = True

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.handle_enter_event()
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) != NICKNAME_MAX_LENGTH:
                    self.text += event.unicode

    def update(self, screen):
        self.draw(screen)
        char_size = 10
        box_width = max(50, self.txt_surface.get_width() + char_size)
        self.rect.w = box_width
        self.txt_surface = self.FONT.render(self.text, True, self.color)

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        text_surface = self.FONT.render("Input your nickname", True, self.color)
        rect = text_surface.get_rect()
        rect.center = (WORLD_WIDTH / 2 - 50, WORLD_HEIGH / 2 - 50)
        screen.blit(text_surface, rect)
        pg.draw.rect(screen, self.color, self.rect, 2)

    def __str__(self):
        return "NameInput"


class WorkInProgress(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"

    def startup(self):
        print("starting WIP state stuff")

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen):
        self.draw(screen)
        message_display(screen, "TODO", "todo " + globals.nickname)

    def draw(self, screen):
        screen.fill(WHITE)
