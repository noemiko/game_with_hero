import pygame as pg
import sys
from app_core import AppCore
from states.menus import Menu, Options
from states.game.game import Game
from states.basics import WorkInProgress


if __name__ == "__main__":
    pg.init()
    app = AppCore()
    state_dict ={
        "menu": Menu(),
        "game": Game(),
        "todo": WorkInProgress(),
        "options": Options()
    }
    app.setup_states(state_dict, "menu")
    app.main_game_loop()
    pg.quit()
    sys.exit()
