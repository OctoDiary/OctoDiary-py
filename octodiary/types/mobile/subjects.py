#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

from octodiary.types.model import Type


class Payload(Type):
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None


class Subjects(Type):
    payload: list[Payload] | None = None
