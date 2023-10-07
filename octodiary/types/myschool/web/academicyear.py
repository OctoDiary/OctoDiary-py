#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import Type


class AcademicYear(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    begin_date: Optional[str] = None
    end_date: Optional[str] = None
    calendar_id: Optional[int] = None
    current_year: Optional[bool] = None
