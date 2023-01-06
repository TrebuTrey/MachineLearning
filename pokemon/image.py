from enum import Enum
import glob
import logging
import os
from typing import List

import cv2

from config import POKEMON_GAME, RETROARCH_SCREENSHOTS_DIR
from dex import gen_2_dex, get_pokemon_number
from helpers.opencv_util import compare_img_color, get_image_height, get_image_width
from helpers.log import get_logger, mod_fname
logger = logging.getLogger(mod_fname(__file__))


SPRITES_DIR = os.path.join("images", "sprites")


class SpriteType(str, Enum):
    """Enumeration for sprite types."""
    NORMAL = "normal"
    SHINY = "shiny"


def determine_sprite_type(name: str, game: str, img_fn: str) -> SpriteType:
    """Determine the sprite type based on image color comparison."""
    # retrieve db image filenames
    normal_fn = create_pokemon_sprite_fn(name, game, SpriteType.NORMAL)
    shiny_fn = create_pokemon_sprite_fn(name, game, SpriteType.SHINY)
    
    normal_img = cv2.imread(normal_fn)
    shiny_img = cv2.imread(shiny_fn)
    img = cv2.imread(img_fn)
    img = cv2.resize(img, (get_image_width(normal_img), get_image_height(normal_img)))

    # use color differences to determine sprite type
    diff_normal = compare_img_color(img, normal_img)
    diff_shiny = compare_img_color(img, shiny_img)
    if diff_normal < diff_shiny:
        logger.info("image is more similar to normal")
        return SpriteType.NORMAL
    else:
        logger.info("image is more similar to shiny")
        return SpriteType.SHINY


def create_pokemon_sprite_fn(name: str,
                             game: str,
                             _type: SpriteType = None,
                             _dir: str = SPRITES_DIR,
                             ext: str = "png"):
    """Generate the sprite filename from the Pokémon properites."""
    number = get_pokemon_number(name)
    base_fn = f"{number:03d}_{get_sprite_name(name)}.{ext}"
    if _type is None:
        pokemon_fn = os.path.join(_dir, base_fn)
    else:
        pokemon_fn = os.path.join(_dir, game, _type, base_fn)
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


def test_img_color(name: str, game: str, img_fn: str, _type: SpriteType):
    sprite_type = determine_sprite_type(name, game, img_fn)
    assert(sprite_type == _type)
    logger.info("Test success!")


def test_sprite_images_exist():
    dex = gen_2_dex()
    for _, row in dex.iterrows():            
        pokemon_name = row.get("NAME")
        normal_fn = create_pokemon_sprite_fn(name=pokemon_name,
                                             game=POKEMON_GAME,
                                             _type=SpriteType.NORMAL)
        shiny_fn = create_pokemon_sprite_fn(name=pokemon_name,
                                            game=POKEMON_GAME,
                                            _type=SpriteType.SHINY)
        if os.path.exists(normal_fn) and os.path.exists(shiny_fn):
            logger.debug(f"{normal_fn} and {shiny_fn} exists")
        else:
            logger.error("Test failed")
            raise FileNotFoundError(f"either {normal_fn} or {shiny_fn} does not exist")
    logger.info("Test success!")


if __name__ == "__main__":
    logger = get_logger(logger.name)

    logger.info(f"testing all sprite images exist")
    test_sprite_images_exist()

    emulator_test_img_path = get_latest_screenshot_fn()
    name = "gyarados"
    game = "crystal"
    logger.info(f"testing img color: {emulator_test_img_path}")
    test_img_color(name, game, emulator_test_img_path, SpriteType.SHINY)