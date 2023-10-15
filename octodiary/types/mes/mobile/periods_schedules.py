#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any

from octodiary.types.model import Type


class PeriodsSchedules(Type):
    date: str | None = None
    type: str | None = None
    title: str | None = None
    description: Any | None = None
    events: Any | None = None
