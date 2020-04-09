import pygame as pg

from states.game.player import Duchshund, Human
from states.game.level import Levels
from messages import message_display

from settings import BLACK
from states.game.counter import Counter
from settings import ground_position_y
from app_core import States

"""
Main loop
"""


class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"

    def startup(self):
        print("starting Game state stuff")
        self.duchshund = Duchshund(0, ground_position_y)  # spawn player
        self.human = Human(250, 250)
        self.players_list = pg.sprite.Group()
        self.players_list.add([self.duchshund, self.human])

        self.counter = Counter()

        self.levels = Levels()
        self.obstacles = pg.sprite.Group()

    def get_event(self, event):
        self.duchshund.get_event(event)
        self.human.get_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == ord("q") or event.key == pg.K_ESCAPE:
                self.done = True

            if event.key == pg.K_r:
                self.startup()

    def update(self, screen, deltatime):
        self.levels.update(screen, self.counter.count)
        self.handle_collision()
        if self.duchshund.health < 90 or self.human.health < 0:
            self.show_fail_message(screen)
            return
        elif self.levels.is_all_passed():
            self.show_winning_message(screen)
            return
        new_obstacles = self.levels.get_obstacles()
        if new_obstacles:
            self.obstacles.add(new_obstacles)
        self.counter.update()
        self.duchshund.update(deltatime)
        self.human.update(deltatime)
        self.obstacles.update()
        self.draw(screen)

    def draw(self, screen):
        self.players_list.draw(screen)  # refresh player position
        self.obstacles.draw(screen)
        self.draw_points(screen)

    def show_fail_message(self, screen):
        message_display(screen, "You Lost!", "click r button to try again")

    def show_winning_message(self, screen):
        message_display(screen, "You Win!", "click r button to try again")

    def draw_points(self, screen):

        screen.blit(self.counter.counterText, (730, 10))
        font = pg.font.Font("freesansbold.ttf", 22)

        dog_health = font.render(f"duchshund health {self.duchshund.health}", True, BLACK)
        human_health = font.render(f"human health {self.human.health}", True, BLACK)

        screen.blit(dog_health, (10, 10))
        screen.blit(human_health, (250, 10))

    def handle_collision(self):
        for obs in self.obstacles:
            is_collision_dog = pg.sprite.collide_rect_ratio(0.7)(self.duchshund, obs)
            is_collision_human = pg.sprite.collide_rect_ratio(0.7)(self.human, obs)
            if is_collision_dog:
                self.duchshund.health -= 1
                print("Dog collision")

            if is_collision_human:
                self.human.health -= 1
                print("Human collision")
