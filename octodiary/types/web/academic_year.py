#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import DT, Type


class AcademicYear(Type):
    id: Optional[int] = None
    name: Optional[str] = None
    begin_date: Optional[DT] = None
    end_date: Optional[DT] = None
    calendar_id: Optional[int] = None
    current_year: Optional[bool] = None
