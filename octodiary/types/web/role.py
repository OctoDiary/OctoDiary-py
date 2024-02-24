#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from pydantic import Field

from octodiary.types.model import Type


class Role(Type):
    id: int
    title: str
    global_role_tag: str = Field(..., alias="globalRoleTag")
