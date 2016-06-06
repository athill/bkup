
# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


from setuptools import setup



with open("readme.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "bkup",
    packages = ["bkup"],
    entry_points = {
        "console_scripts": ['bkup = bkup.bkup:main']
        },
    version = '0.9.2',
    description = "Archive files and folders.",
    long_description = long_descr,
    author = "Andy Hill",
    author_email = "andy@andyhill.us",
    url = "https://github.com/athill/bkup",
)