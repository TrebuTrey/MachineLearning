import os

import cv2

import __init__

from dex import gen_2_dex
from image import (
    SPRITES_DIR,
    SpriteType,
    create_pokemon_sprite_fn,
    crop_pokemon_in_battle,
    determine_sprite_type,
    get_sprite_name,
)
from helpers.opencv_util import compare_img_pixels
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from __init__ import TEST_IMG_DIR
MODULE = "image.py"
POKEMON_GAME = "Crystal"


def test_1_get_sprite_name():
    logger.info("Test 1 - get_sprite_name")
    assert(get_sprite_name("Nidoran F") == "nidoran-f")
    assert(get_sprite_name("Nidoran M") == "nidoran-m")
    assert(get_sprite_name("Mr. Mime") == "mr-mime")
    assert(get_sprite_name("Farfetch'd") == "farfetchd")
    logger.info("Test 1 - success!")


def test_2_create_pokemon_sprite_fn():
    logger.info("Test 2 - create_pokemon_sprite_fn")
    normal_fn = create_pokemon_sprite_fn(name="Gyarados",
                                         game=POKEMON_GAME,
                                         _type=SpriteType.NORMAL)
    assert(normal_fn == os.path.join(SPRITES_DIR, "crystal", SpriteType.NORMAL, "130_gyarados.png"))
    shiny_fn = create_pokemon_sprite_fn(name="Gyarados",
                                        game=POKEMON_GAME,
                                        _type=SpriteType.SHINY)
    assert(shiny_fn == os.path.join(SPRITES_DIR, "crystal", SpriteType.SHINY, "130_gyarados.png"))
    logger.info("Test 2 - success!")


def test_3_verify_sprite_images_exist():
    logger.info("Test 3 - verify_sprite_images_exist")
    dex = gen_2_dex()
    for _, row in dex.iterrows():            
        pokemon_name = row.get("NAME")
        normal_fn = create_pokemon_sprite_fn(name=pokemon_name,
                                             game=POKEMON_GAME,
                                             _type=SpriteType.NORMAL)
        shiny_fn = create_pokemon_sprite_fn(name=pokemon_name,
                                            game=POKEMON_GAME,
                                            _type=SpriteType.SHINY)
        assert(os.path.exists(normal_fn))
        logger.debug(f"{normal_fn} exists")
        assert(os.path.exists(shiny_fn))
        logger.debug(f"{shiny_fn} exists")
    logger.info("Test 3 - success!")


def test_4_crop_pokemon_in_battle():
    logger.info("Test 4 - crop_pokemon_in_battle")
    for i in range(3):
        n = i + 1
        input_img_fn = os.path.join(TEST_IMG_DIR, f"battle_img_{n}.png")
        output_img_fn = os.path.join(TEST_IMG_DIR, f"cropped_poke_battle_img_{n}.png")
        cropped_img = crop_pokemon_in_battle(input_img_fn, del_png=False)
        correct_img = cv2.imread(output_img_fn)
        assert(compare_img_pixels(cropped_img, correct_img) == 0)
    logger.info("Test 4 - success!")


if __name__ == "__main__":
    logger.info(f"Testing {MODULE}")
    test_1_get_sprite_name()
    test_2_create_pokemon_sprite_fn()
    test_3_verify_sprite_images_exist()
    test_4_crop_pokemon_in_battle()
    logger.info("All tests pass!")