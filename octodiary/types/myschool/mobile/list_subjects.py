from typing import Optional

from ...model import Type


class Subject(Type):
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None

class SubjectList(Type):
    payload: list[Subject]
