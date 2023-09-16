from ...model import Type
from typing import List, Optional, Any


class Subject(Type):
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    total_hours: Optional[int] = None
    passed_hours: Optional[int] = None
    max_hours_per_week: Optional[int] = None
    min_hours_per_week: Optional[int] = None


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
