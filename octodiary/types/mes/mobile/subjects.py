#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from octodiary.types.model import Type


class Payload(Type):
    subject_id: int | None = None
    subject_name: str | None = None


class Subjects(Type):
    payload: list[Payload] | None = None
