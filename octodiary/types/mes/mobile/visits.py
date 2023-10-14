#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from pydantic import Field

from octodiary.types.model import Type


class Visit(Type):
    in_: str | None = Field(None, alias="in")
    out: str | None = None
    duration: str | None = None
    address: str | None = None
    type: str | None = None
    is_warning: bool | None = None
    short_name: str | None = None


class Payload(Type):
    date: str | None = None
    visits: list[Visit] | None = None


class Visits(Type):
    payload: list[Payload] | None = None
