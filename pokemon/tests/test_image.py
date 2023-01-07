import os

import __init__

from image import (
    SPRITES_DIR, SpriteType,
    create_pokemon_sprite_fn, get_sprite_name
)
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

MODULE = "image.py"


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
                                         game="Crystal",
                                         _type=SpriteType.NORMAL)
    assert(normal_fn == os.path.join(SPRITES_DIR, "crystal", SpriteType.NORMAL, "130_gyarados.png"))
    shiny_fn = create_pokemon_sprite_fn(name="Gyarados",
                                        game="Crystal",
                                        _type=SpriteType.SHINY)
    assert(shiny_fn == os.path.join(SPRITES_DIR, "crystal", SpriteType.SHINY, "130_gyarados.png"))
    logger.info("Test 2 - success!")


if __name__ == "__main__":
    logger.info(f"Testing {MODULE}")
    test_1_get_sprite_name()
    test_2_create_pokemon_sprite_fn()
    logger.info("All tests pass!")