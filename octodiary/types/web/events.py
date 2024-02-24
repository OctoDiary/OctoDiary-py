#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, Optional

from pydantic import Field

from octodiary.types.model import DT, Type


class Material(Type):
    count_execute: Optional[int] = None
    count_learn: Optional[int] = None


class Entry(Type):
    homework_entry_id: Optional[int] = None
    date_assigned_on: Optional[DT] = None
    date_prepared_for: Optional[DT] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    materials: Optional[str] = None
    attachment_ids: list | None = None
    attachments: list | None = None
    student_ids: list | None = None


class Homework(Type):
    presence_status_id: Optional[int] = None
    total_count: Optional[int] = None
    execute_count: Optional[int] = None
    descriptions: list[str] | None = None
    link_types: Optional[Any] = None
    materials: Material | None = None
    entries: list[Entry] | None = None


class LearningTargets(Type):
    for_lesson: Optional[bool] = Field(None, alias="forLesson")
    for_home: Optional[bool] = Field(None, alias="forHome")


class Material1(Type):
    uuid: Optional[str] = None
    learning_targets: LearningTargets | None = Field(None, alias="learningTargets")
    is_hidden_from_students: Optional[bool] = Field(None, alias="isHiddenFromStudents")


class Criterion(Type):
    name: Optional[str] = None
    value: Optional[str] = None


class Grade(Type):
    five: Optional[float] = None
    hundred: Optional[float] = None
    origin: Optional[str] = None


class Value(Type):
    name: Optional[str] = None
    grade_system_id: Optional[int] = None
    grade_system_type: Optional[str] = None
    nmax: Optional[float] = None
    grade: Grade | None = None


class Mark(Type):
    id: Optional[int] = None
    comment: Optional[str] = None
    comment_exists: Optional[bool] = None
    control_form_name: Optional[str] = None
    is_exam: Optional[bool] = None
    is_point: Optional[bool] = None
    point_date: Optional[DT] = None
    original_grade_system_type: Optional[str] = None
    criteria: list[Criterion] | None = None
    value: Optional[str] = None
    values: list[Value] | None = None
    weight: Optional[int] = None


class Item(Type):
    id: Optional[int] = None
    author_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    start_at: Optional[DT] = None
    finish_at: Optional[DT] = None
    is_all_day: Optional[bool] = None
    conference_link: Optional[str] = None
    outdoor: Optional[bool] = None
    place: Optional[str] = None
    place_latitude: Optional[Any] = None
    place_longitude: Optional[Any] = None
    created_at: Optional[DT] = None
    updated_at: Optional[DT] = None
    types: list | None = None
    author_name: Optional[str] = None
    registration_start_at: Optional[str] = None
    registration_end_at: Optional[str] = None
    source: Optional[str] = None
    source_id: Optional[str] = None
    place_name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    comment: Optional[str] = None
    need_document: Optional[bool] = None
    type: Optional[str] = None
    format_name: Optional[str] = None
    url: Optional[str] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    room_name: Optional[str] = None
    room_number: Optional[str] = None
    replaced: Optional[bool] = None
    replaced_teacher_id: Optional[int] = None
    esz_field_id: Optional[int] = None
    lesson_type: Optional[str] = None
    course_lesson_type: Optional[str] = None
    lesson_education_type: Optional[str] = None
    lesson_name: Optional[str] = None
    lesson_theme: Optional[str] = None
    activities: Optional[list] = None
    link_to_join: Optional[str] = None
    control: Optional[Any] = None
    class_unit_ids: list[int] | None = None
    class_unit_name: Optional[str] = None
    group_id: Optional[int] = None
    group_name: Optional[str] = None
    external_activities_type: Optional[Any] = None
    address: Optional[str] = None
    place_comment: Optional[str] = None
    building_id: Optional[int] = None
    building_name: Optional[str] = None
    city_building_name: Optional[str] = None
    cancelled: Optional[bool] = None
    is_missed_lesson: Optional[bool] = None
    is_metagroup: Optional[bool] = None
    absence_reason_id: Optional[int] = None
    nonattendance_reason_id: Optional[int] = None
    visible_fake_group: Optional[Any] = None
    health_status: Optional[str] = None
    student_count: Optional[int] = None
    attendances: Optional[Any] = None
    journal_fill: Optional[bool] = None
    comment_count: Optional["int | str"] = None
    comments: Optional[Any] = None
    homework: Homework | None = None
    materials: list[Material1] | None = None
    marks: list[Mark] | None = None


class EventsResponse(Type):
    total_count: Optional[int] = None
    response: list[Item] | None = None
    errors: Optional[Any] = None
