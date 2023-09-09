from .model import Type
from typing import Any, List, Optional
from pydantic import Field

class Info(Type):
    birthdate: str
    mail: Any
    gender: str
    trusted: bool
    first_name: str = Field(..., alias='FirstName')
    mobile: Any
    guid: str
    failed: bool
    last_name: str = Field(..., alias='LastName')
    error: Any
    middle_name: str = Field(..., alias='MiddleName')
    snils: str


class Subsystem(Type):
    id: int
    title: str
    url: str
    mnemonic: str
    description: str
    is_mobile: bool
    sort_order: int


class Role(Type):
    id: int
    title: str
    subsystems: List[Subsystem]


class UserInfo(Type):
    user_id: Optional[int] = Field(None, alias='userId')
    is_ad_activated: Optional[bool] = Field(None, alias='isAdActivated')
    info: Optional[Info] = None
    roles: Optional[List[Role]] = None
    saved_choice: Optional[Any] = Field(None, alias='savedChoice')
    notification: Optional[bool] = None
    login: Optional[str] = None
