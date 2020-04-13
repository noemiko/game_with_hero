import pygame

from duchshund_walking.settings import BLACK


class Counter:
    def __init__(self):
        pygame.font.init()
        self.myfont = pygame.font.SysFont("monospace", 20)
        self.count = 0
        text = str(self.count).zfill(5)
        self.counterText = self.myfont.render(text, 1, BLACK)
        self.check = 0

    def update(self):
        self.check += 1
        if self.check == 6:
            self.count += 1
            self.check = 0
        text = str(self.count).zfill(5)
        self.counterText = self.myfont.render(text, 1, BLACK)
