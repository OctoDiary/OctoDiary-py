from datetime import date
from typing import List

from octodiary.types.myschool.mobile import (
    EventsResponse,
    FamilyProfile,
    Marks,
    Notification,
    ParallelCurriculum,
    PeriodSchedule,
    PersonData,
    ProfileInfo,
    ShortHomeworks,
    ShortSubjectMarks,
    SubjectList,
    SubjectMarksForSubject,
    UserChildrens,
    UserSettings,
    LessonScheduleItems
)

from ..base import SyncBaseApi


class SyncMobileAPI(SyncBaseApi):
    """
    Sync Mobile API class wrapper.
    """

    def get_users_profile_info(self) -> List[ProfileInfo]:
        """
        Получить информацию о профиле
        """
        return self.get(
            url="https://myschool.mosreg.ru/acl/api/users/profile_info",
            custom_headers={
                "partner-source-id": "MOBILE"
            },
            model=ProfileInfo,
            is_list=True
        )

    def get_profile(self, profile_id: int) -> FamilyProfile:
        """
        Получить профиль пользователя
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/profile",
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            model=FamilyProfile
        )
    
    def get_user_settings_app(
        self,
        profile_id: int,
        name: str = "settings_group_v1",
        subsystem_id: int = 1
    ) -> UserSettings:
        """
        Получить настройки приложения пользователя
        """
        return self.get(
            url="https://authedu.mosreg.ru/api/usersettings/v1",
            params={
                "name": name,
                "subsystem_id": subsystem_id,
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            model=UserSettings,
        )

    def edit_user_settings_app(
        self,
        settings: UserSettings,
        profile_id: int,
        name: str = "settings_group_v1",
        subsystem_id: int = 1,
    ):
        """
        Изменить настройки приложения пользователя
        """
        self.put(
            url="https://authedu.mosreg.ru/api/usersettings/v1",
            params={
                "name": name,
                "subsystem_id": subsystem_id,
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            json=settings.model_dump(),
            return_raw_text=True
        )
    

    def get_events(
        self,
        person_id: str,
        mes_role: str,
        begin_date: date = None,
        end_date: date = None,
        expand: str = "marks,homework,absence_reason_id,health_status,nonattendance_reason_id"
    ) -> EventsResponse:
        """Получите расписание."""
        return self.get(
            url="https://authedu.mosreg.ru/api/eventcalendar/v1/api/events",
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "x-mes-role": mes_role,
            },
            model=EventsResponse,
            params={
                "person_ids": person_id,
                "begin_date": self.date_to_string(begin_date),
                "end_date": self.date_to_string(end_date),
                "expand": expand,
            }
        )

    def get_homeworks_short(
        self,
        student_id: int,
        profile_id: int,
        from_date: date,
        to_date: date,
        sort_column: str = "date",
        sort_direction: str = "asc",
    ) -> ShortHomeworks:
        """
        Получить список домашних заданий
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/homeworks/short",
            params={
                "student_id": student_id,
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
                "sort_column": sort_column,
                "sort_direction": sort_direction
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            },
            model=ShortHomeworks,
        )

    def get_marks(
        self,
        student_id: int,
        profile_id: int,
        from_date: date,
        to_date: date
    ) -> Marks:
        """
        Получить оценки
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/marks",
            params={
                "student_id": student_id,
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            },
            model=Marks
        )
    
    def get_periods_schedules(
        self,
        student_id: int,
        profile_id: int,
        from_date: date,
        to_date: date
    ) -> List[PeriodSchedule]:
        """
        Получить информацию о всех днях с from_date по to_date:
        - какой учебный модуль идет в этот день
        - что это: каникулы, выходной, рабочий день
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/periods_schedules",
            params={
                "student_id": student_id,
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d"),
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            },
            model=PeriodSchedule,
            is_list=True
        )
    
    def get_subject_marks_short(
        self,
        student_id: int,
        profile_id: int,
    ) -> ShortSubjectMarks:
        """
        Получить оценки и ср.баллы по предметам за период времени
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/subject_marks/short",
            params={
                "student_id": student_id,
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            },
            model=ShortSubjectMarks,
        )

    def get_subjects(
        self,
        student_id: int,
        profile_id: int,
    ) -> List[SubjectList]:
        """
        Получить список предметов
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/subjects/list",
            model=SubjectList,
            is_list=True,
            params={
                "student_id": student_id,
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            }
        )

    def get_programs_parallel_curriculum(
        self,
        profile_id: int,
        student_id: int,
    ) -> ParallelCurriculum:
        """
        Получить программу обучения по текущему классу
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/programs/parallel_curriculum/162269",
            model=ParallelCurriculum,
            is_list=True,
            params={
                "student_id": student_id,
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            }
        )

    def get_person_data(
        self,
        person_id: str,
        profile_id: int,
    ) -> PersonData:
        """
        Получить подробную информацию о пользователе
        """
        return self.get(
            url=f"https://myschool.mosreg.ru/api/persondata/mobile/persons/{person_id}",
            model=PersonData,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            }
        )
    
    def get_user_childrens(
        self,
        person_id: str,
    ) -> UserChildrens:
        """
        Получить детей пользователя
        """
        return self.get(
            url="https://authedu.mosreg.ru/v1/user/childrens",
            params={
                "person_id": person_id,
            },
            model=UserChildrens,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile"
            }
        )

    def get_notifications(
        self,
        student_id: int,
        profile_id: int
    ) -> List[Notification]:
        """
        Получить уведомления пользователя
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/notifications/search",
            model=Notification,
            is_list=True,
            params={
                "student_id": student_id
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            }
        )

    def get_subject_marks_for_subject(
        self,
        student_id: int,
        profile_id: int,
        subject_name: int
    ) -> SubjectMarksForSubject:
        """
        Получить оценки по предмету
        """
        return self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/subject_marks/for_subject",
            model=SubjectMarksForSubject,
            params={
                "student_id": student_id,
                "subject_name": subject_name
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            }
        )

    def get_lesson_schedule_items(
        self,
        profile_id: int,
        lesson_id: int,
        student_id: int,
        type: str = "PLAN"
    ) -> LessonScheduleItems:
        """
        Получить информацию об уроке
        """
        return self.get(
            url=f"https://api.myschool.mosreg.ru/family/mobile/v1/lesson_schedule_items/{lesson_id}",
            params={
                "student_id": student_id,
                "type": type
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            model=LessonScheduleItems
        )
