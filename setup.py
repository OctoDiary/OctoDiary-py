#    ____       _        _____  _                  
#   / __ \     | |      |  __ \(_)                 
#  | |  | | ___| |_ ___ | |  | |_  __ _ _ __ _   _ 
#  | |  | |/ __| __/ _ \| |  | | |/ _` | '__| | | |
#  | |__| | (__| || (_) | |__| | | (_| | |  | |_| |
#   \____/ \___|\__\___/|_____/|_|\__,_|_|   \__, |
#                                             __/ |
#                                            |___/ 
# 
#                 © Copyright 2023
#        🔒 Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import re

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("octodiary/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]


setup(
    name="octodiary",
    version=version,
    author="OctoDiary",
    description="Python библиотека для использования API: МЭШ / Моя Школа.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OctoDiary/OctoDiary-py",
    packages=find_packages(),
    license="Apache License 2.0",
    install_requires=[
        "pydantic",
        "aiohttp",
        "fake_useragent"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords=["octodiary", "api", "мэш", "моя школа", "myschool", "myschool api" "mesh"],
    python_requires=">=3.9",
    project_urls={
        "Bug Reports": "https://github.com/OctoDiary/OctoDiary-py/issues",
        "Source": "https://github.com/OctoDiary/OctoDiary-py",
        "Organization": "https://github.com/OctoDiary",
        "Telegram-Channel": "https://t.me/OctoDiary",
        "Examples": "https://github.com/OctoDiary/OctoDiary-py/blob/main/Examples.md",
    }
)
