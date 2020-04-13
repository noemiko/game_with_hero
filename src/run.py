import sys

import pygame as pg

from duchshund_walking.app_core import AppStateMachine
from duchshund_walking.globals import init_globals
from duchshund_walking.states.basics import NameInput
from duchshund_walking.states.basics import WorkInProgress
from duchshund_walking.states.game.game import Game
from duchshund_walking.states.menu.menus import MainMenu
from duchshund_walking.states.menu.menus import Options
from duchshund_walking.states.menu.menus import Scores

if __name__ == "__main__":
    pg.init()
    init_globals()
    APP = AppStateMachine()
    STATE_DICT = {
        "nickname": NameInput(),
        "menu": MainMenu(),
        "game": Game(),
        "todo": WorkInProgress(),
        "options": Options(),
        "scores": Scores(),
    }
    APP.setup_states(STATE_DICT, "nickname")
    APP.main_game_loop()
    pg.quit()
    sys.exit()
