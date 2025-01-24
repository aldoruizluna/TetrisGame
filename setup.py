"""Setup file for Tetris game."""

from setuptools import setup, find_packages

setup(
    name="tetris",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame>=2.6.1",
    ],
    python_requires=">=3.6",
)
