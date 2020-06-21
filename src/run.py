import sys

import pygame as pg
from duchshund_walk.app_core import AppStateMachine
from duchshund_walk.globals import init_globals
from duchshund_walk.states.basics import AboutAuthor
from duchshund_walk.states.basics import NameInput
from duchshund_walk.states.basics import WorkInProgress
from duchshund_walk.states.game.game import Game
from duchshund_walk.states.menu.menus import Controls
from duchshund_walk.states.menu.menus import Details
from duchshund_walk.states.menu.menus import MainMenu
from duchshund_walk.states.menu.menus import Scores
from duchshund_walk.states.picker_room import HeroesPicker

if __name__ == "__main__":
    pg.init()
    init_globals()
    APP = AppStateMachine()
    STATE_DICT = {
        "picker_room": HeroesPicker,
        "nickname": NameInput,
        "menu": MainMenu,
        "game": Game,
        "todo": WorkInProgress,
        "details": Details,
        "scores": Scores,
        "about_author": AboutAuthor,
        "controls": Controls,
    }
    APP.setup_states(STATE_DICT, "nickname")
    APP.main_game_loop()
    pg.quit()
    sys.exit()
