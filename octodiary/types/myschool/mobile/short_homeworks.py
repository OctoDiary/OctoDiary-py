#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import datetime
from typing import Optional

from octodiary.types.model import Type


class PayloadItem(Type):
    description: Optional[str] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    date: Optional[datetime.date] = None
    date_assigned_on: Optional[str] = None
    homework_entry_student_id: Optional[int] = None
    materials_count: Optional[list] = None
    has_written_answer: Optional[bool] = None
    is_done: Optional[bool] = None
    type: Optional[str] = None


class ShortHomeworks(Type):
    payload: Optional[list[PayloadItem]] = None
