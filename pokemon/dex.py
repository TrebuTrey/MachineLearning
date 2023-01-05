import logging
import os
import pandas as pd

from config import POKEMON_GAME
from image import SpriteType, create_pokemon_sprite_fn
from helpers.log import get_logger, mod_fname
logger = logging.getLogger(mod_fname(__file__))

SPRITES_DIR = "images/sprites"
POKEMON_CSV_FN = "pokemon.csv"

# making dataframe
df = pd.read_csv(POKEMON_CSV_FN)
   
# filter the dataframe by pokemon with a code of 1
df = df.loc[df["CODE"] == 1]


def get_pokemon_number(name: str) -> int:
    """Retrieve a Pokémon's national number by its name."""
    new_df = df.copy()
    pokemon = new_df.loc[df["NAME"].str.upper() == name]
    number = pokemon.get("NUMBER").values[0]
    logger.debug(f"name: {name} | number: {number}")
    return number


def gen_2_dex() -> pd.DataFrame:
    """Retrieve a dex of only Pokémon from generation II."""
    gen_2_df = df.copy()
    return gen_2_df.loc[df["NUMBER"] <= 251]


def test_sprite_images_exist():
    new_df = df.copy()
    for index, row in new_df.iterrows():            
        pokemon_number = row.get("NUMBER")
        if pokemon_number > 251:
            logger.info("Test success!")
            break
        pokemon_name = row.get("NAME")
        normal_fn = create_pokemon_sprite_fn(number=pokemon_number,
                                             name=pokemon_name,
                                             game=POKEMON_GAME,
                                             type_=SpriteType.NORMAL)
        shiny_fn = create_pokemon_sprite_fn(number=pokemon_number,
                                            name=pokemon_name,
                                            game=POKEMON_GAME,
                                            type_=SpriteType.SHINY)
        if os.path.exists(normal_fn) and os.path.exists(shiny_fn):
            logger.info(f"{normal_fn} and {shiny_fn} exists")
        else:
            logger.error("Test failed")
            raise FileNotFoundError(f"either {normal_fn} or {shiny_fn} does not exist")


if __name__ == "__main__":
    logger = get_logger(logger.name)
    test_sprite_images_exist()
