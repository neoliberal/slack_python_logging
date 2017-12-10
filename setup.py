"""setup"""
from typing import List

from setuptools import setup, find_packages

with open("requirements.txt") as file:
    requirements: List[str] = file.read().splitlines()

setup(
    name="slack_python_logging",
    description="Module for logging to a Slack Channel with Webhooks",
    version="1.2.0",
    python_requires='>=3',
    install_requires=requirements,
    packages=find_packages(),
    # metadata
    author="Abhi Agarwal",
    author_email="abhi@neoliber.al",
    url="https://github.com/neoliberal/slack_python_logging",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords=["reddit", "slack python_logging"]
)
