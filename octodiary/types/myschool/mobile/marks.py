from ...model import Type
from typing import Any, List, Optional


class PayloadItem(Type):
    id: int
    value: str
    values: Any
    comment: str
    weight: int
    point_date: Any
    control_form_name: str
    comment_exists: bool
    created_at: str
    updated_at: str
    criteria: Any
    date: str
    subject_name: str
    subject_id: int
    is_exam: bool
    is_point: bool
    original_grade_system_type: str


class Marks(Type):
    payload: Optional[List[PayloadItem]] = None
