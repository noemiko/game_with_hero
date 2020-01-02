import pygame
import sys
import os

from player import Player
from settings import worldx, worldy
from settings import WHITE
from settings import fps

"""
Setup
"""
clock = pygame.time.Clock()
pygame.init()
main = True

world = pygame.display.set_mode([worldx, worldy])
backdrop = pygame.image.load(os.path.join("images", "bg.png"))
backdropbox = world.get_rect()
player = Player(0, 150)  # spawn player

player_list = pygame.sprite.Group()
player_list.add(player)
steps = 30  # how fast to move

"""
Main loop
"""

while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                player.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord("w"):
                print("jump")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                player.control(-steps, 0)
            if event.key == ord("q") or event.key == pygame.K_ESCAPE:
                pygame.quit()
                print("Quit")
                sys.exit()

        world.fill(WHITE)
        world.blit(backdrop, backdropbox)
        player.update()
        player_list.draw(world)  # refresh player position
        pygame.display.flip()
        clock.tick(fps)
