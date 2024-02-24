#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from pydantic import RootModel

from octodiary.types.model import Type


class User(Type):
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    first_name: Optional[str] = None


class School(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    short_name: Optional[str] = None


class ClassUnit(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    home_based: Optional[bool] = None


class ClassMember(Type):
    id: Optional[int] = None
    type: Optional[str] = None
    user_id: Optional[int] = None
    person_id: Optional[str] = None
    agree_pers_data: Optional[bool] = None
    user: User | None = None
    school: School | None = None
    class_unit: ClassUnit | None = None
    roles: list | None = None
    staff_id: Optional[str] = None


class ClassMembers(RootModel[list[ClassMember] | None]):
    root: list[ClassMember] | None = None
