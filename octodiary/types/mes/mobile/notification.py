#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from octodiary.types.model import Type


class Notification(Type):
    datetime: str | None = None
    event_type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    subject_name: str | None = None
    new_hw_description: str | None = None
    teacher_name: str | None = None
    new_date_assigned_on: str | None = None
    new_date_prepared_for: str | None = None
    student_profile_id: int | None = None
    author_profile_id: int | None = None
    lesson_date: str | None = None
    old_mark_value: str | None = None
    new_mark_value: str | None = None
    new_is_exam: bool | None = None
    new_mark_weight: int | None = None
    control_form_name: str | None = None
