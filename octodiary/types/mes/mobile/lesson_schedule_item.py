#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from datetime import date, datetime
from typing import Any, Optional

from pydantic import Field

from octodiary.types.model import Type


class Teacher(Type):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[Any] = None
    user_id: Optional[Any] = None


class Grade(Type):
    origin: Optional[str]
    five: Optional[int]
    hundred: Optional[int]


class Value(Type):
    name: Optional[str] = None
    nmax: Optional[int] = None
    grade: Optional[Grade] = None
    grade_system_id: Optional[int] = None
    grade_system_type: Optional[str] = None


class Mark(Type):
    id: Optional[int] = None
    value: Optional[str] = None
    values: Optional[list[Value]] = []
    comment: Optional[str] = None
    weight: Optional[int] = None
    point_date: Optional[Any] = None
    control_form_name: Optional[str] = None
    comment_exists: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    criteria: Optional[list] = []
    is_exam: Optional[bool] = None
    is_point: Optional[bool] = None
    original_grade_system_type: Optional[str] = None


class Url(Type):
    url: Optional[str] = None
    url_type: Optional[str] = None


class Item(Type):
    id: Optional[int] = None
    uuid: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    file_size: Optional[int] = None
    progress: Optional[Any] = None
    status: Optional[Any] = None
    urls: Optional[list[Url]] = []
    average_rating: Optional[Any] = None
    views: Optional[Any] = None
    class_level_ids: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    accepted_at: Optional[Any] = None
    user_name: Optional[Any] = None
    author: Optional[Any] = None
    icon_url: Optional[Any] = None
    full_cover_url: Optional[Any] = None
    for_lesson: Optional[Any] = None
    for_home: Optional[Any] = None
    selected_mode: Optional[str] = None
    partner_response: Optional[Any] = None
    content_type: Optional[Any] = None
    binding_id: Optional[Any] = None
    is_necessary: Optional[bool] = None
    is_hidden_from_students: Optional[bool] = None


class Material(Type):
    type: Optional[str] = None
    type_name: Optional[str] = None
    action_id: Optional[int] = None
    action_name: Optional[str] = None
    items: Optional[list[Item]] = []


class LessonHomework(Type):
    homework: Optional[str] = None
    materials: Optional[list[Material]] = []
    homework_entry_student_id: Optional[int] = None
    homework_id: Optional[int] = None
    homework_entry_id: Optional[int] = None
    attachments: Optional[list] = []
    homework_created_at: Optional[datetime] = None
    homework_updated_at: Optional[datetime] = None
    is_done: Optional[bool] = None
    written_answer: Optional[Any] = None
    date_assigned_on: Optional[datetime] = None
    date_prepared_for: Optional[datetime] = None


class ThemeFrame(Type):
    id: Optional[int] = None
    title: Optional[str] = None
    theme_integration_id: int = Field(None, alias="themeIntegrationId")
    average_mark: Optional[str] = None
    theme_frames: Optional[list["ThemeFrame"]] = []
    oge_task_name: Optional[Any] = None
    ege_task_name: Optional[Any] = None


class Theme(Type):
    id: Optional[Any] = None
    title: Optional[Any] = None
    theme_integration_id: int = Field(None, alias="themeIntegrationId")
    average_mark: Optional[str] = None
    theme_frames: Optional[list[ThemeFrame]] = None
    oge_task_name: Optional[Any] = None
    ege_task_name: Optional[Any] = None


class Details(Type):
    content: Optional[list] = []
    materials: Optional[list] = []
    theme: Optional[Theme] = None
    lesson_id: Optional[int] = Field(None, alias="lessonId")
    lesson_topic: Optional[str] = None


class LessonScheduleItem(Type):
    id: Optional[int] = None
    plan_id: Optional[int] = None
    date: Optional[str] = None
    begin_time: Optional[str] = None
    begin_utc: Optional[datetime] = None
    end_time: Optional[str] = None
    end_utc: Optional[datetime] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    teacher: Optional[Teacher] = None
    course_lesson_type: Optional[Any] = None
    room_number: Optional[str] = None
    room_name: Optional[str] = None
    building_name: Optional[str] = None
    marks: Optional[list[Mark]] = None
    created_date_time: Optional[datetime] = None
    is_missed_lesson: Optional[bool] = None
    lesson_type: Optional[str] = None
    field_name: Optional[Any] = None
    comment: Optional[Any] = None
    lesson_homeworks: Optional[list[LessonHomework]] = None
    homework_to_give: Optional[Any] = None
    details: Optional[Details] = None
    esz_field_id: Optional[Any] = None
    remote_lesson: Optional[Any] = None
    control: Optional[Any] = None
    evaluation: Optional[Any] = None
    lesson_education_type: Optional[str] = None
    disease_status_type: Optional[Any] = None
    is_virtual: Optional[bool] = None
    homework_presence_status_id: Optional[int] = None
