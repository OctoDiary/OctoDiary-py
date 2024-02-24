#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from octodiary.apis import async_, base, sync
from octodiary.apis.async_ import AsyncMobileAPI, AsyncWebAPI
from octodiary.apis.base import AsyncBaseAPI, SyncBaseAPI
from octodiary.apis.sync import SyncMobileAPI, SyncWebAPI

__all__ = [
    "async_",
    "base",
    "sync",
    "AsyncBaseAPI",
    "AsyncMobileAPI",
    "AsyncWebAPI",
    "SyncBaseAPI",
    "SyncMobileAPI",
    "SyncWebAPI",
]
