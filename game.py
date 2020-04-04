import pygame
import sys
import time
from player import Duchshund, Human
from level import Levels
from messages import message_display
from settings import worldx, worldy
from settings import fps
from settings import BLACK
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
        self.is_running = True

    def setup(self):
        print("Set up")

        self._display_surface = pygame.display.set_mode([worldx, worldy])

        self.backdropbox = self._display_surface.get_rect()
        self.duchshund = Duchshund(0, ground_position_y)  # spawn player
        self.human = Human(250, 250)
        self.players_list = pygame.sprite.Group()
        self.players_list.add([self.duchshund, self.human])

        self.counter = Counter()

        self.levels = Levels()
        self.obstacles = pygame.sprite.Group()

        message_display(self._display_surface, 'Loading new game', "click r button to try again")
        time.sleep(1)

    def crash(self):
        message_display(self._display_surface, 'You Lost!', "click r button to try again")

    def show_winning_message(self):
        message_display(self._display_surface, 'You Win!', "click r button to try again")

    def run(self):
        deltatime = 0
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.duchshund.jump()
                    if event.key == ord("w"):
                        self.human.jump()

                if event.type == pygame.KEYUP:
                    if event.key == ord("q") or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        print("Quit")
                        sys.exit()

                    if event.key == pygame.K_r:
                        self.setup()

            # compute how many milliseconds have passed since the previous call.
            deltatime = self.clock.tick(fps)
            self.draw_world(deltatime)

    def draw_points(self):

        self._display_surface.blit(self.counter.counterText, (730, 10))
        font = pygame.font.Font("freesansbold.ttf", 22)

        dog_health = font.render(f"duchshund health {self.duchshund.health}", True, BLACK)
        human_health = font.render(f"human health {self.human.health}", True, BLACK)

        self._display_surface.blit(dog_health, (10, 10))
        self._display_surface.blit(human_health, (250, 10))

    def draw_world(self, deltatime):
        self.levels.update(self._display_surface, self.counter.count)

        if self.duchshund.health < 0 or self.human.health < 0:
            self.crash()
            return
        elif self.levels.is_all_passed():
            self.show_winning_message()
            return
        self.draw_points()
        self.counter.update()

        self.duchshund.update(deltatime)
        self.human.update(deltatime)

        self.players_list.draw(self._display_surface)  # refresh player position

        new_obstacles = self.levels.get_obstacles()
        if new_obstacles:
            self.obstacles.add(new_obstacles)

        for obs in self.obstacles:
            is_collision_dog = pygame.sprite.collide_rect_ratio(0.7)(self.duchshund, obs)
            is_collision_human = pygame.sprite.collide_rect_ratio(0.7)(self.human, obs)
            if is_collision_dog:
                self.duchshund.health -= 1
                print("Dog collision")

            if is_collision_human:
                self.human.health -= 1
                print("Human collision")

        if self.obstacles:
            self.obstacles.update()
            self.obstacles.draw(self._display_surface)
        pygame.display.update()
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.setup()
    game.run()
