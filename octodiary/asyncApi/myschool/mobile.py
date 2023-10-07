#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import re
from datetime import date
from typing import Optional, Union

from aiohttp import ClientResponse, ClientSession
from aiohttp.cookiejar import CookieJar

from octodiary.asyncApi.base import AsyncBaseApi
from octodiary.exceptions import APIError
from octodiary.types.captcha import async_generate_captcha_class
from octodiary.types.myschool.mobile import (
    EventsResponse,
    FamilyProfile,
    LessonScheduleItems,
    Marks,
    Notification,
    ParallelCurriculum,
    PeriodSchedule,
    PersonData,
    ProfileInfo,
    RatingRankClass,
    RatingRankShort,
    RatingRankSubject,
    ShortHomeworks,
    ShortSubjectMarks,
    SubjectList,
    SubjectMarksForSubject,
    UserChildrens,
    UserSettings,
)
from octodiary.types.myschool.web import SessionUserInfo
from octodiary.urls import URLs


class AsyncMobileAPI(AsyncBaseApi):
    """
    Async Mobile API class wrapper.
    """

    async def login(self, username: str, password: str) -> str:
        """Авторизоваться и получить токен напрямую через обычный логин и пароль."""
        return (
            await self.get(
                url=URLs.LOGIN.AUTH_CALLBACK,
                required_token=False, return_raw_response=True,
                params={
                    "code": (
                        await self.post(
                            url=URLs.API_SESSIONS,
                            required_token=False,
                            json={
                                "login": username,
                                "password_plain": password
                            },
                            model=SessionUserInfo,
                            custom_headers={
                                "Accept": "application/json"
                            }
                        )
                    ).authentication_token
                }
            )
        ).cookies.get("aupd_token").value

    async def handle_action(self, response: ClientResponse, action: Optional[str] = None, failed: Optional[str] = None) -> str | bool:
        match failed or action:
            case None:
                return None
            case "FILL_MFA":
                token_request = (
                    await self.__session_login.get(
                        (
                            await (
                                await self.__session_login.post(
                                    url=URLs.LOGIN.FILL_MFA
                                )
                            ).json()
                        ).get("redirect_url", "")
                    )
                )
                await self.__session_login.close()
                return token_request.cookies.get("aupd_token", None).value
            case "DONE":
                token_request = (
                    await self.__session_login.get(
                        (await response.json()).get("redirect_url", "")
                    )
                )
                await self.__session_login.close()
                self._mfa_details = None
                return token_request.cookies.get("aupd_token", None).value
            case "GRANT_SCOPE_ACCESS":
                response = await self.__session_login.post(
                    url=URLs.LOGIN.ALLOW_SCOPE
                )
                resp_json = await response.json()
                return await self.handle_action(
                    response=response,
                    action=resp_json.get("action", None),
                    failed=resp_json.get("failed", None)
                )
            case "ENTER_MFA":
                self._mfa_details = (await response.json())["mfa_details"]
                return False
            case "SOLVE_ANOMALY_REACTION":
                return await async_generate_captcha_class(
                    response_json=await response.json(),
                    api=self, api_session=self.__session_login
                )
            case other_action_or_failed:
                await self.__session_login.close()
                self._mfa_details = None
                raise APIError(
                    url="ESIA_AUTHORIZATION",
                    status_code=response.status,
                    error_type=other_action_or_failed,
                    description="Esia Authorization error.",
                    details=(await response.json())
                )

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
                url=URLs.LOGIN.AUTHEDU_ESIA_LOGIN,
                allow_redirects=False,
            )
        ).text()
        await self.__session_login.get(
            re.findall(r"0\;url\=(.*?)\">", one)[0]
        )
        await self.__session_login.get(
            url=URLs.LOGIN.GOSUSLUGI_OAUTH2_CONFIG
        )
        login_response = await self.__session_login.post(
            url=URLs.LOGIN.GOSUSLUGI_API_LOGIN,
            json={
                "login": username,
                "password": password
            }
        )
        login_json = await login_response.json()
        return await self.handle_action(
            response=login_response,
            action=login_json.get("action", None),
            failed=login_json.get("failed", None)
        )

    async def esia_enter_MFA(self, code: int) -> str:
        """2 этап получения API-TOKEN прохождение MFA: ввод кода"""
        mfa_method = "otp" if self._mfa_details["type"] == "SMS" else "totp"
        enter_mfa = await self.__session_login.post(
            url=URLs.LOGIN.ENTER_MFA.format(METHOD=mfa_method, CODE=str(code)),
        )
        enter_mfa_json = await enter_mfa.json()
        return await self.handle_action(
            response=enter_mfa,
            action=enter_mfa_json.get("action", None),
            failed=enter_mfa_json.get("failed", None)
        )

    async def get_users_profile_info(self) -> list[ProfileInfo]:
        """
        Получить информацию о профиле
        """
        return await self.get(
            url=URLs.PROFILE_INFO,
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
            url=URLs.MOBILE.FAMILY_PROFILE,
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
            url=URLs.USER_SETTINGS,
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
            url=URLs.USER_SETTINGS,
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
            begin_date: Optional[date] = None,
            end_date: Optional[date] = None,
            expand: str = "marks,homework,absence_reason_id,health_status,nonattendance_reason_id"
    ) -> EventsResponse:
        """Получите расписание."""
        return await self.get(
            url=URLs.EVENTS,
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
            url=URLs.MOBILE.HOMEWORKS_SHORT,
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
            url=URLs.MOBILE.MARKS,
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
    ) -> list[PeriodSchedule]:
        """
        Получить информацию о всех днях с from_date по to_date:
        - какой учебный модуль идет в этот день
        - что это: каникулы, выходной, рабочий день
        """
        return await self.get(
            url=URLs.MOBILE.PERIODS_SCHEDULES,
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
            url=URLs.MOBILE.SUBJECT_MARKS_SHORT,
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
    ) -> list[SubjectList]:
        """
        Получить список предметов
        """
        return await self.get(
            url=URLs.MOBILE.SUBJECTS_LIST,
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
            url=URLs.MOBILE.PROGRAMS_PARALLEL_CURRICULUM,
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
            url=URLs.MOBILE.PERSON_DATA.format(person_id=person_id),
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
            url=URLs.CHILDRENS,
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
    ) -> list[Notification]:
        """
        Получить уведомления пользователя
        """
        return await self.get(
            url=URLs.MOBILE.NOTIFICATIONS,
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
            url=URLs.MOBILE.SUBJECT_MARKS,
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
            url=URLs.MOBILE.LESSON_SCHEDULE_ITEMS.format(lesson_id=lesson_id),
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

    async def get_rating_rank_class(
            self,
            profile_id: int,
            person_id: str,
            class_unit_id: int,
            date: Optional[date] = None
    ) -> list[RatingRankClass]:
        """
        Получить общий рейтинг класса
        """
        return await self.get(
            url=URLs.RATING_RANK_CLASS,
            model=RatingRankClass, is_list=True,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "person_id": person_id,
                "classUnitId": class_unit_id,
                "date": self.date_to_string(date)
            }
        )

    async def get_raging_rank_short(
            self,
            profile_id: int,
            person_id: str,
            begin_date: date,
            end_date: date
    ) -> list[RatingRankShort]:
        """
        Получить общий рейтинг класса
        """
        return await self.get(
            url=URLs.RATING_RANK_SHORT,
            model=RatingRankShort, is_list=True,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "person_id": person_id,
                "beginDate": self.date_to_string(begin_date),
                "endDate": self.date_to_string(end_date),
            }
        )

    async def get_rating_rank_subjects(
            self,
            profile_id: int,
            person_id: str,
            date: date
    ) -> list[RatingRankSubject]:
        """
        Получить рейтинг по предметам
        """
        return await self.get(
            url=URLs.RATING_RANK_SUBJECTS,
            model=RatingRankSubject, is_list=True,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "personId": person_id,
                "date": self.date_to_string(date),
            }
        )
