
# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup



with open("readme.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "pybkup",
    packages = ["pybkup"],
    entry_points = {
        "console_scripts": ['pybkup = pybkup.pybkup:main']
        },
    version = '0.8.0',
    description = "Archive files and folders.",
    long_description = long_descr,
    author = "Andy Hill",
    author_email = "andy@andyhill.us",
    url = "https://github.com/athill/pybkup",
    )