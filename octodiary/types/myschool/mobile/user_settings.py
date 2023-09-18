from ...model import Type
from typing import Optional


class Theme(Type):
    type: Optional[str] = None
    is_automatic: Optional[bool] = None
    color_pattern: Optional[str] = None


class UserSettings(Type):
    goal: Optional[bool] = None
    theme: Optional[Theme] = None
    schedule_type: Optional[str] = None
    estimation_type: Optional[str] = None
