from enum import Enum
import glob
import logging
import os
from typing import List

import cv2

from helpers.opencv_util import (
    RGB, get_color_diff, get_img_color, get_image_height, get_image_width
)
from helpers.log import get_logger, mod_fname
logger = logging.getLogger(mod_fname(__file__))

from config import RETROARCH_SCREENSHOTS_DIR

IMG_SIZE = 80
SPRITES_DIR = "images/sprites"


class SpriteType(str, Enum):
    """Enumeration for sprite types."""
    NORMAL = "normal"
    SHINY = "shiny"


def compare_img_color(img1: cv2.Mat, img2: cv2.Mat) -> float:
    """Compares the color of two images.
    Result is a number between [min=0,max=255*sqrt(3)] where min -> same color and
    max -> opposite color (white vs black)."""
    rgb1 = get_img_color(img1)
    rgb2 = get_img_color(img2)
    return get_color_diff(rgb1, rgb2)


def compare_img_pixels(img1: cv2.Mat, img2: cv2.Mat) -> float:
    """Compares two images for pixel equality.
    Result is a number between [min=0,max=unknown] where min -> same image and
    increasing value indicates more differences between the images."""
    # resize the images
    img1 = cv2.resize(img1, (IMG_SIZE, IMG_SIZE))
    img2 = cv2.resize(img2, (IMG_SIZE, IMG_SIZE))

    diff = 0
    for row1, row2 in zip(img1, img2):
        for pixel1, pixel2 in zip(row1, row2):
            # unpack into rgb values for each image
            rgb1 = RGB(pixel1)
            rgb2 = RGB(pixel2)
            diff += get_color_diff(rgb1, rgb2)
    logger.info(f"total diff: {diff}")
    return diff


def create_pokemon_sprite_fn(number: int,
                             name: str,
                             game: str,
                             dir_: str = SPRITES_DIR,
                             type_: SpriteType = None,
                             ext: str = "png"):
    """Generate the sprite filename from the Pokémon properites."""
    base_fn = f"{number:03d}_{get_sprite_name(name)}.{ext}"
    if type_ is None:
        pokemon_fn = os.path.join(dir_, base_fn)
    else:
        pokemon_fn = os.path.join(dir_, game, type_, base_fn)
    logger.debug(f"pokemon_fn: {pokemon_fn}")
    return pokemon_fn


def get_sprite_name(name: str):
    """Retrieve a Pokémon's sprite name."""
    return name.lower().replace(' ','-').replace('.','').replace('\'','')


def get_screenshots() -> List[str]:
    """Retrieve all screenshots sorted by creation time."""
    # only grab PNG files
    glob_pattern = os.path.join(RETROARCH_SCREENSHOTS_DIR, "*.png")
    files = list(filter(os.path.isfile, glob.glob(glob_pattern)))
    
    # sort by file creation time
    files.sort(key=os.path.getctime)
    return files


def get_latest_screenshot_fn() -> str:
    """Retrieve the most recent screenshot."""
    files = get_screenshots()
    if len(files) == 0:
        logger.warning("No screenshots exist")
        return None
    return files[-1]  # last element in list is most recent


def test_img_color(img_fn: str, normal_fn: str, shiny_fn: str):
    img = cv2.imread(img_fn)
    normal_img = cv2.imread(normal_fn)
    shiny_img = cv2.imread(shiny_fn)
    img = cv2.resize(img, (get_image_width(normal_img), get_image_height(normal_img)))
    
    diff_normal = compare_img_color(img, normal_img)
    diff_shiny = compare_img_color(img, shiny_img)
    if diff_normal < diff_shiny:
        logger.info("image is more similar to normal")
    else:
        logger.info("image is more similar to shiny")


def test_diff_img(img1_fn: str, img2_fn: str):
    img1 = cv2.imread(img1_fn)
    img2 = cv2.imread(img2_fn)
    img_diff = compare_img_pixels(img1, img2)
    assert(img_diff != 0)
    logger.info("images are different")


def test_same_img(img_fn: str):
    img = cv2.imread(img_fn)
    img_diff = compare_img_pixels(img, img)
    assert(img_diff == 0)
    logger.info("images are same")


if __name__ == "__main__":
    logger = get_logger(logger.name)
    emulator_test_img_path = get_latest_screenshot_fn()
    normal_img_path = "images/sprites/crystal/normal/130_gyarados.png"
    shiny_img_path = "images/sprites/crystal/shiny/130_gyarados.png"
    
    logger.info(f"comparing img to itself: {normal_img_path}")
    test_same_img(normal_img_path)

    logger.info(f"comparing imgs: {normal_img_path} and {shiny_img_path}")
    test_diff_img(normal_img_path, shiny_img_path)

    logger.info(f"testing img color: {normal_img_path}")
    test_img_color(emulator_test_img_path, normal_img_path, shiny_img_path)