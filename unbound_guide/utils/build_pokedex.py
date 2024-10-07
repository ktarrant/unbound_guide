import os
import json
from jinja2 import Environment, PackageLoader, select_autoescape
from unbound_guide.utils import source_dir, json_dir


def generate_pokedex():
    env = Environment(
        loader=PackageLoader("unbound_guide"),
        autoescape=select_autoescape()
    )

    template = env.get_template("pokedex.rst.template")

    pokedex_dir = os.path.join(json_dir, "pokedex")
    output_dir = os.path.join(source_dir, "pokedex")
    os.makedirs(output_dir, exist_ok=True)
    for _, _, files in os.walk(pokedex_dir):
        for file in files:
            with open(os.path.join(pokedex_dir, file)) as json_file:
                pokedex = json.load(json_file)

            content = template.render(**pokedex)

            with open(os.path.join(output_dir, file.replace(".json", ".rst")), "w") as out_file:
                out_file.write(content)


if __name__ == "__main__":
    generate_pokedex()
