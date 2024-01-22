#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

__version__ = "0.2.9"

from octodiary import asyncApi, exceptions, syncApi, types
from octodiary.urls import MySchoolURLs

__all__ = [
    "asyncApi",
    "syncApi",
    "exceptions",
    "types",
    "MySchoolURLs",
    "__version__"
]
