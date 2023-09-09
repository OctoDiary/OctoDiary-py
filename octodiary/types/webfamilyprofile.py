from .model import Type
from typing import List, Any, Optional


class Profile(Type):
    last_name: str
    first_name: str
    middle_name: str
    birth_date: str
    sex: str
    user_id: int
    id: int
    contract_id: Any
    phone: str
    email: str
    snils: str
    type: str


class School(Type):
    id: int
    name: str
    short_name: str
    county: Any
    principal: Any
    phone: Any
    global_school_id: int


class Group(Type):
    id: int
    name: str
    subject_id: int
    is_fake: bool


class Representative(Type):
    last_name: str
    first_name: str
    middle_name: str
    birth_date: Any
    sex: Any
    user_id: Any
    id: int
    contract_id: Any
    phone: str
    email: str
    snils: str
    type: Any


class Child(Type):
    last_name: str
    first_name: str
    middle_name: str
    birth_date: str
    sex: str
    user_id: int
    id: int
    contract_id: Any
    phone: str
    email: str
    snils: str
    type: Any
    school: School
    class_name: str
    class_level_id: int
    class_unit_id: int
    groups: List[Group]
    representatives: List[Representative]
    sections: List
    sudir_account_exists: bool
    sudir_login: Any
    is_legal_representative: bool
    parallel_curriculum_id: int
    contingent_guid: str
    enrollment_date: str


class WebFamilyProfile(Type):
    profile: Optional[Profile] = None
    children: Optional[List[Child]] = None
    hash: Optional[str] = None
