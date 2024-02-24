#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import Type


class Student(Type):
    balance: Optional[int] = None
    contract_id: Optional[int] = None
    at_school: Optional[bool] = None


class FamilyStatus(Type):
    students: list[Student] | None = None
