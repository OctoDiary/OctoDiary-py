#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import Type


class PeriodSchedule(Type):
    date: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[Any] = None
    events: Optional[Any] = None
