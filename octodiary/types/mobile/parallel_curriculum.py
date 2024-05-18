#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import DT, Type


class Load(Type):
    id: Optional[int] = None
    hours: Optional[int] = None
    week_number: Optional[int] = None


class Subject(Type):
    subject_name: Optional[str] = None
    subject_id: Optional[int] = None
    total_hours: Optional[int] = None
    passed_hours: Optional[int] = None
    max_hours_per_week: Optional[int] = None
    min_hours_per_week: Optional[int] = None
    teachers: Optional[list[str]] = None
    loads: Optional[list[Load]] = None
    parent_subject_id: Optional[int] = None
    subject_integration_id: Optional[int] = None


class Section(Type):
    knowledge_field_name: str
    subjects: list[Subject]


class WeekHours(Type):
    hours: Optional[int] = None
    days: Optional[int] = None
    week_number: Optional[int] = None
    begin_date: Optional[DT] = None
    end_date: Optional[DT] = None


class ParallelCurriculum(Type):
    title: Optional[str] = None
    hours: Optional[int] = None
    comments: Optional[Any] = None
    specialization: Optional[Any] = None
    sections: Optional[list[Section]] = None
    short_name: Optional[str] = None
    education_level: Optional[str] = None
    days_in_week: Optional[int] = None
    education_form: Optional[str] = None
    class_level_id: Optional[int] = None
    study_profile: Optional[Any] = None
    is_adapted: Optional[bool] = None
    week_hours: Optional[list[WeekHours]] = None
