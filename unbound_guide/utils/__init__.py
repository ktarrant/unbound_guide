import os
import json

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
source_dir = os.path.join(root_dir, "source")
json_dir = os.path.join(source_dir, "json")
pokedex_dir = os.path.join(json_dir, "pokedex")
routes_dir = os.path.join(source_dir, "routes")


def get_pokedex_entry(species):
    pokedex_file = os.path.join(pokedex_dir, f"{species}.json")
    if not os.path.exists(pokedex_file):
        raise FileNotFoundError(pokedex_file)

    with open(pokedex_file, "r") as file:
        return json.load(file)
