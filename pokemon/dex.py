import logging
import pandas as pd

from helpers.log import get_logger, mod_fname
logger = logging.getLogger(mod_fname(__file__))

POKEMON_CSV_FN = "pokemon.csv"

# making dataframe
df = pd.read_csv(POKEMON_CSV_FN)
   
# filter the dataframe by pokemon with a code of 1
df = df.loc[df["CODE"] == 1]


def get_pokemon_number(name: str) -> int:
    """Retrieve a Pokémon's national number by its name."""
    new_df = df.copy()
    pokemon = new_df.loc[df["NAME"].str.upper() == name.upper()]
    number = pokemon.get("NUMBER").values[0]
    logger.debug(f"name: {name} | number: {number}")
    return number


def gen_2_dex() -> pd.DataFrame:
    """Retrieve a dex of only Pokémon from generation II."""
    gen_2_df = df.copy()
    return gen_2_df.loc[df["NUMBER"] <= 251]


if __name__ == "__main__":
    logger = get_logger(logger.name)
    logger.info("hi from dex.py")
