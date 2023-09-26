#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, List, Optional

from pydantic import Field

from .persondata import EveryType
from ...model import Type


class EntityContact(Type):
    data: Optional[str] = None
    type: Optional[EveryType] = None
    is_deleted: Optional[Any] = None


class Parallel(Type):
    id: Optional[int] = None
    name: Optional[str] = None


class Class(Type):
    id: Optional[int] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    organization_id: Optional[int] = None
    open_at: Optional[int] = None
    close_at: Optional[Any] = None
    parallel: Optional[Parallel] = None


class EducationItem(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    organization_id: Optional[int] = None
    actual_from: Optional[float] = None
    actual_to: Optional[float] = None
    training_begin_at: Optional[str] = None
    training_end_at: Optional[str] = None
    service_type: Optional[EveryType] = None
    class_: Class = Field(..., alias='class')


class Category(Type):
    category_id: Optional[int] = None


class Contact(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[Any] = None
    type_id: Optional[int] = None
    data: Optional[str] = None
    default: Optional[bool] = None
    type: Optional[Type] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[Any] = None
    validation_errors: Optional[Any] = None


class AgentPerson1(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    merged_to: Optional[Any] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    patronymic: Optional[str] = None
    birthdate: Optional[str] = None
    birthplace: Optional[Any] = None
    snils: Optional[str] = None
    gender_id: Optional[int] = None
    citizenship_id: Optional[Any] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[Any] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[Any] = None
    addresses: Optional[Any] = None
    documents: Optional[Any] = None
    contacts: Optional[Any] = None
    preventions: Optional[Any] = None
    categories: Optional[Any] = None
    agents: Optional[Any] = None
    children: Optional[Any] = None
    education: Optional[Any] = None
    citizenship: Optional[Any] = None
    validation_errors: Optional[Any] = None


class Child(Type):
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
    agent_person: Optional[AgentPerson1] = None
    validation_errors: Optional[Any] = None


class AgentPerson(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    merged_to: Optional[Any] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    patronymic: Optional[str] = None
    birthdate: Optional[str] = None
    birthplace: Optional[Any] = None
    snils: Optional[str] = None
    gender_id: Optional[int] = None
    citizenship_id: Optional[Any] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[Any] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[Any] = None
    addresses: Optional[Any] = None
    documents: Optional[Any] = None
    contacts: Optional[List[Contact]] = []
    preventions: Optional[Any] = None
    categories: Optional[Any] = None
    agents: Optional[Any] = None
    children: Optional[List[Child]] = []
    education: Optional[Any] = None
    citizenship: Optional[Any] = None
    validation_errors: Optional[Any] = None


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
    id: Optional[int] = None
    obr_id: int = Field(..., alias='obrId')
    login: Optional[Any] = None
    sso_id: Any = Field(..., alias='ssoId')
    staff_id: Any = Field(..., alias='staffId')
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    last_logged: Any = Field(..., alias='lastLogged')
    organizations: Optional[Any] = None
    source: Optional[Any] = None
    active_student: bool = Field(..., alias='activeStudent')
    emails: Optional[List[str]] = None
    phones: Optional[List[str]] = None
    active: Optional[Any] = None
    regional_student: bool = Field(..., alias='regionalStudent')
    regional_emploee: bool = Field(..., alias='regionalEmploee')
    person_id: Optional[str] = None
    contacts: Optional[List[EntityContact]] = None
    education: Optional[List[EducationItem]] = None
    agents: Optional[List[Agent]] = None
    agent_person: Optional[Any] = None
    categories: Optional[List[Category]] = None
    children: Optional[Any] = None
    snils: Optional[str] = None
    validation_state_id: Optional[int] = None
    date: Optional[Any] = None
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    created_at: Optional[str] = None
    role_group: Optional[Any] = None
    region_code: Optional[Any] = None
    actual_from: Optional[Any] = None
    actual_to: Optional[Any] = None


class UserChildren(Type):
    page: Optional[int] = None
    size: Optional[int] = None
    total_size: Optional[int] = Field(None, alias='totalSize')
    parent_categories: Optional[Any] = Field(None, alias='parentCategories')
    entities: Optional[List[Entity]] = None
