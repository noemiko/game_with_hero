import pygame
import os
import sys

from player import Player
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
        self.world = pygame.display.set_mode([worldx, worldy])
        self.background = pygame.image.load(os.path.join("images", "bg.png"))
        self.backdropbox = self.world.get_rect()
        self.player = Player(0, 350)  # spawn player

        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

        eloc = []
        eloc = [50, 250]
        self.enemy_list = Level.bad(1, eloc)
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

        # enemy = Enemy(320, 200)  # spawn enemy
        # self.enemy_list = pygame.sprite.Group()  # create enemy group
        # self.enemy_list.add(enemy)  # add enemy to group

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord("a"):
                        self.player.control(-walk_speed, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord("d"):
                        self.player.control(walk_speed, 0)
                    if event.key == pygame.K_SPACE or event.key == ord("w"):
                        self.player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord("a"):
                        self.player.control(walk_speed, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord("d"):
                        self.player.control(-walk_speed, 0)
                    if event.key == ord("q") or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        print("Quit")
                        sys.exit()

                self.draw_world()

    def draw_world(self):
        self.world.fill(WHITE)
        self.world.blit(self.background, self.backdropbox)
        # self.player.gravity()  # check gravity
        self.player.update(self.enemy_list)

        self.enemy_list.draw(self.world)
        self.player_list.draw(self.world)  # refresh player position
        self.ground_list.draw(self.world)  # refresh ground
        self.plat_list.draw(self.world)  # refresh platforms
        for e in self.enemy_list:
            e.move()
        pygame.display.flip()
        self.clock.tick(fps)


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()
