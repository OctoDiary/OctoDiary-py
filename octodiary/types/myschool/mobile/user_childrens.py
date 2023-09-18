import datetime
from ...model import Type, EveryType
from pydantic import Field
from typing import List, Any, Optional


class Contact(Type):
    data: Optional[str] = None
    type: EveryType
    is_deleted: Optional[Any] = None


class Parallel(Type):
    id: Optional[int] = None
    name: Optional[str] = None


class Class(Type):
    id: Optional[int] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    organization_id: Optional[int] = None
    open_at: Optional[datetime.datetime | datetime.date] = None
    close_at: Optional[datetime.datetime | datetime.date] = None
    parallel: Parallel


class EducationItem(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    organization_id: Optional[int] = None
    actual_from: float
    actual_to: Optional[int] = None
    training_begin_at: Optional[datetime.datetime | datetime.date] = None
    training_end_at: Optional[datetime.datetime | datetime.date] = None
    service_type: EveryType
    class_: Class = Field(..., alias='class')


class Contact1(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    actual_from: Optional[datetime.datetime | datetime.date] = None
    actual_to: Optional[datetime.datetime | datetime.date] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[datetime.datetime | datetime.date] = None
    updated_at: Optional[datetime.datetime | datetime.date] = None
    type_id: Optional[int] = None
    data: Optional[str] = None
    default: Optional[bool] = None
    type: EveryType
    validation_state_id: Optional[int] = None
    validated_at: Optional[datetime.datetime | datetime.date] = None
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
    created_at: Optional[datetime.datetime | datetime.date] = None
    updated_at: Optional[datetime.datetime | datetime.date] = None
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
    validated_at: Optional[datetime.datetime | datetime.date] = None
    data: Optional[Any] = None
    actual_from: Optional[datetime.datetime | datetime.date] = None
    actual_to: Optional[datetime.datetime | datetime.date] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[datetime.datetime | datetime.date] = None
    updated_at: Optional[datetime.datetime | datetime.date] = None
    agent_type: EveryType
    agent_person: AgentPerson1
    validation_errors: Optional[Any] = None


class AgentPerson(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    merged_to: Optional[Any] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    patronymic: Optional[str] = None
    birthdate: Optional[datetime.date] = None
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
    created_at: Optional[datetime.datetime | datetime.date] = None
    updated_at: Optional[datetime.datetime | datetime.date] = None
    addresses: Optional[Any] = None
    documents: Optional[Any] = None
    contacts: List[Contact1]
    preventions: Optional[Any] = None
    categories: Optional[Any] = None
    agents: Optional[Any] = None
    children: List[Child]
    education: Optional[Any] = None
    citizenship: Optional[Any] = None
    validation_errors: Optional[Any] = None


class Agent(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    agent_person_id: Optional[str] = None
    agent_type_id: Optional[int] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[datetime.datetime | datetime.date] = None
    data: Optional[Any] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[datetime.datetime | datetime.date] = None
    updated_at: Optional[datetime.datetime | datetime.date] = None
    agent_type: EveryType
    agent_person: AgentPerson
    validation_errors: Optional[Any] = None


class Category(Type):
    category_id: Optional[int] = None


class Entity(Type):
    id: Optional[int] = None
    obrId: Optional[int] = None
    login: Optional[Any] = None
    ssoId: Optional[Any] = None
    staffId: Optional[Any] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    lastLogged: Optional[Any] = None
    organizations: Optional[Any] = None
    source: Optional[Any] = None
    activeStudent: Optional[bool] = None
    emails: List[str]
    phones: List[str]
    active: Optional[Any] = None
    regionalStudent: Optional[bool] = None
    regionalEmploee: Optional[bool] = None
    person_id: Optional[str] = None
    contacts: List[Contact]
    education: List[EducationItem]
    agents: List[Agent]
    agent_person: Optional[Any] = None
    categories: List[Category]
    children: Optional[Any] = None
    snils: Optional[str] = None
    validation_state_id: Optional[int] = None
    date: Optional[datetime.date] = None
    birthdate: Optional[datetime.date] = None
    gender: Optional[str] = None
    created_at: Optional[datetime.datetime | datetime.date] = None
    role_group: Optional[Any] = None
    region_code: Optional[Any] = None
    actual_from: Optional[Any] = None
    actual_to: Optional[Any] = None


class UserChildrens(Type):
    page: Optional[int] = None
    size: Optional[int] = None
    totalSize: Optional[int] = None
    parentCategories: Optional[Any] = None
    entities: List[Entity]
