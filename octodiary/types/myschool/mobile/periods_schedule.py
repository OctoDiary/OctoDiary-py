from ...model import Type
from typing import Any


class PeriodSchedule(Type):
    date: str
    type: str
    title: str
    description: Any
    events: Any
