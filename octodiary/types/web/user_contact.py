#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import EveryType, Type


class UserContact(Type):
    data: Optional[str] = None
    type: Optional[EveryType] = None
    is_deleted: Optional[bool] = None
