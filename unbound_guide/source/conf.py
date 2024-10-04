# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import json

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Pokemon Unbound Guide'
copyright = '2024, Kevin Tarrant'
author = 'Kevin Tarrant'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


def generate_pokedex(app):
    limit_counter = 10
    root_dir = os.path.dirname(__file__)

    with open(os.path.join(root_dir, "pokedex.rst.template"), "r") as in_file:
        template_src = in_file.read()

    pokedex_dir = os.path.join(root_dir, "json", "pokedex")
    output_dir = os.path.join(root_dir, "pokedex")
    os.makedirs(output_dir, exist_ok=True)
    for _, _, files in os.walk(pokedex_dir):
        for file in files:
            if not limit_counter:
                break
            limit_counter -= 1

            with open(os.path.join(pokedex_dir, file)) as json_file:
                json.load(json_file)

            # TODO Perform template update
            with open(os.path.join(output_dir, file.replace(".json", ".rst")), "w") as out_file:
                out_file.write(template_src)


def setup(app):
    app.connect("builder-inited", generate_pokedex)
