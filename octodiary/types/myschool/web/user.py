from ...model import Type
from typing import List, Any
from pydantic import Field


class Profile(Type):
    id: int
    type: str
    roles: List
    user_id: int
    children_profile_ids: List[int]


class User(Type):
    id: int
    email: str
    sex: str
    password: Any
    locked: bool
    temporary_locked: bool = Field(..., alias='temporaryLocked')
    full_count: int = Field(..., alias='fullCount')
    sessions_count: int = Field(..., alias='sessionsCount')
    updated_at: Any = Field(..., alias='updatedAt')
    profiles: List[Profile]
    captcha: Any
    hidden: bool
    gusoev_login: str
    first_name: str
    last_name: str
    middle_name: str
    date_of_birth: str
    phone_number: str
    mrko_user_id: Any
    sms_notify_message: Any
    email_notify_message: Any
    ekis_key: Any
    change_password_required: Any
    snils: str
    guid: Any
    is_hidden: bool
    locked_by_user_id: int
    lock_datetime: Any
    phone_number_ezd: str
    email_ezd: Any
    last_sign_in_at: Any
