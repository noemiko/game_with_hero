import os
from typing import List, Tuple, NamedTuple
import glob
import csv

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
    image_path = os.path.join(f'states/game/images', folder)
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
    for image in images:
        scaled_image = transform.scale(image, scala)
        scaled_images.append(scaled_image)
    return scaled_images


def open_file(file_name):
    path = os.path.join(f'./', file_name)
    try:
        with open(path, 'r') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []


def write_to_file(file_name, rows):
    path = os.path.join(f'./', file_name)
    try:
        with open(path, 'w') as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(rows)
    except FileNotFoundError:
        return []
