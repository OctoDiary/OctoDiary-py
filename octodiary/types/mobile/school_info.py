#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import Type


class ClassroomTeacher(Type):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None


class Address(Type):
    county: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None


class Teacher(Type):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    subject_names: list[str] | None = None


class Branch(Type):
    name: Optional[str] = None
    type: Optional[str] = None
    address: Optional[str] = None
    is_main_building: Optional[bool] = None
    is_student_building: Optional[bool] = None


class SchoolInfo(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    principal: Optional[str] = None
    classroom_teachers: list[ClassroomTeacher] | None = None
    address: Address | None = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website_link: Optional[str] = None
    teachers: list[Teacher] | None = None
    branches: list[Branch] | None = None
