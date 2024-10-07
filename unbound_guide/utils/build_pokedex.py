import os
import json
from jinja2 import Environment, PackageLoader, select_autoescape
from unbound_guide.utils import source_dir, json_dir


def generate_pokedex():
    limit_counter = 10
    root_dir = os.path.dirname(__file__)

    env = Environment(
        loader=PackageLoader("unbound_guide"),
        autoescape=select_autoescape()
    )

    template = env.get_template("pokedex.rst.template")

    pokedex_dir = os.path.join(json_dir, "pokedex")
    output_dir = os.path.join(root_dir, "pokedex")
    os.makedirs(output_dir, exist_ok=True)
    for _, _, files in os.walk(pokedex_dir):
        for file in files:
            if not limit_counter:
                break
            limit_counter -= 1

            with open(os.path.join(pokedex_dir, file)) as json_file:
                json.load(json_file)

            content = template.render(the="variables", go="here")

            with open(os.path.join(output_dir, file.replace(".json", ".rst")), "w") as out_file:
                out_file.write(content)


if __name__ == "__main__":
    generate_pokedex()
