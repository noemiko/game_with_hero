import pygame
import os
import sys
from random import randint

from player import Duchshund, Human
from background import Background
# from enemy import Enemy
from level import Level
from obstacles import Cactus
from settings import worldx, worldy
from settings import WHITE
from settings import fps
from settings import walk_speed
from settings import ground_position_y
from counter import Counter
from settings import ground_position_y

"""
Main loop
"""


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self._display_surface = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Run")
        pygame.init()

    def setup(self):
        self._display_surface = pygame.display.set_mode([worldx, worldy])
        self.background = Background()
        self.backdropbox = self._display_surface.get_rect()
        self.duchshund = Duchshund(0, ground_position_y)  # spawn player
        self.human = Human(250, 250)
        self.players_list = pygame.sprite.Group()
        self.players_list.add(self.duchshund)
        self.players_list.add(self.human)

        self.counter = Counter()
        self.cactuses = pygame.sprite.Group()
        self.respawn = 5

        eloc = []
        eloc = [50, 250]
        # self.enemy_list = Level.bad(1, eloc)
        self.v = 5
        self.m = 1
        gloc = []
        tx = 64
        ty = 64

        i = 0
        while i <= (worldx / tx) + tx:
            gloc.append(i * tx)
            i = i + 1

        self.ground_list = Level.ground(1, gloc, tx, ty)
        self.platform_list = Level.platform(1)

    def run(self):
        deltatime = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.duchshund.jump()
                    if event.key == event.key == ord("w"):
                        self.human.jump()
                if event.type == pygame.KEYUP:
                    if event.key == ord("q") or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        print("Quit")
                        sys.exit()
            # compute how many milliseconds have passed since the previous call.
            deltatime = self.clock.tick(fps)
            self.draw_world(deltatime)

    def draw_world(self, deltatime):
        self._display_surface.blit(self.background.backgroundImg[self.background.random1],
                                   (self.background.x, self.background.y))
        self._display_surface.blit(self.background.backgroundImg[self.background.random2],
                                   (self.background.x2, self.background.y))
        self._display_surface.blit(self.counter.counterText, (730, 10))
        self.counter.update()

        self.duchshund.update(deltatime)
        self.human.update(deltatime)
        self.background.update()

        self.players_list.draw(self._display_surface)  # refresh player position
        self.ground_list.draw(self._display_surface)  # refresh ground
        # self.platform_list.draw(self._display_surface)  # refresh platforms

        self.respawn -= 1
        if self.respawn == 0:
            self.cactuses.add(Cactus())
            self.respawn = randint(60, 70)

        for cactus in self.cactuses:
            is_collision_dog = pygame.sprite.collide_rect_ratio(0.7)(self.duchshund, cactus)
            is_collision_human = pygame.sprite.collide_rect_ratio(0.7)(self.human, cactus)
            if (is_collision_dog):
                self.counter -= 100
                print("Dog collision")

            if (is_collision_human):
                self.counter -= 100
                print("Human collision")

        self.cactuses.update()
        self.cactuses.draw(self._display_surface)
        pygame.display.update()
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()
