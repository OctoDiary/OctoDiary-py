from typing import Any, List

from ...model import Type


class ClassUnit(Type):
    id: int
    class_level_id: int
    name: str
    home_based: bool


class Curricula(Type):
    id: int
    name: str
    class_level_id: Any


class Mentor(Type):
    id: int
    name: str


class Parent(Type):
    id: int
    user_id: int
    type: str
    gusoev_login: str
    name: str
    phone_number_ezd: Any
    email_ezd: Any
    phone_number: str
    email: str
    snils: Any
    last_sign_in_at: Any
    hidden: bool


class StudentProfile(Type):
    id: int
    created_at: str
    updated_at: str
    deleted_at: Any
    person_id: str
    transferred: bool
    school_id: int
    user_id: int
    study_mode_id: int
    user_name: str
    short_name: str
    last_name: Any
    first_name: Any
    middle_name: Any
    change_password_required: bool
    birth_date: str
    enlisted_on: Any
    gusoev_login: str
    age: int
    sex: str
    deleted: bool
    email: Any
    phone_number: Any
    email_ezd: Any
    phone_number_ezd: Any
    class_unit: ClassUnit
    previously_class_unit: Any
    curricula: Curricula
    non_attendance: int
    mentors: List[Mentor]
    ispp_account: Any
    previously_profile_id: Any
    student_viewed: Any
    migration_date: Any
    education_level: Any
    class_level: Any
    snils: Any
    last_sign_in_at: Any
    groups: List
    parents: List[Parent]
    marks: List
    final_marks: List
    attendances: List
    lesson_comments: List
    home_based_periods: List
    subjects: List
    ae_attendances: List
    ec_attendances: List
    assignments: List
    left_on_registry: Any
