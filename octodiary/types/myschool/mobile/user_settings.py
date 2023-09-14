from ...model import Type
from typing import Optional


class Theme(Type):
    type: str
    is_automatic: bool
    color_pattern: str


class UserSettings(Type):
    goal: Optional[bool] = None
    theme: Optional[Theme] = None
    schedule_type: Optional[str] = None
    estimation_type: Optional[str] = None
