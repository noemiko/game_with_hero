import pygame as pg
from duchshund_walk.app_core import States
from duchshund_walk.settings import WHITE
from duchshund_walk.settings import WORLD_WIDTH
from duchshund_walk.states.game.players.dogs import Duchshund
from duchshund_walk.states.game.players.humans import Human
from duchshund_walk.states.stage import DuchshundStage
from duchshund_walk.states.stage import HumanStage
from duchshund_walk.utils import Point


class HeroesPicker(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"
        self.dog_stage = DuchshundStage(Duchshund, Point(0, 0), (200, 150))
        self.human_stage = HumanStage(Human, Point(WORLD_WIDTH / 2, 0), (200, 250))

    def startup(self):
        print("starting HeroesPicker state stuff")

    def get_event(self, event):
        self.dog_stage.get_event(event)
        self.human_stage.get_event(event)
        if event.type == pg.KEYDOWN:
            self.done = True

    def update(self, screen, deltatime):
        self.draw(screen)
        self.dog_stage.draw(screen)
        self.human_stage.draw(screen)

    def draw(self, screen):
        screen.fill(WHITE)
