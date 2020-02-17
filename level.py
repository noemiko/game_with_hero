from enemy import Enemy
import pygame

from platform import Platform
from settings import worldy, worldx

class Level():
    def bad(lvl,eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0],eloc[1]) # spawn enemy
            enemy_list = pygame.sprite.Group() # create enemy group
            enemy_list.add(enemy)              # add enemy to group
        if lvl == 2:
            print("Level " + str(lvl) )

        return enemy_list

    def ground(lvl, gloc, tx, ty):
        ground_list = pygame.sprite.Group()
        i = 0
        if lvl == 1:
            while i < len(gloc):
                ground = Platform(gloc[i], worldy - ty, tx, ty, 'block.png')
                ground_list.add(ground)
                i = i + 1

        if lvl == 2:
            print("Level " + str(lvl))

        return ground_list

    def platform(lvl):
        plat_list = pygame.sprite.Group()
        if lvl == 1:
            pass
            # plat = Platform(200, worldy - 97 - 128, 285, 67, 'block.png')
            # plat_list.add(plat)
            # plat = Platform(500, worldy - 97 - 320, 197, 54, 'block.png')
            # plat_list.add(plat)
        if lvl == 2:
            print("Level " + str(lvl))

        return plat_list