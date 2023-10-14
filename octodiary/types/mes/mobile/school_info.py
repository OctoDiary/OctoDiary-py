#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from octodiary.types.model import Type


class ClassroomTeacher(Type):
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None


class Address(Type):
    county: str | None = None
    district: str | None = None
    address: str | None = None


class Teacher(Type):
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    subject_names: list[str] | None = None


class Branch(Type):
    name: str | None = None
    type: str | None = None
    address: str | None = None
    is_main_building: bool | None = None
    is_student_building: bool | None = None


class SchoolInfo(Type):
    id: int | None = None
    name: str | None = None
    type: str | None = None
    principal: str | None = None
    classroom_teachers: list[ClassroomTeacher] | None = None
    address: Address | None = None
    phone: str | None = None
    email: str | None = None
    website_link: str | None = None
    teachers: list[Teacher] | None = None
    branches: list[Branch] | None = None
