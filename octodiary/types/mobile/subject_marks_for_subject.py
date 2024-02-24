#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import DT, Type


class Mark(Type):
    id: Optional[int] = None
    value: Optional[str] = None
    values: Optional[list] = None
    comment: Optional[str] = None
    weight: Optional[int] = None
    point_date: Optional[DT] = None
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
    paths: Optional[list[Path]] = []


class Period(Type):
    start: Optional[DT] = None
    end: Optional[DT] = None
    title: Optional[str] = None
    dynamic: Optional[str] = None
    value: Optional[str] = None
    marks: Optional[list[Mark]] = []
    count: Optional[int] = None
    target: Optional[Target] = None
    fixed_value: Optional["str | int"] = None


class SubjectMarksForSubject(Type):
    average: Optional[str] = None
    dynamic: Optional[str] = None
    periods: Optional[list[Period]] = None
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    average_by_all: Optional[str] = None
