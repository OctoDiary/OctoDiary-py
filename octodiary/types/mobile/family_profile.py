#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import DT, Type


class Profile(Type):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[DT] = None
    sex: Optional[str] = None
    user_id: Optional[int] = None
    id: Optional[int] = None
    contract_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    snils: Optional[str] = None
    type: Optional[str] = None


class School(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    short_name: Optional[str] = None
    county: Optional[str] = None
    principal: Optional[str] = None
    phone: Optional[str] = None
    global_school_id: Optional[int] = None


class Group(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    subject_id: Optional[int] = None
    is_fake: Optional[bool] = None


class Representative(Type):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[DT] = None
    sex: Optional[str] = None
    user_id: Optional[int] = None
    id: Optional[int] = None
    contract_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    snils: Optional[str] = None
    type: Optional[str] = None


class Section(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    subject_id: Optional["int | str"] = None
    is_fake: Optional[bool] = None


class Child(Type):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[DT] = None
    sex: Optional[str] = None
    user_id: Optional[int] = None
    id: Optional[int] = None
    contract_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    snils: Optional[str] = None
    type: Optional[str] = None
    school: School | None = None
    class_name: Optional[str] = None
    class_level_id: Optional[int] = None
    class_unit_id: Optional[int] = None
    groups: list[Group] | None = None
    representatives: list[Representative] | None = None
    sections: list[Section] | None = None
    sudir_account_exists: Optional[bool] = None
    sudir_login: Optional[str] = None
    is_legal_representative: Optional[bool] = None
    parallel_curriculum_id: Optional[int] = None
    contingent_guid: Optional[str] = None
    enrollment_date: Optional[DT] = None


class FamilyProfile(Type):
    profile: Profile | None = None
    children: list[Child] | None = None
    hash: Optional[str] = None
