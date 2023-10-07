#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from octodiary.types.myschool.mobile.events import EventsResponse
from octodiary.types.myschool.mobile.family_profile import FamilyProfile
from octodiary.types.myschool.mobile.lesson_schedule_items import LessonScheduleItems
from octodiary.types.myschool.mobile.list_subjects import SubjectList
from octodiary.types.myschool.mobile.marks import Marks
from octodiary.types.myschool.mobile.notifications import Notification
from octodiary.types.myschool.mobile.parallel_curriculum import ParallelCurriculum
from octodiary.types.myschool.mobile.periods_schedule import PeriodSchedule
from octodiary.types.myschool.mobile.person_data import PersonData
from octodiary.types.myschool.mobile.rating import RatingRankClass, RatingRankShort, RatingRankSubject
from octodiary.types.myschool.mobile.short_homeworks import ShortHomeworks
from octodiary.types.myschool.mobile.short_subject_marks import ShortSubjectMarks
from octodiary.types.myschool.mobile.subject_marks_for_subject import SubjectMarksForSubject
from octodiary.types.myschool.mobile.user_childrens import UserChildrens
from octodiary.types.myschool.mobile.user_settings import UserSettings
from octodiary.types.myschool.mobile.users_profile_info import ProfileInfo

__all__ = [
    "EventsResponse",
    "FamilyProfile",
    "ShortHomeworks",
    "UserSettings",
    "ProfileInfo",
    "Marks",
    "PeriodSchedule",
    "ShortSubjectMarks",
    "SubjectList",
    "ParallelCurriculum",
    "PersonData",
    "UserChildrens",
    "Notification",
    "SubjectMarksForSubject",
    "LessonScheduleItems",
    "RatingRankClass",
    "RatingRankShort",
    "RatingRankSubject"
]
