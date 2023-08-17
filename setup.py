# -*- coding: utf-8 -*-
"""Installer for the tud.addons.deepl package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.md").read(),
    ]
)


setup(
    name="tud.addons.deepl",
    version="1.0",
    description="The package includes the possibility to communicate with the DeepL-Api",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Mike Hallbauer",
    author_email="mike.hallbauer@tu-dresden.de",
    url="https://github.com/collective/tud.addons.deepl",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/tud.addons.deepl",
        "Source": "https://github.com/collective/tud.addons.deepl",
        "Tracker": "https://github.com/collective/tud.addons.deepl/issues",
        # 'Documentation': 'https://tud.addons.deepl.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["tud", "tud.addons"],
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "Products.GenericSetup>=1.8.2",
        "plone.api>=1.8.4",
        "plone.rest",
    ],
    extras_require={
        "test": [
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
