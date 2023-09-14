from ...model import Type
from typing import List, Optional


class PayloadItem(Type):
    description: str
    subject_id: int
    subject_name: str
    date: str
    date_assigned_on: str
    homework_entry_student_id: int
    materials_count: List
    has_written_answer: bool
    is_done: bool
    type: str


class ShortHomeworks(Type):
    payload: Optional[List[PayloadItem]] = None
