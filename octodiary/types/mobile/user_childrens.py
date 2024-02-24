#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from pydantic import Field

from octodiary.types.model import DT, EveryType, Type


class Contact(Type):
    data: Optional[str] = None
    type: EveryType
    is_deleted: Optional[bool] = None


class Parallel(Type):
    id: Optional[int] = None
    name: Optional[str] = None


class Class(Type):
    id: Optional[int] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    organization_id: Optional[int] = None
    open_at: Optional[DT] = None
    close_at: Optional[DT] = None
    parallel: Parallel


class EducationItem(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    organization_id: Optional[int] = None
    actual_from: float
    actual_to: Optional[int] = None
    training_begin_at: Optional[DT] = None
    training_end_at: Optional[DT] = None
    service_type: EveryType
    class_: Class = Field(..., alias="class")


class Contact1(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    type_id: Optional[int] = None
    data: Optional[str] = None
    default: Optional[bool] = None
    type: EveryType
    validation_state_id: Optional[int] = None
    validated_at: Optional[DT] = None
    validation_errors: Optional[Any] = None


class Child(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    agent_person_id: Optional[str] = None
    agent_type_id: Optional[int] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[DT] = None
    data: Optional[str] = None
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    agent_type: EveryType
    agent_person: "AgentPerson"
    validation_errors: Optional[Any] = None


class AgentPerson(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    merged_to: Optional[Any] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    patronymic: Optional[str] = None
    birthdate: Optional[DT] = None
    birthplace: Optional[str] = None
    snils: Optional[str] = None
    gender_id: Optional[int] = None
    citizenship_id: Optional[int] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[DT] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    addresses: Optional[Any] = None
    documents: Optional[Any] = None
    contacts: list[Contact1]
    preventions: Optional[Any] = None
    categories: Optional[Any] = None
    agents: Optional[Any] = None
    children: list[Child]
    education: Optional[Any] = None
    citizenship: Optional[Any] = None
    validation_errors: Optional[Any] = None


class Agent(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    agent_person_id: Optional[str] = None
    agent_type_id: Optional[int] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[DT] = None
    data: Optional[str] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    agent_type: EveryType
    agent_person: AgentPerson
    validation_errors: Optional[Any] = None


class Category(Type):
    category_id: Optional[int] = None


class Entity(Type):
    id: Optional[int] = None
    obrId: Optional[int] = None
    login: Optional[str] = None
    ssoId: Optional[int] = None
    staffId: Optional[int] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    lastLogged: Optional[DT] = None
    organizations: Optional[Any] = None
    source: Optional[Any] = None
    activeStudent: Optional[bool] = None
    emails: list[str]
    phones: list[str]
    active: Optional[Any] = None
    regionalStudent: Optional[bool] = None
    regionalEmploee: Optional[bool] = None
    person_id: Optional[str] = None
    contacts: list[Contact]
    education: list[EducationItem]
    agents: list[Agent]
    agent_person: Optional[AgentPerson] = None
    categories: list[Category]
    children: Optional[list[Agent]] = None
    snils: Optional[str] = None
    validation_state_id: Optional[int] = None
    date: Optional[DT] = None
    birthdate: Optional[DT] = None
    gender: Optional[str] = None
    created_at: Optional[DT] = None
    role_group: Optional[str] = None
    region_code: Optional[Any] = None
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None


class UserChildrens(Type):
    page: Optional[int] = None
    size: Optional[int] = None
    totalSize: Optional[int] = None
    parentCategories: Optional[Any] = None
    entities: list[Entity]
