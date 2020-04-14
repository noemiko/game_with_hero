import csv
import glob
import os
from typing import List
from typing import NamedTuple
from typing import Tuple

from duchshund_walk.settings import PROJECT_PATH
from pygame import Surface
from pygame import image
from pygame import transform


class Point(NamedTuple):
    x: int
    y: int


def get_images(folder: str) -> List[Surface]:
    """
    Load images from folder .

    :param folder: folder name where is images

    :return: List of surfaces
    """
    images = []
    path_to_images = os.path.join(PROJECT_PATH, "states/game/images")
    image_path = os.path.join(path_to_images, folder)
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


def open_file(file_name):
    path = os.path.join(PROJECT_PATH, file_name)
    try:
        with open(path, "r") as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []


def write_to_file(file_name, rows):
    path = os.path.join(PROJECT_PATH, file_name)
    with open(path, "w") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerows(rows)
