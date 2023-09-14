from ...model import Type
from typing import List, Optional, Any


class Path(Type):
    value: int
    remain: int
    weight: int


class TargetItem(Type):
    value: int
    remain: int
    round: Optional[str]
    paths: List[Path]


class Grade(Type):
    origin: str
    five: int
    hundred: int


class Value(Type):
    name: Any
    grade: Grade
    grade_system_id: Any
    grade_system_type: str


class Criterion(Type):
    name: Any
    value: str


class Mark(Type):
    id: int
    value: str
    values: List[Value]
    comment: str
    weight: int
    point_date: Any
    control_form_name: str
    comment_exists: bool
    created_at: Any
    updated_at: Any
    criteria: List[Criterion]
    date: str
    is_exam: bool
    is_point: bool
    original_grade_system_type: str


class PayloadItem(Type):
    average: Optional[str]
    dynamic: str
    period: Optional[str]
    count: Optional[int]
    target: Optional[TargetItem]
    marks: Optional[List[Mark]]
    start: Optional[str]
    end: Optional[str]
    subject_name: str
    subject_id: int
    fixed_value: Any


class ShortSubjectMarks(Type):
    payload: Optional[List[PayloadItem]] = None
