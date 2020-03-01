import pygame
import os
import sys

from player import Player
from background import Background
from enemy import Enemy
from level import Level
from settings import worldx, worldy
from settings import WHITE
from settings import fps
from settings import walk_speed

"""
Main loop
"""


# Force (v) up and mass m.


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
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


            self.draw_world()

    def draw_world(self):
        # self._display_surface.fill(WHITE)
        # self.world.blit(self.background, self.backdropbox)
        # self.player.gravity()  # check gravity

        self._display_surface.blit(self.background.backgroundImg[self.background.random1],(self.background.x,self.background.y))
        self._display_surface.blit(self.background.backgroundImg[self.background.random2],(self.background.x2,self.background.y))

        self.player.update()
        self.enemy.update()
        self.background.update()
        # self.enemy_list.draw(self._display_surface)
        self.player_list.draw(self._display_surface)  # refresh player position
        self.ground_list.draw(self._display_surface)  # refresh ground
        self.plat_list.draw(self._display_surface)  # refresh platforms
        # for e in self.enemy_list:
        #     e.move()
        pygame.display.flip()

        self.clock.tick(fps)


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()
