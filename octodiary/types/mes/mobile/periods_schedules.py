#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from octodiary.types.model import Type


class PeriodsSchedules(Type):
    date: str | None = None
    type: str | None = None
    title: str | None = None
    description: None = None
    events: None = None
