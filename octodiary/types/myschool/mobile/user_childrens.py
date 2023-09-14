from ...model import Type, EveryType
from pydantic import Field
from typing import List, Any


class Contact(Type):
    data: str
    type: Type
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
    actual_to: int
    training_begin_at: str
    training_end_at: str
    service_type: EveryType
    class_: Class = Field(..., alias='class')


class Contact1(Type):
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
    type: EveryType
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
    contacts: List[Contact1]
    preventions: Any
    categories: Any
    agents: Any
    children: List[Child]
    education: Any
    citizenship: Any
    validation_errors: Any


class Agent(Type):
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
    agent_person: AgentPerson
    validation_errors: Any


class Category(Type):
    category_id: int


class Entity(Type):
    id: int
    obrId: int
    login: Any
    ssoId: Any
    staffId: Any
    firstname: str
    lastname: str
    patronymic: str
    lastLogged: Any
    organizations: Any
    source: Any
    activeStudent: bool
    emails: List[str]
    phones: List[str]
    active: Any
    regionalStudent: bool
    regionalEmploee: bool
    person_id: str
    contacts: List[Contact]
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
    page: int
    size: int
    totalSize: int
    parentCategories: Any
    entities: List[Entity]
