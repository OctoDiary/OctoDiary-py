#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import re
from datetime import date
from typing import List, Union

from aiohttp import ClientSession, ClientResponse
from aiohttp.cookiejar import CookieJar

from octodiary.exceptions import APIError
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

from ..base import AsyncBaseApi


class AsyncWebAPI(AsyncBaseApi):
    """
    Async Web API class wrapper.
    """

    async def login(self, username: str, password: str) -> str:
        """
        Авторизация по логину и паролю дневника
        Args:
            username: Логин
            password: Пароль

        Returns:
            Токен доступа

        """
        return (
            await self.get(
                url="https://authedu.mosreg.ru/v3/auth/kauth/callback",
                required_token=False, return_raw_response=True,
                params={
                    "code": (
                        await self.post(
                            url="https://authedu.mosreg.ru/lms/api/sessions",
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

    async def handle_action(self, response: ClientResponse, action: str = None, failed: str = None) -> str | bool:
        match action or failed:
            case None:
                return None
            case "FILL_MFA":
                token_request = (
                    await self.__session_login.get(
                        (
                            await (
                                await self.__session_login.post(
                                    "https://esia.gosuslugi.ru/aas/oauth2/api/login/promo-mfa/fill-mfa?decision=false"
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
                return token_request.cookies.get("aupd_token", None).value
            case "GRANT_SCOPE_ACCESS":
                response = await self.__session_login.post(
                    url="https://esia.gosuslugi.ru/aas/oauth2/api/scope/allow"
                )
                resp_json = await response.json()
                return await self.handle_action(
                    response=response,
                    action=resp_json.get("action", None),
                    failed=resp_json.get("failed", None)
                )
            case "ENTER_MFA":
                return False
            case other_action_or_failed:  # SOLVE_ANOMALY_REACTION  INVALID_TTP  INVALID_OTP
                await self.__session_login.close()
                raise APIError(
                    url="ESIA_AUTHORIZATION",
                    status_code=response.status,
                    error_type=other_action_or_failed,
                    description="Esia Authorization error.",
                    details=(await response.json())
                )
    
    async def esia_login(self, username: str, password: str) -> Union[str, bool]:
        """
        Вход через ЕСИА
        Args:
            username: логин Госуслуг (телефон, почта, СНИЛС)
            password: пароль Госуслуг

        Returns:
            Токен доступа или False (-> esia_enter_mfa())

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
            re.findall(r"0;url=(.*?)\">", one)[0]
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
        return await self.handle_action(
            response=login_response,
            action=login_json.get("action", None),
            failed=login_json.get("failed", None)
        )
    
    async def esia_enter_mfa(self, code: int) -> str:
        """
        Ввод кода МФА
        Args:
            code: код МФА (аутентификатор или смс)

        Returns:
            Токен доступа

        """
        enter_mfa = await self.__session_login.post(
            f"https://esia.gosuslugi.ru/aas/oauth2/api/login/totp/verify?code={code}"
        )
        enter_mfa_json = await enter_mfa.json()
        return await self.handle_action(
            response=enter_mfa,
            action=enter_mfa_json.get("action", None),
            failed=enter_mfa_json.get("failed", None)
        )
    
    async def get_user_info(self) -> UserInfo:
        """
        Получить информацию о пользователе
        Returns:
            UserInfo

        """
        return await self.get("https://authedu.mosreg.ru/v3/userinfo", model=UserInfo)
    
    async def refresh_token(self, role_id: int = None, subsystem: int = None) -> str:
        """
        Обновить токен доступа
        Args:
            role_id: int
            subsystem: int

        Returns:
            Новый токен доступ

        """
        return await self.get(
            "https://authedu.mosreg.ru/v2/token/refresh",
            params={"roleId": role_id, "subsystem": subsystem},
            return_raw_text=True
        )
    
    async def get_system_messages(
        self,
        published: bool = True,
        today: bool = True,
        profile_id: int = None,
        profile_type: str = None,
        pid: int = None
    ) -> List:
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
        return await self.get(
            "https://myschool.mosreg.ru/acl/api/system_messages",
            custom_headers={
                "Accept": "application/json",
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            params={"pid": pid, "published": published, "today": today},
            return_json=True
        )
    
    async def get_session_info(self) -> SessionUserInfo:
        """
        Получить информацию о пользователе
        Returns:
            SessionUserInfo

        """
        return await self.post(
            "https://myschool.mosreg.ru/lms/api/sessions",
            {
                "auth_token": self.token,
                "Content-Type": "application/json;charset=utf-8",
            },
            json={"auth_token": self.token},
            model=SessionUserInfo,
        )

    async def get_academic_years(
        self,
        profile_id: int = None,
        profile_type: str = None,
        pid: int = None
    ) -> List[AcademicYear]:
        """
        Получить учебные года
        Args:
            profile_id: int
            profile_type: str
            pid: int

        Returns:
            Список учебных лет

        """
        return await self.get(
            "https://myschool.mosreg.ru/core/api/academic_years",
            {
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            params={"pid": pid},
            model=AcademicYear,
            is_list=True,
        )
    
    async def get_user(
        self,
        ids: Union[int, List[int]] = 1,
        pid: int = None,
        profile_id: int = None,
        profile_type: str = None
    ) -> Union[User, List[User]]:
        """
        Получить информацию о пользователе(-ях)
        Args:
            ids: int или List[int]
            pid: int
            profile_id: int
            profile_type: str

        Returns:
            User или List[User]

        """
        return await self.get(
            "https://myschool.mosreg.ru/acl/api/users",
            {
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            model=User,
            is_list=True,
            params={
                "ids": ids if isinstance(ids, int) else ','.join(map(str, ids)),
                "pid": pid,
            }
        )
    
    async def get_student_profiles(
        self,
        academic_year_id: int = 0,
        page: int = 1,
        per_page: int = 50,
        pid: int = None,
        profile_id: int = None,
        profile_type: str = None
    ) -> Union[StudentProfile, List[StudentProfile]]:
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
            StudentProfile или List[StudentProfile]

        """
        return await self.get(
            "https://myschool.mosreg.ru/core/api/student_profiles",
            {
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

    async def get_family_web_profile(
        self,
        profile_id: int = None,
        profile_type: str = None,
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
        return await self.get(
            "https://authedu.mosreg.ru/api/family/web/v1/profile",
            {
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
                "X-mes-subsystem": "familyweb",
            },
            model=WebFamilyProfile,
            params={
                "nocache": nocache
            }
        )
    
    async def get_person_data(self, person_id: str) -> PersonData:
        """
        Получить полную информацию о пользователе
        Args:
            person_id: str

        Returns:
            PersonData

        """
        return await self.get(
            f"https://authedu.mosreg.ru/api/persondata/v1/persons/{person_id}",
            {
                "x-mes-subsystem": "headerweb",
            },
            model=PersonData,
        )
    
    async def get_all_roles_global(self) -> List[Role]:
        """
        Получить список всех ролей
        Returns:
            List[Role]

        """
        return await self.get(
            "https://authedu.mosreg.ru/v1/roles/allGlobal/",
            model=Role, is_list=True, required_token=False
        )
    
    async def get_events(
        self,
        person_id: str,
        mes_role: str,
        begin_date: date = None,
        end_date: date = None,
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
        return await self.get(
            "https://authedu.mosreg.ru/api/eventcalendar/v1/api/events",
            {
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
    
    async def get_children(self, sso_id: str, timeout: int = 10) -> UserChildren:
        """
        Получить полную информацию о всех детях
        Args:
            sso_id: str
            timeout: int

        Returns:
            UserChildren

        """
        return await self.get(
            "https://authedu.mosreg.ru/v1/user/childrens",
            model=UserChildren,
            params={
                "sso_id": sso_id,
                "timeout": timeout
            }
        )

    async def get_user_contacts(self) -> List[UserContact]:
        """
        Получить контактные данные пользователя
        Returns:
            List[UserContact]

        """
        return await self.get(
            "https://authedu.mosreg.ru/v1/user/contacts",
            model=UserContact,
            params={
                "source": "CONTINGENT",
            },
            is_list=True,
        )

    async def get_organisations(
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
        return await self.get(
            "https://authedu.mosreg.ru/v1/nsi/organisations",
            model=WebOrganizations,
            params={
                "page": page,
                "size": size,
                "organizationId": organization_id,
                "timeout": timeout,
            }
        )
    
    get_organizations = get_organisations
