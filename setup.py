#!/usr/bin/env python

from setuptools import setup

setup(
    name="pino",
    version="0.5.0",
    author="Adrien Becchis @Coorpacademy",
    author_email="adriean.khisbe@live.fr",
    description="Python json logger inspired by pino.js",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/CoorpAcademy/pino.py",
    license="MIT",
    packages=["pino"],
    scripts=['bin/pino-pretty'],
    install_requires=[],
    #setup_requires=["pytest-runner"],
    #tests_require=["tox", "pytest", "pyte"],
    #test_suite="tests",
    keywords="cli terminal log logger logging json",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging"
    ]
)
