#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from .mobile import AsyncMobileAPI
from .web import AsyncWebAPI

__all__ = [
    "AsyncWebAPI",
    "AsyncMobileAPI",
]
