from abc import ABC
from abc import abstractmethod

import pygame as pg

from duchshund_walking.settings import FPS
from duchshund_walking.settings import WORLD_HEIGH
from duchshund_walking.settings import WORLD_WIDTH


class States(ABC):
    def __init__(self):
        self.screen = pg.display.set_mode((WORLD_WIDTH, WORLD_HEIGH))
        self.screen_rect = self.screen.get_rect()

        self.done: bool = False
        self.next: str = ""
        self.quit: bool = False
        self.previous: str = ""

    @abstractmethod
    def startup(self):
        pass

    @abstractmethod
    def update(self, screen, deltatime):
        pass

    @abstractmethod
    def get_event(self, event):
        pass


class AppStateMachine:
    def __init__(self):
        self.done = False
        self.fps = FPS
        self.screen = pg.display.set_mode((WORLD_WIDTH, WORLD_HEIGH))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.state_dict: dict = {}
        self.state_name: str = ""
        self.state: States

    def setup_states(self, state_dict, start_state):
        """
        Define all available states in the system.

        :param state_dict: dictionary with name
         of the state and instance of it {str: State}
        :param start_state: name of the first
         used state from state_dict
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        self.state.done = False
        # get next state to setup
        previous, self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self, deltatime):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, deltatime)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)
            self.event_loop()
            self.update(delta_time)
            pg.display.update()
            pg.display.flip()
