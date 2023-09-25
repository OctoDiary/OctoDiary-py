#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from ...model import Type


class Subject(Type):
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None


class SubjectList(Type):
    payload: list[Subject]
