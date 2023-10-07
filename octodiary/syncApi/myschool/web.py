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
from octodiary.types.myschool.web import (
    AcademicYear,
    EventsResponse,
    PersonData,
    Role,
    SessionUserInfo,
    StudentProfile,
    User,
    UserChildren,
    UserContact,
    UserInfo,
    WebFamilyProfile,
    WebOrganizations,
)
from octodiary.urls import URLs


class SyncWebAPI(SyncBaseApi):
    """
    Sync Web API class wrapper.
    """

    def login(self, username: str, password: str) -> str:
        """
        Авторизация по логину и паролю дневника
        Args:
            username: Логин
            password: Пароль

        Returns:
            Токен доступа

        """
        return (
            self.get(
                url=URLs.LOGIN.AUTH_CALLBACK,
                required_token=False, return_raw_response=True,
                params={
                    "code": (
                        self.post(
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
                                        URLs.LOGIN.FILL_MFA,
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
                    self.__login_request(self.session.get(response.json().get("redirect_url", ""))).cookies
                )["aupd_token"]
            case "GRANT_SCOPE_ACCESS":
                response = self.__login_request(
                    self.session.post(
                        url=URLs.LOGIN.ALLOW_SCOPE
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
                    self.session
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
        Вход через ЕСИА
        Args:
            username: логин Госуслуг (телефон, почта, СНИЛС)
            password: пароль Госуслуг

        Returns:
            Токен доступа или False (-> esia_enter_mfa())

        """

        self.__cookies = cookielib.CookieJar()

        one: str = self.__login_request(
            self.session.get(
                URLs.LOGIN.AUTHEDU_ESIA_LOGIN,
                allow_redirects=False
            )
        ).text
        self.__login_request(self.session.get(re.findall(r"0;url=(.*?)\">", one)[0], cookies=self.__cookies))
        self.__login_request(self.session.get(URLs.LOGIN.GOSUSLUGI_OAUTH2_CONFIG, cookies=self.__cookies))
        login = self.__login_request(self.session.post(
            url=URLs.LOGIN.GOSUSLUGI_API_LOGIN,
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

    def esia_enter_mfa(self, code: int) -> str:
        """
        Ввод кода МФА
        Args:
            code: код МФА (аутентификатор или смс)

        Returns:
            Токен доступа

        """
        mfa_method = "otp" if self._mfa_details["type"] == "SMS" else "totp"
        enter_mfa = self.__login_request(
            self.session.post(
                URLs.LOGIN.ENTER_MFA.format(METHOD=mfa_method, CODE=str(code)),
                cookies=self.__cookies
            )
        )
        enter_mfa_json = enter_mfa.json()
        return self.handle_action(
            response=enter_mfa,
            action=enter_mfa_json.get("action", None),
            failed=enter_mfa_json.get("failed", None)
        )

    def get_user_info(self) -> UserInfo:
        """
        Получить информацию о пользователе
        Returns:
            UserInfo

        """
        return self.get(url=URLs.USER_INFO, model=UserInfo)

    def refresh_token(self, role_id: Optional[int] = None, subsystem: Optional[int] = None) -> str:
        """
        Обновить токен доступа
        Args:
            role_id: int
            subsystem: int

        Returns:
            Новый токен доступ

        """
        return self.get(
            url=URLs.REFRESH_TOKEN,
            params={"roleId": role_id, "subsystem": subsystem},
            return_raw_text=True
        )

    def get_system_messages(
            self,
            published: bool = True,
            today: bool = True,
            profile_id: Optional[int] = None,
            profile_type: Optional[str] = None,
            pid: Optional[int] = None
    ) -> list:
        """
        Получить сообщения системы
        Args:
            published: bool
            today: bool
            profile_id: int
            profile_type: str
            pid: int

        Returns:
            Список сообщений

        """
        return self.get(
            url=URLs.SYSTEM_MESSAGES,
            custom_headers={
                "Accept": "application/json",
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            params={"pid": pid, "published": published, "today": today},
            return_json=True
        )

    def get_session_info(self) -> SessionUserInfo:
        """
        Получить информацию о пользователе
        Returns:
            SessionUserInfo

        """
        return self.post(
            url=URLs.API_SESSIONS2,
            custom_headers={
                "auth_token": self.token,
                "Content-Type": "application/json;charset=utf-8",
            },
            json={"auth_token": self.token},
            model=SessionUserInfo,
        )

    def get_academic_years(
            self,
            profile_id: Optional[int] = None,
            profile_type: Optional[str] = None,
            pid: Optional[int] = None
    ) -> list[AcademicYear]:
        """
        Получить учебные года
        Args:
            profile_id: int
            profile_type: str
            pid: int

        Returns:
            Список учебных лет

        """
        return self.get(
            url=URLs.ACADEMIC_YEARS,
            custom_headers={
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            params={"pid": pid},
            model=AcademicYear,
            is_list=True,
        )

    def get_user(
            self,
            ids: Union[int, list[int]] = 1,
            pid: Optional[int] = None,
            profile_id: Optional[int] = None,
            profile_type: Optional[str] = None
    ) -> Union[User, list[User]]:
        """
        Получить информацию о пользователе(-ях)
        Args:
            ids: int или list[int]
            pid: int
            profile_id: int
            profile_type: str

        Returns:
            User или list[User]

        """
        return self.get(
            url=URLs.USER,
            custom_headers={
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            model=User,
            is_list=True,
            params={
                "ids": ids if isinstance(ids, int) else ",".join(map(str, ids)),
                "pid": pid,
            }
        )

    def get_student_profiles(
            self,
            academic_year_id: int = 0,
            page: int = 1,
            per_page: int = 50,
            pid: Optional[int] = None,
            profile_id: Optional[int] = None,
            profile_type: Optional[str] = None
    ) -> Union[StudentProfile, list[StudentProfile]]:
        """
        Получить информацию об ученике(-ах)
        Args:
            academic_year_id: int
            page: int
            per_page: int
            pid: int
            profile_id: int
            profile_type: str

        Returns:
            StudentProfile или list[StudentProfile]

        """
        return self.get(
            url=URLs.STUDENT_PROFILES,
            custom_headers={
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            model=StudentProfile,
            is_list=True,
            params={
                "pid": pid,
                "academic_year_id": academic_year_id,
                "page": page,
                "per_page": per_page
            }
        )

    def get_family_web_profile(
            self,
            profile_id: Optional[int] = None,
            profile_type: Optional[str] = None,
            nocache: bool = True
    ) -> WebFamilyProfile:
        """
        TODO Описать метод
        Args:
            profile_id: int
            profile_type: str
            nocache: bool

        Returns:
            WebFamilyProfile

        """
        return self.get(
            url=URLs.WEB.FAMILY_PROFILE,
            custom_headers={
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
                "X-mes-subsystem": "familyweb",
            },
            model=WebFamilyProfile,
            params={
                "nocache": nocache
            }
        )

    def get_person_data(self, person_id: str) -> PersonData:
        """
        Получить полную информацию о пользователе
        Args:
            person_id: str

        Returns:
            PersonData

        """
        return self.get(
            url=URLs.PERSON_DATA.format(person_id=person_id),
            custom_headers={
                "x-mes-subsystem": "headerweb",
            },
            model=PersonData,
        )

    def get_all_roles_global(self) -> list[Role]:
        """
        Получить список всех ролей
        Returns:
            list[Role]

        """
        return self.get(
            url=URLs.ROLES,
            model=Role, is_list=True, required_token=False
        )

    def get_events(
            self,
            person_id: str,
            mes_role: str,
            begin_date: Optional[date] = None,
            end_date: Optional[date] = None,
            expand: str = "marks,homework,absence_reason_id,health_status,nonattendance_reason_id"
    ) -> EventsResponse:
        """
        Получить события (их расписание)
        Args:
            person_id: ID персоны
            mes_role: Роль
            begin_date: Начало расписания
            end_date: Окончание расписания
            expand: Дополнительные поля

        Returns:
            EventsResponse

        """
        return self.get(
            url=URLs.EVENTS,
            custom_headers={
                "X-Mes-Subsystem": "familyweb",
                "X-Mes-Role": mes_role,
            },
            model=EventsResponse,
            params={
                "person_ids": person_id,
                "begin_date": self.date_to_string(begin_date),
                "end_date": self.date_to_string(end_date),
                "expand": expand,
            }
        )

    def get_children(self, sso_id: str, timeout: int = 10) -> UserChildren:
        """
        Получить полную информацию о всех детях
        Args:
            sso_id: str
            timeout: int

        Returns:
            UserChildren

        """
        return self.get(
            url=URLs.CHILDRENS,
            model=UserChildren,
            params={
                "sso_id": sso_id,
                "timeout": timeout
            }
        )

    def get_user_contacts(self) -> list[UserContact]:
        """
        Получить контактные данные пользователя
        Returns:
            list[UserContact]

        """
        return self.get(
            url=URLs.USER_CONTACTS,
            model=UserContact,
            params={
                "source": "CONTINGENT",
            },
            is_list=True,
        )

    def get_organisations(
            self,
            organization_id: int,
            page: int = 1,
            size: int = 10,
            timeout: int = 20,
    ) -> WebOrganizations:
        """
        Получить информацию о всех организациях
        Args:
            organization_id: int
            page: int
            size: int
            timeout: int

        Returns:
            WebOrganizations

        """
        return self.get(
            url=URLs.ORGANIZATIONS,
            model=WebOrganizations,
            params={
                "page": page,
                "size": size,
                "organizationId": organization_id,
                "timeout": timeout,
            }
        )

    get_organizations = get_organisations
