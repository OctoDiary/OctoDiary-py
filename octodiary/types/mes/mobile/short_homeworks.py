#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import datetime

from octodiary.types.model import Type


class MaterialsCount(Type):
    amount: int | None = None
    selected_mode: str | None = None


class Payload(Type):
    description: str | None = None
    subject_id: int | None = None
    subject_name: str | None = None
    date: datetime.date | None = None
    date_assigned_on: str | None = None
    homework_entry_student_id: int | None = None
    materials_count: list[MaterialsCount] | None = None
    has_written_answer: bool | None = None
    is_done: bool | None = None
    type: str | None = None
    has_teacher_answer: bool | None = None


class ShortHomeworks(Type):
    payload: list[Payload] | None = None
