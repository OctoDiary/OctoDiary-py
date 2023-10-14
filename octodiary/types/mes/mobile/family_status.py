#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from octodiary.types.model import Type


class Student(Type):
    balance: int | None = None
    contract_id: int | None = None
    at_school: bool | None = None


class FamilyStatus(Type):
    students: list[Student] | None = None
