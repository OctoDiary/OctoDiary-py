#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import DT, Type


class MaterialsCount(Type):
    amount: Optional[int] = None
    selected_mode: Optional[str] = None


class Payload(Type):
    description: Optional[str] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    date: Optional[DT] = None
    date_assigned_on: Optional[str] = None
    homework_entry_student_id: Optional[int] = None
    materials_count: list[MaterialsCount] | None = None
    has_written_answer: Optional[bool] = None
    is_done: Optional[bool] = None
    type: Optional[str] = None
    has_teacher_answer: Optional[bool] = None


class ShortHomeworks(Type):
    payload: list[Payload] | None = None
