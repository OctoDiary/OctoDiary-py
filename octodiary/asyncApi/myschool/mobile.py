import re
from datetime import date
from typing import List, Union

from aiohttp import ClientSession
from aiohttp.cookiejar import CookieJar

from octodiary.exceptions import APIError
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

from ..base import AsyncBaseApi


class AsyncMobileAPI(AsyncBaseApi):
    """
    Async Mobile API class wrapper.
    """


    async def esia_login(self, username: str, password: str) -> Union[str, bool]:
        """
        Вход через ЕСИА(Госуслуги) и получение API-TOKEN.
        Если вы получили ``False``, значит у вас стоит MFA,
        используйте метод ``.esia_enter_MFA(code=<CODE>)``, где <CODE> - код MFA.
        """
        self.__cookie = CookieJar()
        self.__session_login = ClientSession(cookie_jar=self.__cookie, headers=self.headers(False))
        one: str = await (
            await self.__session_login.get(
                "https://authedu.mosreg.ru/v3/auth/esia/login",
                allow_redirects=False,
            )
        ).text()
        await self.__session_login.get(
            re.findall(r"0\;url\=(.*?)\">", one)[0]
        )
        await self.__session_login.get(
            "https://esia.gosuslugi.ru/aas/oauth2/config"
        )
        login_response = await self.__session_login.post(
            "https://esia.gosuslugi.ru/aas/oauth2/api/login",
            json={
                "login": username,
                "password": password
            }
        )
        login_json = await login_response.json()
        action = login_json.get("action", None)

        if action == "FILL_MFA":
            TOKEN = (
                await self.__session_login.get(
                    (
                        await (
                            await self.__session_login.post(
                                "https://esia.gosuslugi.ru/aas/oauth2/api/login/promo-mfa/fill-mfa?decision=false"
                            )
                        ).json()
                    ).get("redirect_url", "")
                )
            ).cookies.get("aupd_token", None).value
            await self.__session_login.close()
            return TOKEN
        elif action == "ENTER_MFA":
            return False
        else:
            await self.__session_login.close()
            
            if (failed := login_json.get("failed", None)):
                raise APIError(
                    url="ESIA_LOGIN_URL",
                    status_code=login_response.status,
                    error_type=failed,
                    description="Login error.",
                    details=login_json
                )
    
    async def esia_enter_MFA(self, code: int) -> str:
        """2 этап получения API-TOKEN прохождение MFA: ввод кода"""
        enter_mfa = await self.__session_login.post(
            f"https://esia.gosuslugi.ru/aas/oauth2/api/login/totp/verify?code={code}"
        )
        enter_mfa_json = await enter_mfa.json()
        if (failed := enter_mfa_json.get("failed", None)):
            await self.__session_login.close()
            raise APIError(
                url="ESIA_ENTER_MFA_URL",
                status_code=enter_mfa.status,
                error_type=failed,
                description="Enter MFA error.",
                details=enter_mfa_json
            )
        
        TOKEN = (
            await self.__session_login.get(
                enter_mfa_json.get("redirect_url", "")
            )
        ).cookies.get("aupd_token", None).value
        await self.__session_login.close()
        return TOKEN
    
    async def get_users_profile_info(self) -> List[ProfileInfo]:
        """
        Получить информацию о профиле
        """
        return await self.get(
            url="https://myschool.mosreg.ru/acl/api/users/profile_info",
            custom_headers={
                "partner-source-id": "MOBILE"
            },
            model=ProfileInfo,
            is_list=True
        )

    async def get_profile(self, profile_id: int) -> FamilyProfile:
        """
        Получить профиль пользователя
        """
        return await self.get(
            url="https://api.myschool.mosreg.ru/family/mobile/v1/profile",
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            model=FamilyProfile
        )
    
    async def get_user_settings_app(
        self,
        profile_id: int,
        name: str = "settings_group_v1",
        subsystem_id: int = 1
    ) -> UserSettings:
        """
        Получить настройки приложения пользователя
        """
        return await self.get(
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

    async def edit_user_settings_app(
        self,
        settings: UserSettings,
        profile_id: int,
        name: str = "settings_group_v1",
        subsystem_id: int = 1,
    ):
        """
        Изменить настройки приложения пользователя
        """
        await self.put(
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
    
    async def get_events(
        self,
        person_id: str,
        mes_role: str,
        begin_date: date = None,
        end_date: date = None,
        expand: str = "marks,homework,absence_reason_id,health_status,nonattendance_reason_id"
    ) -> EventsResponse:
        """Получите расписание."""
        return await self.get(
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

    async def get_homeworks_short(
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
        return await self.get(
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

    async def get_marks(
        self,
        student_id: int,
        profile_id: int,
        from_date: date,
        to_date: date
    ) -> Marks:
        """
        Получить оценки
        """
        return await self.get(
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
    
    async def get_periods_schedules(
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
        return await self.get(
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
    
    async def get_subject_marks_short(
        self,
        student_id: int,
        profile_id: int,
    ) -> ShortSubjectMarks:
        """
        Получить оценки и ср.баллы по предметам за период времени
        """
        return await self.get(
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

    async def get_subjects(
        self,
        student_id: int,
        profile_id: int,
    ) -> List[SubjectList]:
        """
        Получить список предметов
        """
        return await self.get(
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

    async def get_programs_parallel_curriculum(
        self,
        profile_id: int,
        student_id: int,
    ) -> ParallelCurriculum:
        """
        Получить программу обучения по текущему классу
        """
        return await self.get(
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

    async def get_person_data(
        self,
        person_id: str,
        profile_id: int,
    ) -> PersonData:
        """
        Получить подробную информацию о пользователе
        """
        return await self.get(
            url=f"https://myschool.mosreg.ru/api/persondata/mobile/persons/{person_id}",
            model=PersonData,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            }
        )
    
    async def get_user_childrens(
        self,
        person_id: str,
    ) -> UserChildrens:
        """
        Получить детей пользователя
        """
        return await self.get(
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

    async def get_notifications(
        self,
        student_id: int,
        profile_id: int
    ) -> List[Notification]:
        """
        Получить уведомления пользователя
        """
        return await self.get(
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

    async def get_subject_marks_for_subject(
        self,
        student_id: int,
        profile_id: int,
        subject_name: int
    ) -> SubjectMarksForSubject:
        """
        Получить оценки по предмету
        """
        return await self.get(
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

    async def get_lesson_schedule_items(
        self,
        profile_id: int,
        lesson_id: int,
        student_id: int,
        type: str = "PLAN"
    ) -> LessonScheduleItems:
        """
        Получить информацию об уроке
        """
        return await self.get(
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
