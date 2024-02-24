#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from pydantic import Field

from octodiary.types.model import DT, Type


class Visit(Type):
    in_: Optional[str] = Field(None, alias="in")
    out: Optional[str] = None
    duration: Optional[str] = None
    address: Optional[str] = None
    type: Optional[str] = None
    is_warning: Optional[bool] = None
    short_name: Optional[str] = None


class Payload(Type):
    date: Optional[DT] = None
    visits: list[Visit] | None = None


class Visits(Type):
    payload: list[Payload] | None = None
