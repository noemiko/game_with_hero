from typing import List

import pygame as pg
from duchshund_walk.app_core import States
from duchshund_walk.settings import BLACK
from duchshund_walk.settings import BLUE
from duchshund_walk.settings import WHITE
from duchshund_walk.settings import WORLD_WIDTH
from duchshund_walk.states.game.scores import ScoreRow
from duchshund_walk.states.game.scores import get_scores_results
from duchshund_walk.states.menu.core import MenuCore
from duchshund_walk.utils import Point


class MainMenu(States, MenuCore):
    def __init__(self):
        States.__init__(self)
        MenuCore.__init__(self)
        self.next = "game"
        self.options = [
            "Play",
            "Choose heroes",
            "Details",
            "Quit",
        ]
        self.states_names_options = [
            "game",
            "picker_room",
            "details",
        ]  # last option is by default quit
        self.pre_render_options()
        self.from_bottom = 100
        self.spacer = 75

    def cleanup(self):
        print("cleaning up Main Menu state stuff")

    def startup(self):
        print("starting Main Menu state stuff")

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)

    def update(self, screen):
        self.update_menu()
        self.draw(screen)


class Details(States, MenuCore):
    def __init__(self):
        States.__init__(self)
        MenuCore.__init__(self)
        self.next = "menu"
        self.options = ["The best scores", "About author", "Controls", "Main Menu"]
        self.states_names_options = ["scores", "about_author", "controls", "menu"]
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

    def update(self, screen):
        self.update_menu()
        self.draw(screen)


class Scores(States):
    def __init__(self):
        States.__init__(self)
        self.next = "details"
        self.FONT = pg.font.Font("freesansbold.ttf", 30)
        self.board_of_scores: List[Scores] = []

    def startup(self):
        headers = ScoreRow(nickname="NAME", points="POINTS", date="DATE")
        self.board_of_scores = [headers] + get_scores_results()
        print("starting Game state stuff")

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def create_scores_table_field(self, text, coordinates: Point, screen):
        surface = self.FONT.render(text, True, BLACK)
        rect = surface.get_rect()
        rect.topleft = (coordinates.x, coordinates.y)
        screen.blit(surface, rect)

    def update(self, screen):
        self.draw(screen)
        left_margin = 10
        x_first_column = 10
        x_second_column = 410
        x_third_column = 550
        for index, row in enumerate(self.board_of_scores):
            y_row = left_margin + index * 100
            self.create_scores_table_field(row.nickname, Point(x_first_column, y_row), screen)
            self.create_scores_table_field(row.points, Point(x_second_column, y_row), screen)
            self.create_scores_table_field(row.date, Point(x_third_column, y_row), screen)

    def draw(self, screen):
        screen.fill(WHITE)
        pg.draw.line(screen, BLUE, (0, 80), (WORLD_WIDTH, 80), 5)


class Controls(States):
    def __init__(self):
        States.__init__(self)
        self.FONT = pg.font.Font("freesansbold.ttf", 30)
        self.next = "details"
        self.controls_board = [
            {"description": "Human"},
            {"button": "w", "description": "jump"},
            {"button": "enter", "description": "shoot"},
            {"description": "Dog"},
            {"button": "space", "description": "jump"},
            {"button": "shift", "description": "shoot"},
            {"description": "Other"},
            {"button": "q", "description": "escape from view"},
            {"button": "r", "description": "repeat game"},
        ]

    def startup(self):
        print("state with controls")

    def create_scores_table_field(self, text, coordinates: Point, screen):
        surface = self.FONT.render(text, True, BLACK)
        rect = surface.get_rect()
        rect.topleft = (coordinates.x, coordinates.y)
        screen.blit(surface, rect)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen):
        self.draw(screen)
        left_margin = 10
        x_first_column = 100
        x_second_column = 410
        space_between_rows = 50
        for index, row in enumerate(self.controls_board):
            y_row = left_margin + index * space_between_rows
            self.create_scores_table_field(row["description"], Point(x_first_column, y_row), screen)
            if "button" in row:
                self.create_scores_table_field(row["button"], Point(x_second_column, y_row), screen)
            else:
                point = Point(x_second_column, y_row)
                pg.draw.line(screen, BLUE, (0, y_row), (WORLD_WIDTH, point.y), 5)
                pg.draw.line(
                    screen, BLUE, (0, y_row + space_between_rows), (WORLD_WIDTH, point.y + space_between_rows), 5
                )

    def draw(self, screen):
        screen.fill(WHITE)
