#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any

from octodiary.types.model import Type


class Payload(Type):
    id: int | None = None
    value: str | None = None
    values: Any | None = None
    comment: str | None = None
    weight: int | None = None
    point_date: Any | None = None
    control_form_name: str | None = None
    comment_exists: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    criteria: Any | None = None
    date: str | None = None
    subject_name: str | None = None
    subject_id: int | None = None
    is_exam: bool | None = None
    is_point: bool | None = None
    original_grade_system_type: str | None = None


class Marks(Type):
    payload: list[Payload] | None = None
