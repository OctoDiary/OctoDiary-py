#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from octodiary.types.model import DT, Type


class CreateCustomEventBody(Type):
    author_id: str
    title: str
    description: Optional[str] = ""
    conference_link: Optional[str] = ""
    place: Optional[str] = ""
    start_at: Optional[DT] = ""
    finish_at: Optional[DT] = ""
    is_all_day: Optional[bool] = False
    created_at: Optional[DT] = ""
    format_type: Optional[str] = None
    format_type_id: Optional[int] = None
    outdoor: Optional[bool] = None
    place_latitude: Optional[Any] = None
    place_longitude: Optional[Any] = None
    types: Optional[Any] = None
    updated_at: Optional[DT] = ""
    id: Optional[int] = 0
