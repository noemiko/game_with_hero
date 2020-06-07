from os import path

import pygame
from duchshund_walk.settings import GAME_IMAGES_PATH


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.explosion_anim = self.load_images()
        self.size = size
        self.image = self.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def load_images(self):
        explosion_anim = {}
        explosion_anim["lg"] = []
        explosion_anim["sm"] = []
        for i in range(9):
            filename = f"regularExplosion0{i}.png"
            explosion_path = path.join(GAME_IMAGES_PATH, "explosion")
            img = pygame.image.load(path.join(explosion_path, filename)).convert_alpha()
            img_lg = pygame.transform.scale(img, (75, 75))
            explosion_anim["lg"].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            explosion_anim["sm"].append(img_sm)
        return explosion_anim

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
