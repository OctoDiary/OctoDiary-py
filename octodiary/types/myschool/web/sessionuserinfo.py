#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from datetime import date
from typing import Optional

from octodiary.types.model import Type


class Profile(Type):
    id: Optional[int] = None
    type: Optional[str] = None
    roles: Optional[list] = []
    user_id: Optional[int] = None
    agree_pers_data: Optional[bool] = None
    subject_ids: Optional[list] = []


class SessionUserInfo(Type):
    id: Optional[int] = None
    email: Optional[str] = None
    snils: Optional[str] = None
    profiles: Optional[list[Profile]] = []
    guid: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    phone_number: Optional[str] = None
    authentication_token: Optional[str] = None
    person_id: Optional[str] = None
    password_change_required: Optional[bool] = None
    regional_auth: Optional[str] = None
    sex: Optional[str] = None
    date_of_birth: Optional[date] = None
