from .model import Type
from typing import List, Any, Optional
from pydantic import Field
from datetime import datetime


class EveryType(Type):
    id: int
    name: str
    actual_from: datetime
    actual_to: datetime


class Contact(Type):
    default: bool
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
    type: EveryType
    validation_state_id: int
    validated_at: Any
    validation_errors: Any


class Organization(Type):
    global_id: int
    constituent_entity_id: int
    status_id: int
    actual_from: str
    actual_to: str


class Class(Type):
    id: int
    uid: str
    name: str
    organization_id: int
    building_id: Optional[int]
    staff_ids: Optional[List[int]]
    academic_year_id: int
    open_at: str
    close_at: Optional[str]
    parallel_id: int
    education_stage_id: int
    letter: Any
    age_group_id: Any
    data: Any
    notes: Any
    actual_from: str
    actual_to: str
    created_by: str
    updated_by: Any
    created_at: str
    updated_at: Any
    parallel: EveryType
    organization: Organization


class Organization1(Type):
    global_id: int
    constituent_entity_id: int
    status_id: int
    actual_from: str
    actual_to: str


class EducationItem(Type):
    id: int
    person_id: str
    organization_id: int
    class_uid: str
    notes: Any
    education_form_id: int
    financing_type_id: int
    service_type_id: int
    deduction_reason_id: Any
    training_begin_at: str
    training_end_at: str
    actual_from: str
    actual_to: str
    created_by: str
    updated_by: Any
    created_at: str
    updated_at: Any
    class_: Class = Field(..., alias='class')
    education_form: EveryType
    financing_type: EveryType
    deduction_reason: Any
    service_type: EveryType
    organization: Organization1


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
    documents: List
    contacts: List[Contact]
    preventions: Any
    categories: Any
    agents: Any
    children: Any
    education: List[EducationItem]
    citizenship: Any
    validation_errors: Any


class Children(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    agent_person_id: Optional[str] = None
    agent_type_id: Optional[int] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[Any] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[Any] = None
    agent_type: Optional[EveryType] = None
    agent_person: Optional[AgentPerson] = None
    validation_errors: Optional[Any] = None


class Document(Type):
    id: int
    person_id: str
    validation_state_id: int
    validated_at: Any
    actual_from: str
    actual_to: str
    created_by: str
    updated_by: Any
    created_at: str
    updated_at: Any
    document_type_id: int
    series: str
    number: str
    subdivision_code: Any
    issuer: Any
    issued: Any
    expiration: Any
    attachments: Any
    document_type: EveryType
    validation_errors: Any


class PersonData(Type):
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
    documents: Optional[List[Document]] = None
    contacts: Optional[List[Contact]] = None
    preventions: Optional[Any] = None
    categories: Optional[Any] = None
    agents: Optional[Any] = None
    children: Optional[List[Children]] = None
    education: Optional[Any] = None
    citizenship: Optional[Any] = None
    validation_errors: Optional[Any] = None
