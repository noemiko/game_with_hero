import pygame as pg
import sys
from app_core import AppStateMachine
from states.menus import MainMenu, Options
from states.game.game import Game
from states.basics import WorkInProgress

if __name__ == "__main__":
    pg.init()
    app = AppStateMachine()
    state_dict = {
        "menu": MainMenu(),
        "game": Game(),
        "todo": WorkInProgress(),
        "options": Options()
    }
    app.setup_states(state_dict, "menu")
    app.main_game_loop()
    pg.quit()
    sys.exit()
