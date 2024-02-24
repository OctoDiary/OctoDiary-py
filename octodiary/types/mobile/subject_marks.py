#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary


from typing import Any, Optional

from octodiary.types.model import DT, Type


class Mark(Type):
    id: Optional[int] = None
    value: Optional[str] = None
    values: Optional[Any] = None
    comment: Optional[str] = None
    weight: Optional[int] = None
    point_date: Optional[Any] = None
    control_form_name: Optional[str] = None
    comment_exists: Optional[bool] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    criteria: Optional[Any] = None
    date: Optional[DT] = None
    is_exam: Optional[bool] = None
    is_point: Optional[bool] = None
    original_grade_system_type: Optional[str] = None


class Path(Type):
    value: Optional[int] = None
    remain: Optional[int] = None
    weight: Optional[int] = None


class Target(Type):
    value: Optional[int] = None
    remain: Optional[int] = None
    round: Optional[str] = None
    paths: list[Path] | None = None


class Period(Type):
    start: Optional[str] = None
    end: Optional[str] = None
    title: Optional[str] = None
    dynamic: Optional[str] = None
    value: Optional[str] = None
    marks: list[Mark] | None = None
    count: Optional[int] = None
    target: Target | None = None
    fixed_value: Optional[str] = None
    start_iso: Optional[str] = None
    end_iso: Optional[str] = None


class Payload(Type):
    average: Optional[str] = None
    dynamic: Optional[str] = None
    periods: list[Period] | None = None
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    average_by_all: Optional[str] = None
    year_mark: Optional[Any] = None


class SubjectsMarks(Type):
    payload: list[Payload] | None = None
