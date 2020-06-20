import os

WORLD_WIDTH = 850
WORLD_HEIGH = 480

FPS = 15  # frame rate

WALK_SPEED = 30  # how fast to move
NICKNAME_MAX_LENGTH = 20

GROUND_POSITION_Y = 370
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
GREEN = (0, 255, 0)
ALPHA = (0, 255, 0)

DEFAULT_GAME_CONFIG = {"duchshund": "duchshund/with_red_bow", "human": "human/default"}

PROJECT_PATH = "./src/duchshund_walk/"
GAME_IMAGES_PATH = os.path.join(PROJECT_PATH, "states/game/images")

COSMOS_GRAVITATION = 5
EARTH_GRAVITATION = 8
MAX_BULLETS = 1
