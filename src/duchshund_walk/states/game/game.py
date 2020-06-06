from datetime import datetime
from datetime import timezone

import pygame as pg
from duchshund_walk import globals
from duchshund_walk.app_core import States
from duchshund_walk.messages import message_display
from duchshund_walk.settings import BLACK
from duchshund_walk.settings import GROUND_POSITION_Y
from duchshund_walk.settings import WORLD_WIDTH
from duchshund_walk.states.game.counter import Counter
from duchshund_walk.states.game.explosion import Explosion
from duchshund_walk.states.game.level import Levels
from duchshund_walk.states.game.player import Duchshund
from duchshund_walk.states.game.player import Human
from duchshund_walk.states.game.scores import ScoreRow
from duchshund_walk.states.game.scores import save_new_scores
from duchshund_walk.utils import get_game_config


"""
Main loop
"""


class Game(States):
    MAX_BULLET = 2
    DESTROYED_SOUND_PATH = "./src/duchshund_walk/static/sounds/destroyed.flac"

    def __init__(self):
        States.__init__(self)
        self.next = "menu"
        self.config = get_game_config()

    def startup(self):
        print("starting Game state stuff")
        pg.mixer.init()
        pg.mixer.music.load("./src/duchshund_walk/static/music/JeffSpeed68_-_Lockdown_Song.wav")
        pg.mixer.music.play(-1)
        self.duchshund = Duchshund(0, GROUND_POSITION_Y)  # spawn player
        self.human = Human(250, 220)
        self.players_list = pg.sprite.Group()
        self.players_list.add([self.duchshund, self.human])
        self.counter = Counter()
        self.levels = Levels()
        self.obstacles = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.duchshund.get_event(event)
            self.human.get_event(event)
            if event.key == ord("q") or event.key == pg.K_ESCAPE:
                self.exit()
            if event.key == pg.K_r:
                self.save_scores()
                self.startup()

    def exit(self):
        self.save_scores()
        pg.mixer.music.stop()
        self.done = True

    def save_scores(self):
        user_points = self.duchshund.health + self.human.health + self.counter.count
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        score_row = ScoreRow(nickname=globals.nickname, points=user_points, date=date)
        save_new_scores(score_row)

    def update(self, screen, deltatime):
        self.levels.update(screen, self.counter.count)
        self.handle_collision()

        if len(self.bullets) <= self.MAX_BULLET:
            self.bullets.add(self.human.bullets)
            self.bullets.add(self.duchshund.bullets)
        if self.duchshund.health < 0 or self.human.health < 0:
            self.show_fail_message(screen)
            return
        elif self.levels.is_game_finished():
            self.show_winning_message(screen)
            return
        if self.levels.is_cosmos_level():
            self.human.cosmos_mode()
            self.duchshund.cosmos_mode()
        else:
            self.human.earth_mode()
            self.duchshund.earth_mode()
        new_obstacle = self.levels.get_obstacles()
        if new_obstacle:
            self.obstacles.add(new_obstacle)
        self.counter.update()
        self.duchshund.update(deltatime)
        self.human.update(deltatime)
        self.all_sprites.update()

        self.obstacles.update()
        self.bullets.update()

        self.draw(screen)

    def draw(self, screen):
        self.players_list.draw(screen)  # refresh player position
        self.obstacles.draw(screen)
        self.draw_points(screen)
        self.bullets.draw(screen)
        self.all_sprites.draw(screen)

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
        self.remove_dog_bullet()
        self.remove_human_bullet()

        for obs in self.obstacles:
            is_collision_dog = pg.sprite.collide_rect_ratio(0.7)(self.duchshund, obs)
            is_collision_human = pg.sprite.collide_rect_ratio(0.7)(self.human, obs)
            if is_collision_dog:
                self.duchshund.health -= 1
                self.duchshund.scream_in_pain()
                print("Dog collision")

            if is_collision_human:
                self.human.health -= 1
                self.human.scream_in_pain()
                print("Human collision")

    def remove_dog_bullet(self):

        for bullet in self.duchshund.bullets:
            hit_list = pg.sprite.spritecollide(bullet, self.obstacles, True, pg.sprite.collide_circle)
            if hit_list:
                expl = Explosion(hit_list[0].rect.center, "lg")
                self.all_sprites.add(expl)

                self.play_explosion_sound()
                self.bullets.remove(bullet)
                self.duchshund.bullets.remove(bullet)
                self.duchshund.health += 10

            if bullet.rect.x > WORLD_WIDTH:
                self.duchshund.bullets.remove(bullet)
                self.bullets.remove(bullet)

    def play_explosion_sound(self):
        pg.mixer.init()
        sound = pg.mixer.Sound(self.DESTROYED_SOUND_PATH)
        sound.play(0)

    def remove_human_bullet(self):
        for bullet in self.human.bullets:

            hit_list = pg.sprite.spritecollide(bullet, self.obstacles, True)

            if hit_list:
                self.play_explosion_sound()
                self.bullets.remove(bullet)
                self.human.bullets.remove(bullet)
                self.human.health += 1

            if bullet.rect.x > WORLD_WIDTH:
                self.human.bullets.remove(bullet)
                self.bullets.remove(bullet)
