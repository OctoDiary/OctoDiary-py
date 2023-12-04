#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any

from octodiary.types.model import Type


class Path(Type):
    value: int | None = None
    remain: int | None = None
    weight: int | None = None


class Target(Type):
    value: int | None = None
    remain: int | None = None
    round: str | None = None
    paths: list[Path] | None = None


class Grade(Type):
    origin: str | None = None
    five: int | None = None
    hundred: int | None = None


class Value(Type):
    name: Any | None = None
    grade: Grade | None = None
    grade_system_id: Any | None = None
    grade_system_type: str | None = None


class Criterion(Type):
    name: Any | None = None
    value: str | None = None


class Mark(Type):
    id: int | None = None
    value: str | None = None
    values: list[Value] | None = None
    comment: str | None = None
    weight: int | None = None
    point_date: Any | None = None
    control_form_name: str | None = None
    comment_exists: bool | None = None
    created_at: Any | None = None
    updated_at: Any | None = None
    criteria: list[Criterion] | None = None
    date: str | None = None
    is_exam: bool | None = None
    is_point: bool | None = None
    original_grade_system_type: str | None = None


class Payload(Type):
    average: str | None = None
    dynamic: str | None = None
    period: str | None = None
    count: int | None = None
    target: Target | None = None
    marks: list[Mark] | None = None
    start: str | None = None
    end: str | None = None
    subject_name: str | None = None
    subject_id: int | None = None
    fixed_value: str | None = None


class ShortSubjectMarks(Type):
    payload: list[Payload] | None = None
