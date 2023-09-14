from ...model import Type
from typing import Optional


class Notification(Type):
    datetime: str
    event_type: str
    created_at: str
    updated_at: str
    lesson_date: Optional[str] = None
    old_mark_value: Optional[str] = None
    new_mark_value: Optional[str] = None
    new_is_exam: Optional[bool] = None
    new_mark_weight: Optional[int] = None
    control_form_name: Optional[str] = None
    subject_name: str
    teacher_name: str
    student_profile_id: int
    author_profile_id: int
    new_hw_description: Optional[str] = None
    new_date_assigned_on: Optional[str] = None
    new_date_prepared_for: Optional[str] = None
