import pygame as pg

from settings import BLACK, WHITE, BLUE, world_width
from utils import open_file
from app_core import States
from states.menu.core import MenuCore


class MainMenu(States, MenuCore):
    def __init__(self):
        States.__init__(self)
        MenuCore.__init__(self)
        self.next = "game"
        self.options = [
            "Play", "The best scores", "Choose heroes", "Options", "About author", "Quit"
        ]
        self.states_names_options = ["game", "scores", "todo", "options", "todo"]  # last option is by default quit
        self.pre_render_options()
        self.from_bottom = 50
        self.spacer = 75

    def cleanup(self):
        print("cleaning up Main Menu state stuff")

    def startup(self):
        print("starting Main Menu state stuff")

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)

    def update(self, screen, deltatime):
        self.update_menu()
        self.draw(screen)


class Options(States, MenuCore):
    def __init__(self):
        States.__init__(self)
        MenuCore.__init__(self)
        self.next = "menu"
        self.options = ["Music", "Sound", "Graphics", "Controls", "Main Menu"]
        self.states_names_options = ["options", "options", "options", "options", "menu"]
        self.from_bottom = 100
        self.spacer = 75
        self.pre_render_options()

    def cleanup(self):
        print("cleaning up Options state stuff")

    def startup(self):
        print("starting Options state stuff")

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)

    def update(self, screen, deltatime):
        self.update_menu()
        self.draw(screen)


class Scores(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"
        self.FONT = pg.font.Font('freesansbold.ttf', 30)
        self.users_scores = open_file("scores.csv")

    def startup(self):
        print("starting Game state stuff")

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def create_scores_table_field(self, text, coordinates):
        x, y = coordinates
        date_surface = self.FONT.render(text, True, BLACK)
        rect = date_surface.get_rect()
        rect.topleft = (x, y)
        return date_surface, rect

    def update(self, screen, deltatime):
        self.draw(screen)
        pg.draw.line(screen, BLUE, (0, 80), (world_width, 80), 5)
        headers = ["NAME", "POINTS", "DATE"]
        scores_table = [headers] + self.users_scores
        left_margin = 10
        for index, row in enumerate(scores_table):
            scores_surface, scores_rect = self.create_scores_table_field(
                row[0], (10, left_margin + (index * 100)))
            screen.blit(scores_surface, scores_rect)

            date_surface, date_rect = self.create_scores_table_field(
                row[1], (410, left_margin + (index * 100)))
            screen.blit(date_surface, date_rect)

            nickname_surface, nickname_rect = self.create_scores_table_field(
                row[2], (550, left_margin + (index * 100)))
            screen.blit(nickname_surface, nickname_rect)

    def draw(self, screen):
        screen.fill(WHITE)
