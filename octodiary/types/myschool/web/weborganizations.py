#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, List, Optional

from pydantic import Field

from ...model import Type


class ConstituentEntityItem(Type):
    key: str


class Entity(Type):
    signature_date: Optional[str] = None
    global_id: Optional[int] = None
    system_object_id: Optional[str] = None
    full_name: Optional[str] = None
    short_name: Optional[str] = None
    constituent_entity: List[ConstituentEntityItem]


class WebOrganizations(Type):
    page: Optional[int] = None
    size: Optional[int] = None
    total_size: Optional[int] = Field(None, alias='totalSize')
    parent_categories: Optional[Any] = Field(None, alias='parentCategories')
    entities: Optional[List[Entity]] = None
