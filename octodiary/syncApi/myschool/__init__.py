#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from .mobile import SyncMobileAPI
from .web import SyncWebAPI

__all__ = [
    "SyncWebAPI",
    "SyncMobileAPI",
]