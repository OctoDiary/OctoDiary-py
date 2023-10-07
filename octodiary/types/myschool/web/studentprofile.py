#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import Type


class ClassUnit(Type):
    id: Optional[int] = None
    class_level_id: Optional[int] = None
    name: Optional[str] = None
    home_based: Optional[bool] = None


class Curricula(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    class_level_id: Optional[Any] = None


class Mentor(Type):
    id: Optional[int] = None
    name: Optional[str] = None


class Parent(Type):
    id: Optional[int] = None
    user_id: Optional[int] = None
    type: Optional[str] = None
    gusoev_login: Optional[str] = None
    name: Optional[str] = None
    phone_number_ezd: Optional[Any] = None
    email_ezd: Optional[Any] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    snils: Optional[Any] = None
    last_sign_in_at: Optional[Any] = None
    hidden: Optional[bool] = None


class StudentProfile(Type):
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    deleted_at: Optional[Any] = None
    person_id: Optional[str] = None
    transferred: Optional[bool] = None
    school_id: Optional[int] = None
    user_id: Optional[int] = None
    study_mode_id: Optional[int] = None
    user_name: Optional[str] = None
    short_name: Optional[str] = None
    last_name: Optional[Any] = None
    first_name: Optional[Any] = None
    middle_name: Optional[Any] = None
    change_password_required: Optional[bool] = None
    birth_date: Optional[str] = None
    enlisted_on: Optional[Any] = None
    gusoev_login: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    deleted: Optional[bool] = None
    email: Optional[Any] = None
    phone_number: Optional[Any] = None
    email_ezd: Optional[Any] = None
    phone_number_ezd: Optional[Any] = None
    class_unit: Optional[ClassUnit] = None
    previously_class_unit: Optional[Any] = None
    curricula: Optional[Curricula] = None
    non_attendance: Optional[int] = None
    mentors: Optional[list[Mentor]] = []
    ispp_account: Optional[Any] = None
    previously_profile_id: Optional[Any] = None
    student_viewed: Optional[Any] = None
    migration_date: Optional[Any] = None
    education_level: Optional[Any] = None
    class_level: Optional[Any] = None
    snils: Optional[Any] = None
    last_sign_in_at: Optional[Any] = None
    groups: Optional[list] = []
    parents: Optional[list[Parent]] = []
    marks: Optional[list] = []
    final_marks: Optional[list] = []
    attendances: Optional[list] = []
    lesson_comments: Optional[list] = []
    home_based_periods: Optional[list] = []
    subjects: Optional[list] = []
    ae_attendances: Optional[list] = []
    ec_attendances: Optional[list] = []
    assignments: Optional[list] = []
    left_on_registry: Optional[Any] = None
