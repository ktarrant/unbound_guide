# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
sys.path.append("../..")

from unbound_guide.utils.build_pokedex import generate_pokedex
from unbound_guide.utils.build_routes import generate_routes

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


def _generate_pokedex(app):
    generate_pokedex()


def _generate_routes(app):
    generate_routes()

def setup(app):
    app.connect("builder-inited", _generate_pokedex)
    app.connect("builder-inited", _generate_routes)
