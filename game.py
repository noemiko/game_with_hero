import pygame
import os
import sys

from player import Player
from settings import worldx, worldy
from settings import WHITE
from settings import fps
from settings import walk_speed

"""
Main loop
"""


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()

    def setup(self):
        self.world = pygame.display.set_mode([worldx, worldy])
        self.background = pygame.image.load(os.path.join("images", "bg.png"))
        self.backdropbox = self.world.get_rect()
        self.player = Player(0, 150)  # spawn player

        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord("a"):
                        self.player.control(-walk_speed, -1)
                    if event.key == pygame.K_RIGHT or event.key == ord("d"):
                        self.player.control(walk_speed, -1)
                    if event.key == pygame.K_UP or event.key == ord("w"):
                        print("jump")

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord("a"):
                        self.player.control(walk_speed, -1)
                    if event.key == pygame.K_RIGHT or event.key == ord("d"):
                        self.player.control(-walk_speed, -1)
                    if event.key == ord("q") or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        print("Quit")
                        sys.exit()
                self.draw_world()

    def handle_controlls(self):

    def draw_world(self):
        self.world.fill(WHITE)
        self.world.blit(self.background, self.backdropbox)
        self.player.update()
        self.player_list.draw(self.world)  # refresh player position
        pygame.display.flip()
        self.clock.tick(fps)


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()
