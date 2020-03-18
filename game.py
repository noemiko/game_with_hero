import pygame
import os
import sys
from random import randint

from player import Player
from background import Background
from enemy import Enemy
from level import Level
from obstacles import Cactus
from settings import worldx, worldy
from settings import WHITE
from settings import fps
from settings import walk_speed
from settings import ground_position_y
from counter import Counter
"""
Main loop
"""


class Game:
    def __init__(self):
        self.flpsClock = pygame.time.Clock()
        self._display_surface = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Run")
        pygame.init()

    def setup(self):
        self._display_surface = pygame.display.set_mode([worldx, worldy])
        self.background = Background()
        self.backdropbox = self._display_surface.get_rect()
        self.player = Player(0, 350)  # spawn player
        self.enemy = Enemy(150, 250)
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        self.player_list.add(self.enemy)
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
        self.plat_list = Level.platform(1)


    def run(self):
        deltatime = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_LEFT or event.key == ord("a"):
                    #     self.player.control(-walk_speed, 0)
                    # if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    #     self.player.control(walk_speed, 0)
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == event.key == ord("w"):
                        self.enemy.jump()
                if event.type == pygame.KEYUP:
                    # if event.key == pygame.K_LEFT or event.key == ord("a"):
                    #     self.player.control(walk_speed, 0)
                    # if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    #     self.player.control(-walk_speed, 0)
                    if event.key == ord("q") or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        print("Quit")
                        sys.exit()

            deltatime = self.flpsClock.tick(fps) / 300.0
            self.draw_world(deltatime)

    def draw_world(self, deltatime):
        self._display_surface.blit(self.background.backgroundImg[self.background.random1],(self.background.x,self.background.y))
        self._display_surface.blit(self.background.backgroundImg[self.background.random2],(self.background.x2,self.background.y))
        self._display_surface.blit(self.counter.counterText, (730, 10))
        self.counter.update()

        self.player.update(deltatime)
        self.enemy.update()
        self.background.update()
        # self.enemy_list.draw(self._display_surface)
        self.player_list.draw(self._display_surface)  # refresh player position
        self.ground_list.draw(self._display_surface)  # refresh ground
        self.plat_list.draw(self._display_surface)  # refresh platforms
        # for e in self.enemy_list:
        #     e.move()


        self.respawn -= 1
        if self.respawn == 0:
            self.cactuses.add(Cactus())
            self.respawn = randint(60, 70)

        for cactus in self.cactuses:
            is_collided = pygame.sprite.collide_rect_ratio(0.7)(self.player, cactus)
            if (is_collided):
                print("KOLIZJA!!!")
                # self._running = False

        self.cactuses.update()
        self.cactuses.draw(self._display_surface)
        pygame.display.update()
        pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()
