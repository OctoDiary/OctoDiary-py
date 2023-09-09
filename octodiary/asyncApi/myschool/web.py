from datetime import date
from typing import List, Union

from bs4 import BeautifulSoup

from octodiary.types import (
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


class WebAsyncApi(AsyncBaseApi):
    """
    Async Web API class wrapper.
    """

    async def get_esia_login_link(self) -> str:
        """Получите ссылку для входа в систему ЕСИА(Госуслуги)."""
        response: str = await self.get(
            "https://authedu.mosreg.ru/v3/auth/esia/login",
            required_token=False,
            return_raw_text=True,
            allow_redirects=False
        )
        return (
            BeautifulSoup(response, "html.parser")
            .find("head")
            .find("meta")
            .get("content")[5:]
        )

    async def get_user_info(self) -> UserInfo:
        """Получите информацию о пользователе."""
        return await self.get("https://authedu.mosreg.ru/v3/userinfo", model=UserInfo)
    
    async def refresh_token(self, roleId: int = None, subsystem: int = None) -> str:
        """Обновите токен."""
        return await self.get(
            "https://authedu.mosreg.ru/v2/token/refresh",
            params={"roleId": roleId, "subsystem": subsystem},
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
                "Content-Type":"application/json;charset=utf-8",
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
    
    async def get_childrens(self, sso_id: str, timeout: int = 10) -> UserChildrens:
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
