#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import DT, Type


class Payload(Type):
    id: Optional[int] = None
    value: Optional[str] = None
    values: Optional[list] = None
    comment: Optional[str] = None
    weight: Optional[int] = None
    point_date: Optional[DT] = None
    control_form_name: Optional[str] = None
    comment_exists: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    criteria: Optional[Any] = None
    date: Optional[DT] = None
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    is_exam: Optional[bool] = None
    is_point: Optional[bool] = None
    original_grade_system_type: Optional[str] = None


class Marks(Type):
    payload: list[Payload] | None = None
