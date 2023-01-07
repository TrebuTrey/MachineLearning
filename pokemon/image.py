from enum import Enum
import glob
import logging
import os
from typing import List

import cv2
from PIL import Image

from config import RETROARCH_SCREENSHOTS_DIR
from dex import get_pokemon_number
from helpers.opencv_util import compare_img_color, get_image_height, get_image_width
from helpers.log import get_logger, mod_fname
logger = logging.getLogger(mod_fname(__file__))


SPRITES_DIR = os.path.join("images", "sprites")


class SpriteType(str, Enum):
    """Enumeration for sprite types."""
    NORMAL = "normal"
    SHINY = "shiny"


def determine_sprite_type(name: str, game: str, img: cv2.Mat) -> SpriteType:
    """Determine the sprite type based on image color comparison."""
    # retrieve db image filenames
    normal_fn = create_pokemon_sprite_fn(name, game, SpriteType.NORMAL)
    shiny_fn = create_pokemon_sprite_fn(name, game, SpriteType.SHINY)
    
    normal_img = cv2.imread(normal_fn)
    shiny_img = cv2.imread(shiny_fn)
    img = cv2.resize(img, (get_image_width(normal_img), get_image_height(normal_img)))

    # use color differences to determine sprite type
    diff_normal = compare_img_color(img, normal_img)
    diff_shiny = compare_img_color(img, shiny_img)
    if diff_normal < diff_shiny:
        logger.info(f"{name} is more similar to normal")
        return SpriteType.NORMAL
    else:
        logger.info(f"{name} is more similar to shiny")
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
        pokemon_fn = os.path.join(_dir, game.lower(), _type, base_fn)
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


def crop_pokemon_in_battle(battle_img_fn: str, del_png: bool = True) -> cv2.Mat:
    """Crop square image of a Pokémon in battle."""
    im = Image.open(battle_img_fn)

    # percentages used in calcs were determined empirically
    # valid only for generation II games
    pokemon_width = im.width*(0.35)
    pokemon_height = pokemon_width
    left = im.width*(0.6)
    right = left + pokemon_width
    top = 0
    bottom = pokemon_height

    # crop image and save to disk
    im = im.crop((left, top, right, bottom))
    cropped_fn = "crop.png"
    im.save(cropped_fn)

    # load into OpenCV obj
    img = cv2.imread(cropped_fn)
    
    if del_png:
        os.remove(cropped_fn)

    return img


def crop_name_in_battle(battle_img_fn: str) -> str:
    """Crop name of a Pokémon in battle."""
    im = Image.open(battle_img_fn)

    # generation II games have maximum 10 letters for names
    max_letters = 10
    for i in range(max_letters):
        # percentages used in calcs were determined empirically
        # valid only for generation II games
        letter_width = im.width*(0.04375)
        letter_height = letter_width
        letter_space = letter_width/7
        
        left = i*(letter_width + letter_space) + im.width*(0.05)
        right = left + letter_width
        top = 0
        bottom = letter_height

        im1 = im.crop((left, top, right, bottom))
        cropped_fn = "name_" + str(i) + ".png"
        im1.save(cropped_fn)
    return cropped_fn


def get_name(battle_img_fn: str) -> str:
    """Crop name of a Pokémon in battle."""
    name = ""
    pix = []
    im = Image.open(battle_img_fn)

    # percentages used in calcs were determined empirically
    # valid only for generation II games
    for i in range(1, 3):
        name_width = im.width*(0.0495)
        name_height = im.height*(0.05)
        left = i*name_width
        right = left + name_width
        top = 0
        bottom = name_height

        im1 = im.crop((left, top, right, bottom))
        cropped_fn = "char_" + str(i) + ".png"
        im1.save(cropped_fn)
        for x in range(0, im1.width):
            for y in range(0, im1.height):
                coordinate = x, y
                pix = im1.getpixel(coordinate)
                avg = round(pix[0]+pix[1]+pix[2]/3)
                # print(avg)
                if avg >= 300:
                    pix = (255, 255, 255)
                else:
                    pix = (0, 0, 0)
                print(pix)
                im1.putpixel(coordinate, pix)
        im1.save(cropped_fn)
                
        
    
    return name


def test_img_color(name: str, game: str, img_fn: str, _type: SpriteType):
    img = cv2.imread(img_fn)
    sprite_type = determine_sprite_type(name, game, img)
    assert(sprite_type == _type)
    logger.info("Test success!")


if __name__ == "__main__":
    logger = get_logger(logger.name)

    # test 2
    name = "gyarados"
    game = "crystal"
    emulator_battle_img_path = get_latest_screenshot_fn()
    get_name(emulator_battle_img_path)
    logger.info(f"testing {name} color: {emulator_battle_img_path}")
    cropped_letters = crop_name_in_battle(emulator_battle_img_path)

    cropped_img_path = crop_pokemon_in_battle(emulator_battle_img_path)
    name_path = crop_name_in_battle(emulator_battle_img_path)
    test_img_color(name, game, cropped_img_path, SpriteType.SHINY)