from datetime import date
from typing import List, Optional

from ...model import Type


class Profile(Type):
    id: int
    type: str
    roles: List
    user_id: int
    agree_pers_data: bool
    subject_ids: List


class SessionUserInfo(Type):
    id: Optional[int] = None
    email: Optional[str] = None
    snils: Optional[str] = None
    profiles: Optional[List[Profile]] = None
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
