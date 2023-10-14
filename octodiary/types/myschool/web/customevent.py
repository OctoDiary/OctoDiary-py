#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import Type


class CreateCustomEventBody(Type):
    author_id: str
    title: str
    description: Optional[str] = ""
    conference_link: Optional[str] = ""
    place: Optional[str] = ""
    start_at: Optional[str] = None
    finish_at: str
    is_all_day: Optional[bool] = False
    created_at: Optional[str] = ""
    format_type: Optional[Any] = None
    format_type_id: Optional[Any] = None
    outdoor: Optional[Any] = None
    place_latitude: Optional[Any] = None
    place_longitude: Optional[Any] = None
    types: Optional[Any] = None
    updated_at: Optional[str] = ""
    id: Optional[int] = 0
