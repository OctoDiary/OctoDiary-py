#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from datetime import date, datetime
from typing import Any, List, Optional

from pydantic import Field

from ...model import Type


class Material(Type):
    count_execute: Optional[int] = None
    count_learn: Optional[int] = None


class Entry(Type):
    homework_entry_id: Optional[int] = None
    date_assigned_on: date
    date_prepared_for: date
    description: str
    duration: Optional[int] = None
    materials: Optional[str]
    attachment_ids: List
    attachments: List
    student_ids: Any


class HomeworkItem(Type):
    presence_status_id: Optional[int] = None
    total_count: Optional[int] = None
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


class ResponseItem(Type):
    id: Optional[int] = None
    author_id: Any
    title: Optional[str]
    description: Optional[str]
    start_at: datetime
    finish_at: datetime
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
    room_name: Optional[str] = None
    room_number: Optional[str] = None
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
    place_comment: Any
    building_id: Optional[int] = None
    building_name: Optional[str] = None
    city_building_name: Any
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
    marks: Optional[List[Any]]


class EventsResponse(Type):
    total_count: Optional[int] = None
    response: Optional[List[ResponseItem]] = None
