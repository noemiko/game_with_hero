from random import randint
from typing import List
from typing import NamedTuple

from duchshund_walk.states.game.background import Background
from duchshund_walk.states.game.obstacles import Cactus
from duchshund_walk.states.game.obstacles import Flower
from duchshund_walk.states.game.obstacles import Flying
from duchshund_walk.states.game.obstacles import Obstacle
from duchshund_walk.states.game.obstacles import Stone
from duchshund_walk.states.game.obstacles import Windmill


class LevelDetails(NamedTuple):
    obstacles: List[Obstacle]
    background_index: int
    respawn_max_tempo: int


class Levels:
    WORLDS = [
        LevelDetails(obstacles=[Cactus], background_index=1, respawn_max_tempo=70),
        LevelDetails(obstacles=[Flower], background_index=1, respawn_max_tempo=70),
        LevelDetails(obstacles=[Stone], background_index=2, respawn_max_tempo=70),
        LevelDetails(obstacles=[Windmill], background_index=3, respawn_max_tempo=70),
        LevelDetails(obstacles=[Flying, Cactus], background_index=1, respawn_max_tempo=70),
        LevelDetails(obstacles=[Flying, Flower], background_index=2, respawn_max_tempo=60),
        LevelDetails(obstacles=[Flying, Stone], background_index=3, respawn_max_tempo=50),
        LevelDetails(obstacles=[Flying, Windmill], background_index=2, respawn_max_tempo=20),
        LevelDetails(obstacles=[Flying, Cactus], background_index=3, respawn_max_tempo=10),
        LevelDetails(obstacles=[Flying, Windmill], background_index=1, respawn_max_tempo=10),
        LevelDetails(obstacles=[Flying, Stone], background_index=0, respawn_max_tempo=40),
        LevelDetails(obstacles=[], background_index=4, respawn_max_tempo=10000),  # win background
    ]

    def __init__(self):
        self.background = Background()
        self.respawn = 5
        self.current_world = self.WORLDS[0]

    def update(self, display_surface, game_time: int):
        display_surface.blit(self.background.current, (self.background.x, self.background.y))
        display_surface.blit(self.background.current, (self.background.next_x, self.background.y))
        self.background.update()

        for index, world in enumerate(self.WORLDS):
            waiting = index * 45
            if game_time == waiting:
                self.current_world = world
        self.background.change_image(self.current_world.background_index)

    def get_obstacles(self):
        self.respawn -= 1
        if self.respawn == 0:
            self.respawn = randint(10, self.current_world.respawn_max_tempo)
            number_of_possible_obs = len(self.current_world.obstacles)
            if number_of_possible_obs:
                rand_obstacle_index = randint(0, number_of_possible_obs - 1)
                return self.current_world.obstacles[rand_obstacle_index]()
        return []

    def is_cosmos_level(self):
        if self.current_world.background_index == 0:
            return True
        return False

    def is_game_finished(self):
        return self.current_world == self.WORLDS[-1]
