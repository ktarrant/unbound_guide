import os
import json
from jinja2 import Environment, PackageLoader, select_autoescape
from unbound_guide.utils import source_dir, json_dir


param_prefixes = [
    "ABILITY_", "ITEM_", "EGG_GROUP_", "MOVE_"
]


def clean_param_value(param_value):
    for param_prefix in param_prefixes:
        if param_value.startswith(param_prefix):
            return param_value.replace(param_prefix, "").replace("_", " ").title()
    return param_value


def clean_param_values(entry):
    if isinstance(entry, dict):
        for key in entry:
            entry[key] = clean_param_values(entry[key])
        return entry
    elif isinstance(entry, list):
        return [clean_param_values(value) for value in entry]
    elif isinstance(entry, str):
        return clean_param_value(entry)
    else:
        return entry


def update_egg_groups(entry, egg_groups):
    for key in ["eggGroup1", "eggGroup2"]:
        if key not in entry:
            continue
        group = entry[key]
        if group not in egg_groups:
            egg_groups[group] = set()
        if "name" not in entry:
            continue
        egg_groups[group].add(entry["name"])


def update_held_items(entry, items):
    for key in ["item1", "item2"]:
        if key not in entry:
            continue
        item = entry[key]
        if item == "None":
            continue
        if item not in items:
            items[item] = []
        if "name" not in entry:
            continue
        value = {"name": entry["name"]}
        if "location" in entry:
            value["location"] = entry["location"]
        else:
            value["location"] = []
        items[item].append(value)


def generate_pokedex():
    env = Environment(
        loader=PackageLoader("unbound_guide"),
        autoescape=select_autoescape()
    )

    template = env.get_template("pokedex.rst.template")

    egg_groups = {}
    held_items = {}

    pokedex_dir = os.path.join(json_dir, "pokedex")
    output_dir = os.path.join(source_dir, "pokedex")
    os.makedirs(output_dir, exist_ok=True)
    for _, _, files in os.walk(pokedex_dir):
        for file in files:
            with open(os.path.join(pokedex_dir, file)) as json_file:
                pokedex = json.load(json_file)

            if not pokedex:
                continue

            clean_param_values(pokedex)
            update_egg_groups(pokedex, egg_groups)
            update_held_items(pokedex, held_items)

            content = template.render(**pokedex)

            with open(os.path.join(output_dir, file.replace(".json", ".rst")), "w") as out_file:
                out_file.write(content)

    template = env.get_template("egg_groups.rst.template")
    content = template.render(egg_groups=egg_groups)
    egg_groups_out = os.path.join(source_dir, "appendix", "egg_groups.rst")
    with open(egg_groups_out, "w") as out_file:
        out_file.write(content)

    template = env.get_template("held_items.rst.template")
    content = template.render(held_items=held_items)
    held_items_out = os.path.join(source_dir, "appendix", "held_items.rst")
    with open(held_items_out, "w") as out_file:
        out_file.write(content)


if __name__ == "__main__":
    generate_pokedex()
