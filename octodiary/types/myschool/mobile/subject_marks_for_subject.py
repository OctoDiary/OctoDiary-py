import datetime
from ...model import Type
from typing import Optional, List, Any


class Mark(Type):
    id: Optional[int] = None
    value: Optional[str] = None
    values: Optional[Any] = None
    comment: Optional[str] = None
    weight: Optional[int] = None
    point_date: Optional[datetime.datetime | datetime.date] = None
    control_form_name: Optional[str] = None
    comment_exists: Optional[bool] = None
    created_at: Optional[datetime.datetime | datetime.date] = None
    updated_at: Optional[datetime.datetime | datetime.date] = None
    criteria: Optional[Any] = None
    date: Optional[datetime.date] = None
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
    paths: Optional[List[Path]] = []


class Period(Type):
    start: Optional[datetime.datetime | datetime.date] = None
    end: Optional[datetime.datetime | datetime.date] = None
    title: Optional[str] = None
    dynamic: Optional[str] = None
    value: Optional[str] = None
    marks: Optional[List[Mark]] = []
    count: Optional[int] = None
    target: Optional[Target] = None
    fixed_value: Optional[Any] = None


class SubjectMarksForSubject(Type):
    average: Optional[str] = None
    dynamic: Optional[str] = None
    periods: Optional[List[Period]] = None
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    average_by_all: Optional[str] = None
