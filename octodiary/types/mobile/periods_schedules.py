#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import DT, Type


class PeriodsSchedules(Type):
    date: Optional[DT] = None
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    events: Optional[Any] = None
