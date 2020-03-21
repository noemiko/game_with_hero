import os
from typing import List
import glob

from pygame import Surface
from pygame import image
from pygame import transform


def get_scaled_images(folder: str, scale: tuple) -> List[Surface]:
    """
    Load images from folder and scale to expected size.

    :param folder: folder name where is images
    :param scale:(width, height) information to which size scale all images
    :return: List of scaled surfaces
    """
    images = []
    image_path = os.path.join(f'images', folder)
    all_images = glob.glob(f"{image_path}/*.png")
    sorted_images = sorted(all_images)
    for image_ in sorted_images:
        surface = image.load(image_)
        surface = transform.scale(surface, scale)
        images.append(surface)
    return images
