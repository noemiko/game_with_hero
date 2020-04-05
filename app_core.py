import pygame as pg

from settings import world_width, world_heigh
from settings import fps


class AppCore:
    def __init__(self):
        self.done = False
        self.fps = fps
        self.screen = pg.display.set_mode((world_width, world_heigh))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()

    def setup_states(self, state_dict, start_state):
        """

        :param state_dict:
        :param start_state:
        :return:
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]  # try except

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
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


class States(AppCore):
    def __init__(self):
        AppCore.__init__(self)
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
