# Python Future imports
from __future__ import unicode_literals

# Python System imports
from os import path
from setuptools import setup

# Technicals parameters you need to set
NAME = "python-memory-profiler"
DESCRIPTION = "A package for monitoring memory usage of a python program."

# Technical parameters that should be more or less the same for every projects
CLASSIFIERS = [
    "Programming Language :: Python :: 3.6",
]

with open(path.join(path.dirname(__file__), "requirements.txt")) as req:
    REQUIREMENTS = list(line.strip() for line in req)

setup(
    name=NAME,
    version="0.3.1",
    author="Ghassene Jebali",
    description=DESCRIPTION,
    include_package_data=True,
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
)
