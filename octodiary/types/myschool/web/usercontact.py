#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import Type
from octodiary.types.myschool.web.persondata import EveryType


class UserContact(Type):
    data: Optional[str] = None
    type: Optional[EveryType] = None
    is_deleted: Optional[Any] = None
