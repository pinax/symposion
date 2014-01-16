#!/usr/bin/env python
import os
from setuptools import setup, find_packages

import symposion


def read_file(filename):
    """Read a file into a string."""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.ojoin(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name="symposion",
    author="James Tauber",
    author_email="jtauber@jtauber.com",
    version=symposion.__version__,
    description="A collection of Django apps for conference websites.",
    url="http://eldarion.com/symposion/",
    packages=find_packages(),
    include_package_data=True,
    classifiers=(
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
    ),
    install_requires=read_file("requirements/base.txt").splitlines(),
)
