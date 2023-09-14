from ...model import Type
from typing import Optional, List, Any


class Mark(Type):
    id: int
    value: str
    values: Any
    comment: str
    weight: int
    point_date: Any
    control_form_name: str
    comment_exists: bool
    created_at: Any
    updated_at: Any
    criteria: Any
    date: str
    is_exam: bool
    is_point: bool
    original_grade_system_type: str


class Path(Type):
    value: int
    remain: int
    weight: int


class Target(Type):
    value: int
    remain: int
    round: str
    paths: List[Path]


class Period(Type):
    start: str
    end: str
    title: str
    dynamic: str
    value: str
    marks: List[Mark]
    count: int
    target: Target
    fixed_value: Any


class SubjectMarksForSubject(Type):
    average: Optional[str] = None
    dynamic: Optional[str] = None
    periods: Optional[List[Period]] = None
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    average_by_all: Optional[str] = None
