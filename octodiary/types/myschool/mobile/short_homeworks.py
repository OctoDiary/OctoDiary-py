import datetime
from ...model import Type
from typing import List, Optional


class PayloadItem(Type):
    description: Optional[str] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    date: Optional[datetime.date] = None
    date_assigned_on: Optional[str] = None
    homework_entry_student_id: Optional[int] = None
    materials_count: Optional[List] = None
    has_written_answer: Optional[bool] = None
    is_done: Optional[bool] = None
    type: Optional[str] = None


class ShortHomeworks(Type):
    payload: Optional[List[PayloadItem]] = None
