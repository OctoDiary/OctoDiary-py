from ...model import Type
from typing import Any, Optional


class PeriodSchedule(Type):
    date: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[Any] = None
    events: Optional[Any] = None
