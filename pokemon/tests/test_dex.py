import __init__

from dex import get_pokemon_number, gen_2_dex
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

MODULE = "dex.py"


def test_1_get_pokemon_number():
    logger.info("Test 1 - get_pokemon_number")
    assert(get_pokemon_number("bulbasaur") == 1)
    assert(get_pokemon_number("BULBASAUR") == 1)
    assert(get_pokemon_number("MEW") == 151)
    assert(get_pokemon_number("celebi") == 251)
    logger.info("Test 1 - success!")


def test_2_gen_2_dex():
    logger.info("Test 2 - gen_2_dex")
    df = gen_2_dex()
    assert(df.shape[0] == 251)
    bulbasaur = df.loc[df["NAME"].str.upper() == "BULBASAUR"]
    assert(bulbasaur.get("NUMBER").values[0] == 1)
    celebi = df.loc[df["NAME"].str.upper() == "CELEBI"]
    assert(celebi.get("NUMBER").values[0] == 251)
    logger.info("Test 2 - success!")


if __name__ == "__main__":
    logger.info(f"Testing {MODULE}")
    test_1_get_pokemon_number()
    test_2_gen_2_dex()
    logger.info("All tests pass!")