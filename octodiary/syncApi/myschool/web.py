#    ____       _        _____  _                  
#   / __ \     | |      |  __ \(_)                 
#  | |  | | ___| |_ ___ | |  | |_  __ _ _ __ _   _ 
#  | |  | |/ __| __/ _ \| |  | | |/ _` | '__| | | |
#  | |__| | (__| || (_) | |__| | | (_| | |  | |_| |
#   \____/ \___|\__\___/|_____/|_|\__,_|_|   \__, |
#                                             __/ |
#                                            |___/ 
# 
#                 © Copyright 2023
#        🔒 Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import http.cookiejar as cookielib
import re
from datetime import date
from typing import List, Union

from requests import Response
from requests.utils import dict_from_cookiejar

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

from ..base import SyncBaseApi


class SyncWebAPI(SyncBaseApi):
    """
    Sync Web API class wrapper.
    """

    def login(self, username: str, password: str) -> str:
        """Авторизоваться и получить токен напрямую через обычный логин и пароль."""
        return (
            self.get(
                url="https://authedu.mosreg.ru/v3/auth/kauth/callback",
                required_token=False, return_raw_response=True,
                params={
                    "code": (
                        self.post(
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
        ).cookies["aupd_token"]

    def handle_action(self, response: Response, action: str = None, failed: str = None) -> str | bool:
        match action or failed:
            case None:
                return None
            case "FILL_MFA":
                return (
                    dict_from_cookiejar(
                        self.__login_request(
                            self.session.get(
                                self.__login_request(
                                    self.session.post(
                                        "https://esia.gosuslugi.ru/aas/oauth2/api/login/promo-mfa/fill-mfa?decision=false",
                                        cookies=self.__cookies
                                    )
                                ).json().get("redirect_url", "")
                            )
                        ).cookies
                    )["aupd_token"]
                )
            case "DONE":
                return dict_from_cookiejar(
                    self.__login_request(self.session.get(response.json().get("redirect_url", ""))).cookies
                )["aupd_token"]
            case "GRANT_SCOPE_ACCESS":
                response = self.__login_request(
                    self.session.post(
                        url="https://esia.gosuslugi.ru/aas/oauth2/api/scope/allow"
                    )
                )
                resp_json = response.json()
                return self.handle_action(
                    response=response,
                    action=resp_json.get("action", None),
                    failed=resp_json.get("failed", None)
                )
            case "ENTER_MFA":
                return False
            case other_action_or_failed:
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
                "https://authedu.mosreg.ru/v3/auth/esia/login",
                allow_redirects=False
            )
        ).text
        self.__login_request(self.session.get(re.findall(r"0\;url\=(.*?)\">", one)[0], cookies=self.__cookies))
        self.__login_request(self.session.get("https://esia.gosuslugi.ru/aas/oauth2/config", cookies=self.__cookies))
        login = self.__login_request(self.session.post(
            "https://esia.gosuslugi.ru/aas/oauth2/api/login",
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
        enter_mfa = self.__login_request(
            self.session.post(
                f"https://esia.gosuslugi.ru/aas/oauth2/api/login/totp/verify?code={code}",
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
        """Получите информацию о пользователе."""
        return self.get("https://authedu.mosreg.ru/v3/userinfo", model=UserInfo)
    
    def refresh_token(self, roleId: int = None, subsystem: int = None) -> str:
        """Обновите токен."""
        return self.get(
            "https://authedu.mosreg.ru/v2/token/refresh",
            params={"roleId": roleId, "subsystem": subsystem},
            return_raw_text=True
        )
    
    def get_system_messages(
        self,
        published: bool = True,
        today: bool = True,
        profile_id: int = None,
        profile_type: str = None,
        pid: int = None
    ) -> List:
        """Получите сообщения системы."""
        return self.get(
            "https://myschool.mosreg.ru/acl/api/system_messages",
            custom_headers={
                "Accept": "application/json",
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            params={"pid": pid, "published": published, "today": today},
            return_json=True
        )
    
    def get_session_info(self) -> SessionUserInfo:
        """Получите информацию о пользователе аккаунта."""
        return self.post(
            "https://myschool.mosreg.ru/lms/api/sessions",
            {
                "auth_token": self.token,
                "Content-Type":"application/json;charset=utf-8",
            },
            json={"auth_token": self.token},
            model=SessionUserInfo,
        )

    def get_academic_years(
        self,
        profile_id: int = None,
        profile_type: str = None,
        pid: int = None
    ) -> List[AcademicYear]:
        """Получите список учебных годов."""
        return self.get(
            "https://myschool.mosreg.ru/core/api/academic_years",
            {
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            params={"pid": pid},
            model=AcademicYear,
            is_list=True,
        )
    
    def get_user(
        self,
        ids: Union[int, List[int]] = 1,
        pid: int = None,
        profile_id: int = None,
        profile_type: str = None
    ) -> Union[User, List[User]]:
        """Получите информацию о пользователе или пользователях."""
        return self.get(
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
    
    def get_student_profiles(
        self,
        academic_year_id: int = 0,
        page: int = 1,
        per_page: int = 50,
        pid: int = None,
        profile_id: int = None,
        profile_type: str = None
    ) -> Union[StudentProfile, List[StudentProfile]]:
        """Получите информацию о студенте или студентах."""
        return self.get(
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

    def get_family_web_profile(
        self,
        profile_id: int = None,
        profile_type: str = None,
        nocache: bool = True
    ) -> WebFamilyProfile:
        """Получите информацию о студенте или студентах."""
        return self.get(
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
    
    def get_person_data(self, person_id: str) -> PersonData:
        """Получите полную подробную информацию о пользователе."""
        return self.get(
            f"https://authedu.mosreg.ru/api/persondata/v1/persons/{person_id}",
            {
                "x-mes-subsystem": "headerweb",
            },
            model=PersonData,
        )
    
    def get_all_roles_global(self) -> List[Role]:
        """Получите список всех ролей."""
        return self.get(
            "https://authedu.mosreg.ru/v1/roles/allGlobal/",
            model=Role, is_list=True, required_token=False
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
    
    def get_childrens(self, sso_id: str, timeout: int = 10) -> UserChildrens:
        """Получите подробную информацию о всех детей."""
        return self.get(
            "https://authedu.mosreg.ru/v1/user/childrens",
            model=UserChildrens,
            params={
                "sso_id": sso_id,
                "timeout": timeout
            }
        )

    def get_user_contacts(self) -> List[UserContact]:
        """Получите контактные данные о пользователе."""
        return self.get(
            "https://authedu.mosreg.ru/v1/user/contacts",
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
        """Получите информацию о всех организациях."""
        return self.get(
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
    


