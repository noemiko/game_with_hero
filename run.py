import pygame as pg
import sys
from app_core import AppStateMachine
from states.menus import MainMenu, Options
from states.game.game import Game
from states.basics import WorkInProgress, NameInput
from globals import init as init_globals

if __name__ == "__main__":
    pg.init()
    init_globals()
    app = AppStateMachine()
    state_dict = {
        "nickname": NameInput(),
        "menu": MainMenu(),
        "game": Game(),
        "todo": WorkInProgress(),
        "options": Options()
    }
    app.setup_states(state_dict, "nickname")
    app.main_game_loop()
    pg.quit()
    sys.exit()
