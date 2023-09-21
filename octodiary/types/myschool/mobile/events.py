#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any, List, Optional

from pydantic import Field

from ...model import Type


class Material(Type):
    count_execute: int
    count_learn: int


class Entry(Type):
    homework_entry_id: int
    date_assigned_on: str
    date_prepared_for: str
    description: str
    duration: int
    materials: Optional[str]
    attachment_ids: List
    attachments: List
    student_ids: Any


class HomeworkItem(Type):
    presence_status_id: int
    total_count: int
    execute_count: Optional[int]
    descriptions: Optional[List[str]]
    link_types: Any
    materials: Optional[Material]
    entries: Optional[List[Entry]]


class LearningTargets(Type):
    for_lesson: bool = Field(..., alias='forLesson')
    for_home: bool = Field(..., alias='forHome')


class Material1(Type):
    uuid: str
    learning_targets: LearningTargets = Field(..., alias='learningTargets')
    is_hidden_from_students: bool = Field(..., alias='isHiddenFromStudents')


class Criterion(Type):
    name: str
    value: str


class Grade(Type):
    five: float
    hundred: float
    origin: str


class Value(Type):
    name: str
    grade_system_id: int
    grade_system_type: str
    nmax: float
    grade: Grade


class Mark(Type):
    id: int
    comment: Any
    comment_exists: bool
    control_form_name: str
    is_exam: bool
    is_point: bool
    point_date: Any
    original_grade_system_type: str
    criteria: List[Criterion]
    value: str
    values: List[Value]
    weight: int


class EventType(Type):
    id: int
    author_id: Any
    title: Optional[str]
    description: Optional[str]
    start_at: str
    finish_at: str
    is_all_day: Any
    conference_link: Any
    outdoor: Any
    place: Any
    place_latitude: Any
    place_longitude: Any
    created_at: Any
    updated_at: Any
    types: Any
    author_name: Any
    registration_start_at: Any
    registration_end_at: Any
    source: str
    source_id: str
    place_name: Any
    contact_name: Any
    contact_phone: Any
    contact_email: Any
    comment: Any
    need_document: Any
    type: Optional[str]
    format_name: Any
    url: Any
    subject_id: Optional[int]
    subject_name: Optional[str]
    room_name: Optional[str]
    room_number: Optional[str]
    replaced: Optional[bool]
    replaced_teacher_id: Optional[int]
    esz_field_id: Any
    lesson_type: Optional[str]
    course_lesson_type: Any
    lesson_education_type: Any
    lesson_name: Optional[str]
    lesson_theme: Optional[str]
    activities: Any
    link_to_join: Any
    control: Any
    class_unit_ids: Optional[List[int]]
    class_unit_name: Optional[str]
    group_id: Optional[int]
    group_name: Optional[str]
    external_activities_type: Any
    address: Any
    place_comment: Optional[str]
    building_id: Optional[int]
    building_name: Optional[str]
    city_building_name: Optional[str]
    cancelled: Optional[bool]
    is_missed_lesson: Optional[bool]
    is_metagroup: Any
    absence_reason_id: Any
    nonattendance_reason_id: Any
    visible_fake_group: Any
    health_status: Any
    student_count: Any
    attendances: Any
    journal_fill: Optional[bool]
    comment_count: Any
    comments: Any
    homework: Optional[HomeworkItem]
    materials: Optional[List[Material1]]
    marks: Optional[List[Mark]]


class EventsResponse(Type):
    total_count: int
    response: List[EventType]
