#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from pydantic import Field

from octodiary.types.model import Type


class Profile(Type):
    id: Optional[int] = None
    type: Optional[str] = None
    roles: Optional[list] = []
    user_id: Optional[int] = None
    children_profile_ids: Optional[list[int]] = []


class User(Type):
    id: Optional[int] = None
    email: Optional[str] = None
    sex: Optional[str] = None
    password: Optional[Any] = None
    locked: Optional[bool] = None
    temporary_locked: bool = Field(..., alias="temporaryLocked")
    full_count: int = Field(..., alias="fullCount")
    sessions_count: int = Field(..., alias="sessionsCount")
    updated_at: Any = Field(..., alias="updatedAt")
    profiles: Optional[list[Profile]] = []
    captcha: Optional[Any] = None
    hidden: Optional[bool] = None
    gusoev_login: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    phone_number: Optional[str] = None
    mrko_user_id: Optional[Any] = None
    sms_notify_message: Optional[Any] = None
    email_notify_message: Optional[Any] = None
    ekis_key: Optional[Any] = None
    change_password_required: Optional[Any] = None
    snils: Optional[str] = None
    guid: Optional[Any] = None
    is_hidden: Optional[bool] = None
    locked_by_user_id: Optional[int] = None
    lock_datetime: Optional[Any] = None
    phone_number_ezd: Optional[str] = None
    email_ezd: Optional[Any] = None
    last_sign_in_at: Optional[Any] = None
