from ...model import Type
from typing import List, Optional, Any


class Subject(Type):
    subject_name: str
    subject_id: int
    total_hours: int
    passed_hours: int
    max_hours_per_week: int
    min_hours_per_week: int


class Section(Type):
    knowledge_field_name: str
    subjects: List[Subject]


class ParallelCurriculum(Type):
    title: Optional[str] = None
    hours: Optional[int] = None
    comments: Optional[Any] = None
    specialization: Optional[Any] = None
    sections: Optional[List[Section]] = None
    short_name: Optional[str] = None
    education_level: Optional[str] = None
    days_in_week: Optional[int] = None
    education_form: Optional[str] = None
    class_level_id: Optional[int] = None
    study_profile: Optional[Any] = None
    is_adapted: Optional[bool] = None
