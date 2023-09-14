from typing import Any, List, Optional

from pydantic import Field

from ...model import Type
from .persondata import EveryType


class EntityContact(Type):
    data: str
    type: EveryType
    is_deleted: Any


class Parallel(Type):
    id: int
    name: str


class Class(Type):
    id: int
    uid: str
    name: str
    organization_id: int
    open_at: int
    close_at: Any
    parallel: Parallel


class EducationItem(Type):
    id: int
    person_id: str
    organization_id: int
    actual_from: float
    actual_to: float
    training_begin_at: str
    training_end_at: str
    service_type: EveryType
    class_: Class = Field(..., alias='class')


class Category(Type):
    category_id: int


class Contact(Type):
    id: int
    person_id: str
    actual_from: str
    actual_to: str
    created_by: str
    updated_by: Any
    created_at: str
    updated_at: Any
    type_id: int
    data: str
    default: bool
    type: Type
    validation_state_id: int
    validated_at: Any
    validation_errors: Any


class AgentPerson1(Type):
    id: int
    person_id: str
    merged_to: Any
    lastname: str
    firstname: str
    patronymic: str
    birthdate: str
    birthplace: Any
    snils: str
    gender_id: int
    citizenship_id: Any
    validation_state_id: int
    validated_at: Any
    actual_from: str
    actual_to: str
    created_by: str
    updated_by: Any
    created_at: str
    updated_at: Any
    addresses: Any
    documents: Any
    contacts: Any
    preventions: Any
    categories: Any
    agents: Any
    children: Any
    education: Any
    citizenship: Any
    validation_errors: Any


class Child(Type):
    id: int
    person_id: str
    agent_person_id: str
    agent_type_id: int
    validation_state_id: int
    validated_at: Any
    data: Any
    actual_from: str
    actual_to: str
    created_by: str
    updated_by: Any
    created_at: str
    updated_at: Any
    agent_type: EveryType
    agent_person: AgentPerson1
    validation_errors: Any


class AgentPerson(Type):
    id: int
    person_id: str
    merged_to: Any
    lastname: str
    firstname: str
    patronymic: str
    birthdate: str
    birthplace: Any
    snils: str
    gender_id: int
    citizenship_id: Any
    validation_state_id: int
    validated_at: Any
    actual_from: str
    actual_to: str
    created_by: str
    updated_by: Any
    created_at: str
    updated_at: Any
    addresses: Any
    documents: Any
    contacts: List[Contact]
    preventions: Any
    categories: Any
    agents: Any
    children: List[Child]
    education: Any
    citizenship: Any
    validation_errors: Any


class Agent(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    agent_person_id: Optional[str] = None
    agent_type_id: Optional[int] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[Any] = None
    data: Optional[Any] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[Any] = None
    agent_type: Optional[EveryType] = None
    agent_person: Optional[AgentPerson] = None
    validation_errors: Optional[Any] = None


class Entity(Type):
    id: int
    obr_id: int = Field(..., alias='obrId')
    login: Any
    sso_id: Any = Field(..., alias='ssoId')
    staff_id: Any = Field(..., alias='staffId')
    firstname: str
    lastname: str
    patronymic: str
    last_logged: Any = Field(..., alias='lastLogged')
    organizations: Any
    source: Any
    active_student: bool = Field(..., alias='activeStudent')
    emails: List[str]
    phones: List[str]
    active: Any
    regional_student: bool = Field(..., alias='regionalStudent')
    regional_emploee: bool = Field(..., alias='regionalEmploee')
    person_id: str
    contacts: List[EntityContact]
    education: List[EducationItem]
    agents: List[Agent]
    agent_person: Any
    categories: List[Category]
    children: Any
    snils: str
    validation_state_id: int
    date: Any
    birthdate: str
    gender: str
    created_at: str
    role_group: Any
    region_code: Any
    actual_from: Any
    actual_to: Any


class UserChildrens(Type):
    page: Optional[int] = None
    size: Optional[int] = None
    total_size: Optional[int] = Field(None, alias='totalSize')
    parent_categories: Optional[Any] = Field(None, alias='parentCategories')
    entities: Optional[List[Entity]] = None
