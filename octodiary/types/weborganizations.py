from typing import Any, List, Optional

from pydantic import Field

from .model import Type


class ConstituentEntityItem(Type):
    key: str


class Entity(Type):
    signature_date: str
    global_id: int
    system_object_id: str
    full_name: str
    short_name: str
    constituent_entity: List[ConstituentEntityItem]


class WebOrganizations(Type):
    page: Optional[int] = None
    size: Optional[int] = None
    total_size: Optional[int] = Field(None, alias='totalSize')
    parent_categories: Optional[Any] = Field(None, alias='parentCategories')
    entities: Optional[List[Entity]] = None
