import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('censys_client/client.py').read(),
    re.M
    ).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name = "censys_client",
    packages = ["censys_client"],
    entry_points = {
        "console_scripts": ['censys-client = censys_client.client:main']
    },
    version = version,
    description = "A censys client that allow to you to use multiple api key.",
    long_description = long_descr,
    author = "SystemVll",
    author_email = "SystemVll+CJzsQs9YERcEn5r9@protonmail.ch",
    url = "https://github.com/SystemVll/censys-client",
)
