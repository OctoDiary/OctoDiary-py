#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import http.cookiejar as cookielib
import re
from datetime import date
from typing import Optional, Union

from requests import Response
from requests.utils import dict_from_cookiejar

from octodiary.exceptions import APIError
from octodiary.syncApi.base import SyncBaseApi
from octodiary.types.captcha import generate_captcha_class
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
from octodiary.urls import MySchoolURLs


class SyncMobileAPI(SyncBaseApi):
    """
    Sync Mobile API class wrapper.
    """

    def login(self, username: str, password: str) -> str:
        """Авторизоваться и получить токен напрямую через обычный логин и пароль."""
        return (
            self.get(
                url=MySchoolURLs.LOGIN.AUTH_CALLBACK,
                required_token=False, return_raw_response=True,
                params={
                    "code": (
                        self.post(
                            url=MySchoolURLs.API_SESSIONS,
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
        ).cookies["aupd_token"]

    def handle_action(self, response: Response, action: Optional[str] = None, failed: Optional[str] = None) -> str | bool:
        match failed or action:
            case None:
                return None
            case "FILL_MFA":
                return (
                    dict_from_cookiejar(
                        self.__login_request(
                            self.session.get(
                                self.__login_request(
                                    self.session.post(
                                        url=MySchoolURLs.LOGIN.FILL_MFA,
                                        cookies=self.__cookies
                                    )
                                ).json().get("redirect_url", "")
                            )
                        ).cookies
                    )["aupd_token"]
                )
            case "DONE":
                self._mfa_details = None
                return dict_from_cookiejar(
                    self.__login_request(self.session.get(url=response.json().get("redirect_url", ""))).cookies
                )["aupd_token"]
            case "GRANT_SCOPE_ACCESS":
                response = self.__login_request(
                    self.session.post(
                        url=MySchoolURLs.LOGIN.ALLOW_SCOPE
                    )
                )
                resp_json = response.json()
                return self.handle_action(
                    response=response,
                    action=resp_json.get("action", None),
                    failed=resp_json.get("failed", None)
                )
            case "ENTER_MFA":
                self._mfa_details = response.json()["mfa_details"]
                return False
            case "SOLVE_ANOMALY_REACTION":
                return generate_captcha_class(
                    self,
                    response.json(),
                    self.session,
                )
            case other_action_or_failed:
                self._mfa_details = None
                raise APIError(
                    url="ESIA_AUTHORIZATION",
                    status_code=response.status,
                    error_type=other_action_or_failed,
                    description="Esia Authorization error.",
                    details=response.json()
                )

    def __login_request(self, response):
        self._check_response(response)
        return response

    def esia_login(self, username: str, password: str) -> Union[str, bool]:
        """
        Вход через ЕСИА(Госуслуги) и получение API-TOKEN.
        Если вы получили ``False``, значит у вас стоит MFA,
        используйте метод ``.esia_enter_MFA(code=<CODE>)``, где <CODE> - код MFA.
        """

        self.__cookies = cookielib.CookieJar()

        one: str = self.__login_request(
            self.session.get(
                url=MySchoolURLs.LOGIN.AUTHEDU_ESIA_LOGIN,
                allow_redirects=False
            )
        ).text
        self.__login_request(self.session.get(re.findall(r"0\;url\=(.*?)\">", one)[0], cookies=self.__cookies))
        self.__login_request(self.session.get(MySchoolURLs.LOGIN.GOSUSLUGI_OAUTH2_CONFIG, cookies=self.__cookies))
        login = self.__login_request(self.session.post(
            MySchoolURLs.LOGIN.GOSUSLUGI_API_LOGIN,
            json={
                "login": username,
                "password": password
            },
            cookies=self.__cookies
        ))
        login_json = login.json()
        return self.handle_action(
            response=login,
            action=login_json.get("action", None),
            failed=login_json.get("failed", None)
        )

    def esia_enter_MFA(self, code: int) -> str:
        """2 этап получения API-TOKEN прохождение MFA: ввод кода"""
        mfa_method = "otp" if self._mfa_details["type"] == "SMS" else "totp"
        enter_mfa = self.__login_request(
            self.session.post(
                url=MySchoolURLs.LOGIN.ENTER_MFA.format(METHOD=mfa_method, CODE=str(code)),
                cookies=self.__cookies
            )
        )
        enter_mfa_json = enter_mfa.json()
        return self.handle_action(
            response=enter_mfa,
            action=enter_mfa_json.get("action", None),
            failed=enter_mfa_json.get("failed", None)
        )

    def get_users_profile_info(self) -> list[ProfileInfo]:
        """
        Получить информацию о профиле
        """
        return self.get(
            url=MySchoolURLs.PROFILE_INFO,
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
            url=MySchoolURLs.MOBILE.FAMILY_PROFILE,
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
            url=MySchoolURLs.USER_SETTINGS,
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
            url=MySchoolURLs.USER_SETTINGS,
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
            begin_date: Optional[date] = None,
            end_date: Optional[date] = None,
            expand: str = "marks,homework,absence_reason_id,health_status,nonattendance_reason_id"
    ) -> EventsResponse:
        """Получите расписание."""
        return self.get(
            url=MySchoolURLs.EVENTS,
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
            url=MySchoolURLs.MOBILE.HOMEWORKS_SHORT,
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
            url=MySchoolURLs.MOBILE.MARKS,
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
    ) -> list[PeriodSchedule]:
        """
        Получить информацию о всех днях с from_date по to_date:
        - какой учебный модуль идет в этот день
        - что это: каникулы, выходной, рабочий день
        """
        return self.get(
            url=MySchoolURLs.MOBILE.PERIODS_SCHEDULES,
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
            url=MySchoolURLs.MOBILE.SUBJECT_MARKS_SHORT,
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
    ) -> list[SubjectList]:
        """
        Получить список предметов
        """
        return self.get(
            url=MySchoolURLs.MOBILE.SUBJECTS_LIST,
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
            id: int,
            profile_id: int,
            student_id: int,
    ) -> ParallelCurriculum:
        """
        Получить программу обучения по текущему классу
        """
        return self.get(
            url=MySchoolURLs.MOBILE.PROGRAMS_PARALLEL_CURRICULUM(ID=id),
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
            url=MySchoolURLs.MOBILE.PERSON_DATA.format(person_id=person_id),
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
            url=MySchoolURLs.CHILDRENS,
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
    ) -> list[Notification]:
        """
        Получить уведомления пользователя
        """
        return self.get(
            url=MySchoolURLs.MOBILE.NOTIFICATIONS,
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
            url=MySchoolURLs.MOBILE.SUBJECT_MARKS,
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
            url=MySchoolURLs.MOBILE.LESSON_SCHEDULE_ITEMS.format(lesson_id=lesson_id),
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

    def get_rating_rank_class(
            self,
            profile_id: int,
            person_id: str,
            class_unit_id: int,
            date: Optional[date] = None
    ) -> list[RatingRankClass]:
        """
        Получить общий рейтинг класса
        """
        return self.get(
            url=MySchoolURLs.RATING_RANK_CLASS,
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

    def get_raging_rank_short(
            self,
            profile_id: int,
            person_id: str,
            begin_date: date,
            end_date: date
    ) -> list[RatingRankShort]:
        """
        Получить общий рейтинг класса
        """
        return self.get(
            url=MySchoolURLs.RATING_RANK_SHORT,
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

    def get_rating_rank_subjects(
            self,
            profile_id: int,
            person_id: str,
            date: date
    ) -> list[RatingRankSubject]:
        """
        Получить рейтинг по предметам
        """
        return self.get(
            url=MySchoolURLs.RATING_RANK_SUBJECTS,
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
