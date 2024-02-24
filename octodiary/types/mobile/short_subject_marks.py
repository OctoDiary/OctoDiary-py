#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import DT, Type


class Path(Type):
    value: Optional[int] = None
    remain: Optional[int] = None
    weight: Optional[int] = None


class Target(Type):
    value: Optional[int] = None
    remain: Optional[int] = None
    round: Optional[str] = None
    paths: list[Path] | None = None


class Grade(Type):
    origin: Optional[str] = None
    five: Optional[int] = None
    hundred: Optional[int] = None


class Value(Type):
    name: Optional[str] = None
    grade: Grade | None = None
    grade_system_id: Optional[int] = None
    grade_system_type: Optional[str] = None


class Criterion(Type):
    name: Optional[str] = None
    value: Optional[str] = None


class Mark(Type):
    id: Optional[int] = None
    value: Optional[str] = None
    values: list[Value] | None = None
    comment: Optional[str] = None
    weight: Optional[int] = None
    point_date: Optional[DT] = None
    control_form_name: Optional[str] = None
    comment_exists: Optional[bool] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    criteria: list[Criterion] | None = None
    date: Optional[DT] = None
    is_exam: Optional[bool] = None
    is_point: Optional[bool] = None
    original_grade_system_type: Optional[str] = None


class Payload(Type):
    average: Optional[str] = None
    dynamic: Optional[str] = None
    period: Optional[str] = None
    count: Optional[int] = None
    target: Target | None = None
    marks: list[Mark] | None = None
    start: Optional[str] = None
    end: Optional[str] = None
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    fixed_value: Optional[str] = None


class ShortSubjectMarks(Type):
    payload: list[Payload] | None = None
