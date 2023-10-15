#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any

from pydantic import Field

from octodiary.types.model import EveryType, Type


class Address1(Type):
    id: int | None = None
    address: str | None = None
    fias_id: str | None = None
    unom: int | None = None
    flat: str | None = None
    global_id: int | None = None
    validation_state_id: int | None = None
    validated_at: Any | None = None
    validation_errors: Any | None = None


class Address(Type):
    id: int | None = None
    person_id: str | None = None
    address_id: int | None = None
    address_type_id: int | None = None
    validation_state_id: int | None = None
    validated_at: Any | None = None
    actual_from: str | None = None
    actual_to: str | None = None
    created_by: str | None = None
    updated_by: Any | None = None
    created_at: str | None = None
    updated_at: Any | None = None
    address: Address1 | None = None
    address_type: EveryType | None = None
    validation_errors: Any | None = None


class Attachment(Type):
    id: str | None = None
    name: str | None = None
    uploaded_at: str | None = None


class Document(Type):
    id: int | None = None
    person_id: str | None = None
    validation_state_id: int | None = None
    validated_at: Any | None = None
    actual_from: str | None = None
    actual_to: str | None = None
    created_by: str | None = None
    updated_by: Any | None = None
    created_at: str | None = None
    updated_at: Any | None = None
    document_type_id: int | None = None
    series: str | None = None
    number: str | None = None
    subdivision_code: str | None = None
    issuer: str | None = None
    issued: str | None = None
    expiration: Any | None = None
    attachments: list[Attachment] | None = None
    document_type: EveryType | None = None
    validation_errors: Any | None = None


class Organization(Type):
    global_id: int | None = None
    constituent_entity_id: int | None = None
    status_id: int | None = None
    actual_from: str | None = None
    actual_to: str | None = None


class Class(Type):
    id: int | None = None
    uid: str | None = None
    name: str | None = None
    organization_id: int | None = None
    building_id: int | None = None
    staff_ids: list[int] | None = None
    academic_year_id: int | None = None
    open_at: str | None = None
    close_at: Any | None = None
    parallel_id: int | None = None
    education_stage_id: int | None = None
    letter: str | None = None
    age_group_id: Any | None = None
    data: Any | None = None
    notes: Any | None = None
    actual_from: str | None = None
    actual_to: str | None = None
    created_by: str | None = None
    updated_by: Any | None = None
    created_at: str | None = None
    updated_at: Any | None = None
    parallel: EveryType | None = None
    organization: Organization | None = None


class Education(Type):
    id: int | None = None
    person_id: str | None = None
    organization_id: int | None = None
    class_uid: str | None = None
    notes: Any | None = None
    education_form_id: int | None = None
    financing_type_id: int | None = None
    service_type_id: int | None = None
    deduction_reason_id: Any | None = None
    training_begin_at: str | None = None
    training_end_at: str | None = None
    actual_from: str | None = None
    actual_to: str | None = None
    created_by: str | None = None
    updated_by: Any | None = None
    created_at: str | None = None
    updated_at: Any | None = None
    class_: Class | None = Field(None, alias="class")
    education_form: EveryType | None = None
    financing_type: EveryType | None = None
    deduction_reason: Any | None = None
    service_type: EveryType | None = None
    organization: Organization | None = None


class PersonData(Type):
    id: int | None = None
    person_id: str | None = None
    merged_to: Any | None = None
    lastname: str | None = None
    firstname: str | None = None
    patronymic: str | None = None
    birthdate: str | None = None
    birthplace: str | None = None
    snils: str | None = None
    gender_id: int | None = None
    citizenship_id: int | None = None
    validation_state_id: int | None = None
    validated_at: Any | None = None
    actual_from: str | None = None
    actual_to: str | None = None
    created_by: str | None = None
    updated_by: Any | None = None
    created_at: str | None = None
    updated_at: Any | None = None
    addresses: list[Address] | None = None
    documents: list[Document] | None = None
    contacts: Any | None = None
    preventions: Any | None = None
    categories: Any | None = None
    agents: Any | None = None
    children: Any | None = None
    education: list[Education] | None = None
    citizenship: Any | None = None
    validation_errors: Any | None = None
