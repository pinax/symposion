#!/usr/bin/env python

from setuptools import setup, find_packages

import symposion


setup(
    name="symposion",
    author="James Tauber",
    author_email="jtauber@jtauber.com",
    version=symposion.__version__,
    description="A collection of Django apps for conference websites.",
    url="http://pinax.github.com/symposion/",
    packages=find_packages(exclude=["symposion_project"]),
    include_package_data=True,
    classifiers=(
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
    ),
)
