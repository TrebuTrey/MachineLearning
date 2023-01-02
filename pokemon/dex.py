import os
import pandas as pd

SPRITES_DIR = "sprites"
POKEMON_CSV_FN = "pokemon.csv"

# making dataframe
df = pd.read_csv(POKEMON_CSV_FN)
   
# filter the dataframe by pokemon with a code of 1
df = df.loc[df["CODE"] == 1]


def get_pokemon_number(name: str) -> int:
    pokemon = df.loc[df["NAME"].str.upper() == name]
    number = pokemon.get("NUMBER").values[0]
    return number


def get_pokemon_fn(number: int, name: str, ext: str = "png"):
    base_fn = f"{number:03d}_{name.lower().replace(' ', '')}.{ext}"
    pokemon_fn = os.path.join(SPRITES_DIR, base_fn)
    return pokemon_fn


def test_sprite_images_exist():
    for index, row in df.iterrows():            
        pokemon_number = row.get("NUMBER")
        if pokemon_number > 251:
            print("Test success!")
            break
        pokemon_name = row.get("NAME")
        fn = get_pokemon_fn(pokemon_number, pokemon_name)
        if os.path.exists(fn):
            print(f"{fn} exists")
        else:
            raise FileNotFoundError(f"{fn} does not exist!")


if __name__ == "__main__":
    test_sprite_images_exist()
