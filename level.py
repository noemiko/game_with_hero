from random import randint
from typing import NamedTuple

from background import Background
from obstacles import Cactus, Obstacle, Flower, Windmill, Stone


class LevelDetails(NamedTuple):
    obstacle: Obstacle
    background_index: int


class Levels():
    WORLDS = [
        LevelDetails(obstacle=Cactus, background_index=0),
        LevelDetails(obstacle=Flower, background_index=1),
        LevelDetails(obstacle=Stone, background_index=2),
        LevelDetails(obstacle=Windmill, background_index=3),
        LevelDetails(obstacle=Windmill, background_index=4)
    ]

    def __init__(self):
        self.background = Background()
        self.respawn = 5
        self.current_world = self.WORLDS[0]

    def update(self, display_surface, game_duration: int):

        display_surface.blit(self.background.current,
                             (self.background.x, self.background.y))
        display_surface.blit(self.background.current,
                             (self.background.next_x, self.background.y))

        self.background.update()
        if game_duration == 15:
            self.current_world = self.WORLDS[1]
        elif game_duration == 30:
            self.current_world = self.WORLDS[2]
        elif game_duration == 40:
            self.current_world = self.WORLDS[3]
        elif game_duration == 50:
            self.current_world = self.WORLDS[4]
        self.background.change_image(self.current_world.background_index)

    def get_obstacles(self):
        self.respawn -= 1
        if self.respawn == 0:
            self.respawn = randint(60, 70)
            return self.current_world.obstacle()
        return []

    def is_all_passed(self):
        return self.current_world == self.WORLDS[-1]
