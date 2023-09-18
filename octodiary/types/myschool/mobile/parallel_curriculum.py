#    ____       _        _____  _                  
#   / __ \     | |      |  __ \(_)                 
#  | |  | | ___| |_ ___ | |  | |_  __ _ _ __ _   _ 
#  | |  | |/ __| __/ _ \| |  | | |/ _` | '__| | | |
#  | |__| | (__| || (_) | |__| | | (_| | |  | |_| |
#   \____/ \___|\__\___/|_____/|_|\__,_|_|   \__, |
#                                             __/ |
#                                            |___/ 
# 
#                 © Copyright 2023
#        🔒 Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, List, Optional

from ...model import Type


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
