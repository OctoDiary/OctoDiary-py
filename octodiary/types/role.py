from pydantic import Field

from .model import Type


class Role(Type):
    id: int
    title: str
    global_role_tag: str = Field(..., alias='globalRoleTag')
