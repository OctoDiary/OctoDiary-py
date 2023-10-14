#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any

from pydantic import Field

from octodiary.types.model import Type


class Material(Type):
    count_execute: int | None = None
    count_learn: int | None = None


class Entry(Type):
    homework_entry_id: int | None = None
    date_assigned_on: str | None = None
    date_prepared_for: str | None = None
    description: str | None = None
    duration: int | None = None
    materials: str | None = None
    attachment_ids: list | None = None
    attachments: list | None = None
    student_ids: None = None


class Homework(Type):
    presence_status_id: int | None = None
    total_count: int | None = None
    execute_count: int | None = None
    descriptions: list[str] | None = None
    link_types: None = None
    materials: Material | None = None
    entries: list[Entry] | None = None


class LearningTargets(Type):
    for_lesson: bool | None = Field(None, alias="forLesson")
    for_home: bool | None = Field(None, alias="forHome")


class Material1(Type):
    uuid: str | None = None
    learning_targets: LearningTargets | None = Field(None, alias="learningTargets")
    is_hidden_from_students: bool | None = Field(None, alias="isHiddenFromStudents")


class Criterion(Type):
    name: str | None = None
    value: str | None = None


class Grade(Type):
    five: float | None = None
    hundred: float | None = None
    origin: str | None = None


class Value(Type):
    name: str | None = None
    grade_system_id: int | None = None
    grade_system_type: str | None = None
    nmax: float | None = None
    grade: Grade | None = None


class Mark(Type):
    id: int | None = None
    comment: str | None = None
    comment_exists: bool | None = None
    control_form_name: str | None = None
    is_exam: bool | None = None
    is_point: bool | None = None
    point_date: None = None
    original_grade_system_type: str | None = None
    criteria: list[Criterion] | None = None
    value: str | None = None
    values: list[Value] | None = None
    weight: int | None = None


class Response(Type):
    id: int | None = None
    author_id: str | None = None
    title: str | None = None
    description: None = None
    start_at: str | None = None
    finish_at: str | None = None
    is_all_day: bool | None = None
    conference_link: None = None
    outdoor: bool | None = None
    place: None = None
    place_latitude: None = None
    place_longitude: None = None
    created_at: str | None = None
    updated_at: str | None = None
    types: list[Any] | None = None
    author_name: None = None
    registration_start_at: None = None
    registration_end_at: None = None
    source: str | None = None
    source_id: str | None = None
    place_name: None = None
    contact_name: None = None
    contact_phone: None = None
    contact_email: None = None
    comment: None = None
    need_document: None = None
    type: None = None
    format_name: None = None
    url: None = None
    subject_id: int | None = None
    subject_name: str | None = None
    room_name: str | None = None
    room_number: str | None = None
    replaced: bool | None = None
    replaced_teacher_id: int | None = None
    esz_field_id: int | None = None
    lesson_type: str | None = None
    course_lesson_type: None = None
    lesson_education_type: None = None
    lesson_name: str | None = None
    lesson_theme: str | None = None
    activities: None = None
    link_to_join: None = None
    control: None = None
    class_unit_ids: list[int] | None = None
    class_unit_name: str | None = None
    group_id: int | None = None
    group_name: str | None = None
    external_activities_type: None = None
    address: None = None
    place_comment: None = None
    building_id: int | None = None
    building_name: str | None = None
    city_building_name: None = None
    cancelled: bool | None = None
    is_missed_lesson: bool | None = None
    is_metagroup: None = None
    absence_reason_id: int | None = None
    nonattendance_reason_id: int | None = None
    visible_fake_group: None = None
    health_status: None = None
    student_count: None = None
    attendances: None = None
    journal_fill: bool | None = None
    comment_count: None = None
    comments: None = None
    homework: Homework | None = None
    materials: list[Material1] | None = None
    marks: list[Mark] | None = None


class EventsResponse(Type):
    total_count: int | None = None
    response: list[Response] | None = None
    errors: None = None
