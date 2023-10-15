#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any

from octodiary.types.model import Type


class Profile(Type):
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    birth_date: str | None = None
    sex: str | None = None
    user_id: int | None = None
    id: int | None = None
    contract_id: Any | None = None
    phone: str | None = None
    email: Any | None = None
    snils: str | None = None
    type: str | None = None


class School(Type):
    id: int | None = None
    name: str | None = None
    short_name: str | None = None
    county: str | None = None
    principal: str | None = None
    phone: str | None = None
    global_school_id: int | None = None


class Group(Type):
    id: int | None = None
    name: str | None = None
    subject_id: int | None = None
    is_fake: bool | None = None


class Representative(Type):
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    birth_date: Any | None = None
    sex: Any | None = None
    user_id: Any | None = None
    id: int | None = None
    contract_id: Any | None = None
    phone: str | None = None
    email: str | None = None
    snils: str | None = None
    type: Any | None = None


class Section(Type):
    id: int | None = None
    name: str | None = None
    subject_id: Any | None = None
    is_fake: bool | None = None


class Child(Type):
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    birth_date: str | None = None
    sex: str | None = None
    user_id: int | None = None
    id: int | None = None
    contract_id: int | None = None
    phone: str | None = None
    email: Any | None = None
    snils: str | None = None
    type: Any | None = None
    school: School | None = None
    class_name: str | None = None
    class_level_id: int | None = None
    class_unit_id: int | None = None
    groups: list[Group] | None = None
    representatives: list[Representative] | None = None
    sections: list[Section] | None = None
    sudir_account_exists: bool | None = None
    sudir_login: Any | None = None
    is_legal_representative: bool | None = None
    parallel_curriculum_id: int | None = None
    contingent_guid: str | None = None
    enrollment_date: str | None = None


class FamilyProfile(Type):
    profile: Profile | None = None
    children: list[Child] | None = None
    hash: str | None = None
