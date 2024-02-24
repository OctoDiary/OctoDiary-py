#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from pydantic import Field

from octodiary.types.model import EveryType, Type, DT


class Address1(Type):
    id: Optional[int] = None
    address: Optional[str] = None
    fias_id: Optional[str] = None
    unom: Optional[int] = None
    flat: Optional[str] = None
    global_id: Optional[int] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[DT] = None
    validation_errors: Optional[Any] = None


class Address(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    address_id: Optional[int] = None
    address_type_id: Optional[int] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[DT] = None
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    address: Address1 | None = None
    address_type: EveryType | None = None
    validation_errors: Optional[Any] = None


class Attachment(Type):
    id: Optional[str] = None
    name: Optional[str] = None
    uploaded_at: Optional[str] = None


class Document(Type):
    id: Optional[int] = None
    person_id: Optional[str] = None
    validation_state_id: Optional[int] = None
    validated_at: Optional[DT] = None
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    document_type_id: Optional[int] = None
    series: Optional[str] = None
    number: Optional[str] = None
    subdivision_code: Optional[str] = None
    issuer: Optional[str] = None
    issued: Optional[str] = None
    expiration: Optional[Any] = None
    attachments: list[Attachment] | None = None
    document_type: EveryType | None = None
    validation_errors: Optional[Any] = None


class Organization(Type):
    global_id: Optional[int] = None
    constituent_entity_id: Optional[int] = None
    status_id: Optional[int] = None
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None


class Class(Type):
    id: Optional[int] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    organization_id: Optional[int] = None
    building_id: Optional[int] = None
    staff_ids: list[int] | None = None
    academic_year_id: Optional[int] = None
    open_at: Optional[DT] = None
    close_at: Optional[DT] = None
    parallel_id: Optional[int] = None
    education_stage_id: Optional[int] = None
    letter: Optional[str] = None
    age_group_id: Optional[int] = None
    data: Optional[Any] = None
    notes: Optional[Any] = None
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    parallel: EveryType | None = None
    organization: Organization | None = None


class Education(Type):
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
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    class_: Class | None = Field(None, alias="class")
    education_form: EveryType | None = None
    financing_type: EveryType | None = None
    deduction_reason: Optional[Any] = None
    service_type: EveryType | None = None
    organization: Organization | None = None


class PersonData(Type):
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
    actual_from: Optional[DT] = None
    actual_to: Optional[DT] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    addresses: list[Address] | None = None
    documents: list[Document] | None = None
    contacts: Optional[Any] = None
    preventions: Optional[Any] = None
    categories: Optional[Any] = None
    agents: Optional[Any] = None
    children: Optional[Any] = None
    education: list[Education] | None = None
    citizenship: Optional[Any] = None
    validation_errors: Optional[Any] = None
