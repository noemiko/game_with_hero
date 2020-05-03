import csv
import glob
import json
import os
from enum import Enum
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple

from duchshund_walk.settings import DEFAULT_GAME_CONFIG
from duchshund_walk.settings import GAME_IMAGES_PATH
from duchshund_walk.settings import PROJECT_PATH
from pygame import Surface
from pygame import image
from pygame import transform


class InvalidGameConfig(Exception):
    pass


class HeroType(Enum):
    duchshund = "duchshund"
    human = "human"


class Point(NamedTuple):
    x: int
    y: int


def get_all_hero_clothes(hero) -> Dict:
    """
    :param hero: class
    :return: name of images with list of surface to make animation {name:str:List[Surface]}
    """
    from duchshund_walk.states.game.player import Duchshund

    if hero == Duchshund:
        folder_name = HeroType.duchshund.value
    else:
        folder_name = HeroType.human.value
    hero_clothes_path = os.path.join(GAME_IMAGES_PATH, folder_name)
    os.walk(hero_clothes_path)
    hero_clothes = {}
    for subdir, dirs, files in os.walk(hero_clothes_path):
        if not files:
            continue
        folder = subdir.split("/")[-1]
        hero_clothes[folder] = []
        files = sorted(files)
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                image_path = os.path.join(subdir, file)
                surface = image.load(image_path)
                hero_clothes[folder].append(surface)
    return hero_clothes


def get_images(folder: str) -> List[Surface]:
    """
    Load images from folder .

    :param folder: folder name where is images

    :return: List of surfaces
    """
    images = []
    image_path = os.path.join(GAME_IMAGES_PATH, folder)
    all_images = glob.glob(f"{image_path}/*")
    sorted_images = sorted(all_images)
    for image_ in sorted_images:
        surface = image.load(image_)
        images.append(surface)
    return images


def scale_images(images: List[Surface], scala: Tuple) -> List[Surface]:
    """
    Scale images to expected size
    :param images:
    :param scala:(width, height) information to which size scale all images
    :return:
    """
    scaled_images = []
    for image_ in images:
        scaled_image = transform.scale(image_, scala)
        scaled_images.append(scaled_image)
    return scaled_images


def open_file(file_name: str):
    path = os.path.join(PROJECT_PATH, file_name)
    try:
        with open(path, "r") as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []


def validate_config(config: Dict):
    required_keys = ["duchshund", "human"]
    missing_keys = []
    for key in required_keys:
        if key not in config.keys():
            missing_keys.append(key)
    if missing_keys:
        raise InvalidGameConfig(f"Missing keys {missing_keys}")


def get_game_config():
    try:
        config = open_json_file("config.json")
    except FileNotFoundError:
        return DEFAULT_GAME_CONFIG
    try:
        validate_config(config)
    except InvalidGameConfig as error:
        print(error)
        return DEFAULT_GAME_CONFIG
    return config


def set_new_dog_image_folder(folder_name):
    print(f"Overriding dog image folder to {folder_name}")
    return override_game_config({"duchshund": f"duchshund/{folder_name}"})


def get_human_image_folder():
    try:
        config = open_json_file("config.json")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Missing config file: {e}")
    return config["human"]


def get_dog_image_folder():
    try:
        config = open_json_file("config.json")
    except FileNotFoundError:
        config = DEFAULT_GAME_CONFIG
    return config["duchshund"]


def set_new_human_image_folder(folder_name):
    print(f"Overriding human image folder {folder_name}")
    return override_game_config({"human": f"human/{folder_name}"})


def override_game_config(new_config):
    print("overriding config")
    try:
        config = open_json_file("config.json")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Missing config file: {e}")
    updated_config = {**config, **new_config}
    try:
        validate_config(updated_config)
    except InvalidGameConfig as error:
        print(error)
        return False
    path = os.path.join(PROJECT_PATH, "config.json")
    with open(path, "w") as jsonFile:
        json.dump(updated_config, jsonFile)
        return True


def open_json_file(file_name):
    path = os.path.join(PROJECT_PATH, file_name)
    with open(path) as json_file:
        return json.load(json_file)


def write_to_file(file_name, rows):
    path = os.path.join(PROJECT_PATH, file_name)
    if not os.path.exists(path):
        raise FileExistsError(f"Missing config file in: {path}")
    with open(path, "w") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(rows)
