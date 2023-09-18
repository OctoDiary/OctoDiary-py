#    ____       _        _____  _                  
#   / __ \     | |      |  __ \(_)                 
#  | |  | | ___| |_ ___ | |  | |_  __ _ _ __ _   _ 
#  | |  | |/ __| __/ _ \| |  | | |/ _` | '__| | | |
#  | |__| | (__| || (_) | |__| | | (_| | |  | |_| |
#   \____/ \___|\__\___/|_____/|_|\__,_|_|   \__, |
#                                             __/ |
#                                            |___/ 
# 
#                 © Copyright 2023
#        🔒 Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, List, Optional

from ...model import Type


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
    mentors: Optional[List[Mentor]] = []
    ispp_account: Optional[Any] = None
    previously_profile_id: Optional[Any] = None
    student_viewed: Optional[Any] = None
    migration_date: Optional[Any] = None
    education_level: Optional[Any] = None
    class_level: Optional[Any] = None
    snils: Optional[Any] = None
    last_sign_in_at: Optional[Any] = None
    groups: Optional[List] = []
    parents: Optional[List[Parent]] = []
    marks: Optional[List] = []
    final_marks: Optional[List] = []
    attendances: Optional[List] = []
    lesson_comments: Optional[List] = []
    home_based_periods: Optional[List] = []
    subjects: Optional[List] = []
    ae_attendances: Optional[List] = []
    ec_attendances: Optional[List] = []
    assignments: Optional[List] = []
    left_on_registry: Optional[Any] = None
