#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from .persondata import EveryType
from ...model import Type


class UserContact(Type):
    data: Optional[str] = None
    type: Optional[EveryType] = None
    is_deleted: Optional[Any] = None
