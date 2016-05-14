
# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('bkup/bkup.py').read(),
    re.M
    ).group(1)


with open("readme.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "bkup",
    packages = ["bkup"],
    entry_points = {
        "console_scripts": ['bkup = bkup.bkup:main']
        },
    version = version,
    description = "Archive files and folders.",
    long_description = long_descr,
    author = "Andy Hill",
    author_email = "andy@andyhill.us",
    url = "https://github.com/athill/bkup",
    )