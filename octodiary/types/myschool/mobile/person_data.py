from ...model import Type, EveryType
from typing import Optional, Any, List
from pydantic import Field


class Contact(Type):
    default: bool
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
    type: EveryType
    validation_state_id: Optional[int] = None
    validated_at: Optional[Any] = None
    validation_errors: Optional[Any] = None


class Organization(Type):
    global_id: Optional[int] = None
    constituent_entity_id: Optional[int] = None
    status_id: Optional[int] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None


class Class(Type):
    id: Optional[int] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    organization_id: Optional[int] = None
    building_id: Optional[int]
    staff_ids: Optional[List[int]]
    academic_year_id: Optional[int] = None
    open_at: Optional[str] = None
    close_at: Optional[str]
    parallel_id: Optional[int] = None
    education_stage_id: Optional[int] = None
    letter: Optional[Any] = None
    age_group_id: Optional[Any] = None
    data: Optional[Any] = None
    notes: Optional[Any] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[Any] = None
    parallel: EveryType
    organization: Organization


class Organization1(Type):
    global_id: Optional[int] = None
    constituent_entity_id: Optional[int] = None
    status_id: Optional[int] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None


class EducationItem(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    organization_id: Optional[int] = None
    class_uid: Optional[str] = None
    notes: Optional[Any] = None
    education_form_id: Optional[int] = None
    financing_type_id: Optional[int] = None
    service_type_id: Optional[int] = None
    deduction_reason_id: Optional[Any] = None
    training_begin_at: Optional[str] = None
    training_end_at: Optional[str] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[Any] = None
    class_: Class = Field(..., alias='class')
    education_form: EveryType
    financing_type: EveryType
    deduction_reason: Optional[Any] = None
    service_type: EveryType
    organization: Organization1


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
    documents: List
    contacts: List[Contact]
    preventions: Optional[Any] = None
    categories: Optional[Any] = None
    agents: Optional[Any] = None
    children: Optional[Any] = None
    education: List[EducationItem]
    citizenship: Optional[Any] = None
    validation_errors: Optional[Any] = None


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
    id: Optional[int] = None
    person_id: Optional[str] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[Any] = None
    actual_from: Optional[str] = None
    actual_to: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[Any] = None
    document_type_id: Optional[int] = None
    series: Optional[str] = None
    number: Optional[str] = None
    subdivision_code: Optional[Any] = None
    issuer: Optional[Any] = None
    issued: Optional[Any] = None
    expiration: Optional[Any] = None
    attachments: Optional[Any] = None
    document_type: EveryType
    validation_errors: Optional[Any] = None


class Contact(Type):
    default: bool
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
    type: EveryType
    validation_state_id: Optional[int] = None
    validated_at: Optional[Any] = None
    validation_errors: Optional[Any] = None


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
