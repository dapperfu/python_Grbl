#!/usr/bin/env python3
import os

import setuptools

import versioneer

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))


def read_requirements(path="requirements.txt"):
    """Read requirements file relative to setup.py"""
    full_path = os.path.join(LOCAL_DIR, path)

    def yield_line(path):
        with open(path, "r") as fid:
            for line in fid.readlines():
                yield line

    return [
        requirement.strip()
        for requirement in yield_line(full_path)
        if not requirement.startswith("#")
    ]


requirements = read_requirements()
test_requirements = read_requirements(path="requirements_test.txt")

setuptools.setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="grbl",
    description="Python module to control Grbl CNC Firmware.",
    author="Jed",
    license="BSD",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=requirements,
    extras_require={"test": test_requirements},
    include_package_data=True,
    entry_points={"console_scripts": ["grblcli = grbl:cli"]},
)
