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
    UserChildrens,
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
        """Авторизоваться и получить токен напрямую через обычный логин и пароль."""
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
        return await self.handle_action(
            response=login_response,
            action=login_json.get("action", None),
            failed=login_json.get("failed", None)
        )
    
    async def esia_enter_mfa(self, code: int) -> str:
        """2 этап получения API-TOKEN прохождение MFA: ввод кода"""
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
        """Получите информацию о пользователе."""
        return await self.get("https://authedu.mosreg.ru/v3/userinfo", model=UserInfo)
    
    async def refresh_token(self, role_id: int = None, subsystem: int = None) -> str:
        """Обновите токен."""
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
        """Получите сообщения системы."""
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
        """Получите информацию о пользователе аккаунта."""
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
        """Получите список учебных годов."""
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
        """Получите информацию о пользователе или пользователях."""
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
        """Получите информацию о студенте или студентах."""
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
        """Получите информацию о студенте или студентах."""
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
        """Получите полную подробную информацию о пользователе."""
        return await self.get(
            f"https://authedu.mosreg.ru/api/persondata/v1/persons/{person_id}",
            {
                "x-mes-subsystem": "headerweb",
            },
            model=PersonData,
        )
    
    async def get_all_roles_global(self) -> List[Role]:
        """Получите список всех ролей."""
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
        """Получите расписание."""
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
    
    async def get_children(self, sso_id: str, timeout: int = 10) -> UserChildrens:
        """Получите подробную информацию о всех детей."""
        return await self.get(
            "https://authedu.mosreg.ru/v1/user/childrens",
            model=UserChildrens,
            params={
                "sso_id": sso_id,
                "timeout": timeout
            }
        )

    async def get_user_contacts(self) -> List[UserContact]:
        """Получите контактные данные о пользователе."""
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
        """Получите информацию о всех организациях."""
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
