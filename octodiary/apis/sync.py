#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import base64
import hashlib
import http.cookiejar as cookielib
import random
import re
import string
from datetime import date
from typing import Optional, Union

from requests import Response
from requests.utils import dict_from_cookiejar

from octodiary.apis.base import SyncBaseAPI
from octodiary.exceptions import APIError
from octodiary.types import web
from octodiary.types.captcha import generate_captcha_class
from octodiary.types.enter_sms_code import EnterSmsCode
from octodiary.types.mobile import (
    ClassMembers,
    DayBalanceInfo,
    EventsResponse,
    FamilyProfile,
    FamilyStatus,
    LessonScheduleItem,
    Marks,
    MealsClients,
    Notification,
    ParallelCurriculum,
    PeriodsSchedules,
    PersonData,
    RatingRankClass,
    RatingRankShort,
    RatingRankSubject,
    SchoolInfo,
    ShortHomeworks,
    ShortSubjectMarks,
    SubjectMarksForSubject,
    Subjects,
    UserChildrens,
    UserSettings,
    UsersProfilesInfo,
    Visits,
)
from octodiary.types.mobile.subject_marks import SubjectsMarks
from octodiary.types.web import SessionUserInfo
from octodiary.urls import BaseURL, Systems, URLTypes


class SyncMobileAPI(SyncBaseAPI):
    """
    Sync Mobile API class wrapper.
    """

    def login(self, username: str, password: str) -> str:
        """
        Logs in a user with the given username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            str: The authentication token for the logged-in user.
        """

        if self.system == Systems.MYSCHOOL:
            return (
                self.request(
                    method="get",
                    base_url=BaseURL(type=URLTypes.DNEVNIK, system=Systems.MYSCHOOL),
                    path="/v3/auth/kauth/callback",
                    required_token=False, return_raw_response=True,
                    params={
                        "code": (
                            self.request(
                                method="post",
                                base_url=BaseURL(type=URLTypes.DNEVNIK, system=Systems.MYSCHOOL),
                                path="/lms/api/sessions",
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
        else:
            self.session.cookies = cookielib.CookieJar()

            get_variables = self.session.post(
                BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/oauth/register",
                headers={"Authorization": "Bearer FqzGn1dTJ9BQCHgV0rmMjtYFIgaFf9TrGVEzgtju-zbtIbeJSkIyDcl0e2QMirTNpEqovTT8NvOLZI0XklVEIw"},
                json={
                    "software_id": "dnevnik.mos.ru",
                    "device_type": "android_phone",
                    "software_statement": "eyJ0eXAiOiJKV1QiLCJibGl0ejpraW5kIjoiU09GVF9TVE0iLCJhbGciOiJSUzI1NiJ9.eyJncmFudF90eXBlcyI6WyJhdXRob3JpemF0aW9uX2NvZGUiLCJwYXNzd29yZCIsImNsaWVudF9jcmVkZW50aWFscyIsInJlZnJlc2hfdG9rZW4iXSwic2NvcGUiOiJiaXJ0aGRheSBibGl0el9jaGFuZ2VfcGFzc3dvcmQgYmxpdHpfYXBpX3VzZWNfY2hnIGJsaXR6X3VzZXJfcmlnaHRzIGNvbnRhY3RzIG9wZW5pZCBwcm9maWxlIGJsaXR6X3JtX3JpZ2h0cyBibGl0el9hcGlfc3lzX3VzZXJfY2hnIGJsaXR6X2FwaV9zeXNfdXNlcnMgYmxpdHpfYXBpX3N5c191c2Vyc19jaGcgc25pbHMgYmxpdHpfYXBpX3N5c191c2VjX2NoZyBibGl0el9xcl9hdXRoIiwianRpIjoiYTVlM2NiMGQtYTBmYi00ZjI1LTk3ODctZTllYzRjOTFjM2ZkIiwic29mdHdhcmVfaWQiOiJkbmV2bmlrLm1vcy5ydSIsInNvZnR3YXJlX3ZlcnNpb24iOiIxIiwicmVzcG9uc2VfdHlwZXMiOlsiY29kZSIsInRva2VuIl0sImlhdCI6MTYzNjcyMzQzOSwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5tb3MucnUiLCJyZWRpcmVjdF91cmlzIjpbImh0dHA6Ly9sb2NhbGhvc3QiLCJzaGVsbDovL2F1dGhwb3J0YWwiLCJkbmV2bmlrLW1lczovL29hdXRoMnJlZGlyZWN0IiwiaHR0cHM6Ly9zY2hvb2wubW9zLnJ1L2F1dGgvbWFpbi9jYWxsYmFjayIsImh0dHBzOi8vc2Nob29sLm1vcy5ydS92MS9vYXV0aC9jYWxsYmFjayIsImh0dHBzOi8vZG5ldm5pay5tb3MucnUvc3VkaXIiLCJodHRwczovL3NjaG9vbC5tb3MucnUvYXV0aC9jYWxsYmFjayIsImh0dHA6Ly9kbmV2bmlrLm1vcy5ydS9zdWRpciJdLCJhdWQiOlsiZG5ldm5pay5tb3MucnUiXX0.EERWGw5RGhLQ1vBiGrdG_eJrCyJEyan-H4UWT1gr4B9ZfP58pyJoVw5wTt8YFqzwbvHNQBnvrYfMCzOkHpsU7TxlETJpbWcWbnV5JI-inzXGyKCic2fAVauVCjos3v6AFiP6Uw6ZXIC6b9kQ5WgRVM66B9UwAB2MKTThTohJP7_MNZJ0RiOd8RLlvF4C7yfuqoGU2-KWLwr78ATniTvYFWszl8jAi_SiD9Ai1GWW4mO9-JQ01f4N9umC5Cy2tYiZhxbaz2rOsAQBBjY6rbCCJbCpb1lyGfs2qhhAB-ODGTq7W7r1WBlAm5EXlPpuW_9pi8uxdxiqjkG3d6xy7h7gtQ"
                }
            ).json()

            self.client_id = get_variables["client_id"]
            self.client_secret = get_variables["client_secret"]

            self.code_verifier = "".join(random.choices(string.ascii_letters + string.digits + "_-", k=80))  # noqa: S311
            self.code_challenge = base64.urlsafe_b64encode(
                hashlib.sha256(self.code_verifier.encode()).digest()
            ).decode().replace("=", "")

            proof_of_work = self._resolve_proof_of_work(
                next(
                    item["proofOfWork"]
                    for item in (
                        (
                            self.session.get(
                                self.init_params(
                                    url=BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/oauth/ae",
                                    params={
                                        "response_type": "code",
                                        "scope": "birthday+contacts+openid+profile+snils+blitz_change_password+blitz_user_rights+blitz_qr_auth",
                                        "access_type": "offline",
                                        "display": "script",
                                        "client_id": self.client_id,
                                        "bip_action_hint": "used_sms",
                                        "code_challenge": self.code_challenge,
                                        "code_challenge_method": "S256",
                                        "redirect_uri": "dnevnik-mes%3A%2F%2Foauth2redirect"
                                    }
                                )
                            )
                        ).json()
                    )["items"]
                    if item["inquire"] == "login_with_password"
                )
            )
            resp = self.session.post(
                BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/login/methods/headless/password",
                json={
                    "login": username,
                    "password": password,
                    "proofOfWork": proof_of_work
                }
            )

            return self._handle_login_response(resp, resp.json())

    def handle_action(self, response: Response, action: Optional[str] = None, failed: Optional[str] = None) -> str | bool:
        match failed or action:
            case None:
                return None
            case "DONE":
                self._mfa_details = None
                return dict_from_cookiejar(
                    self.__login_request(self.session.get(url=response.json().get("redirect_url", ""))).cookies
                )["aupd_token"]
            case "GRANT_SCOPE_ACCESS":
                response = self.__login_request(
                    self.session.post(
                        url=BaseURL(type=URLTypes.AUTH, system=Systems.MYSCHOOL) + "/aas/oauth2/api/scope/allow"
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
                    error_types=other_action_or_failed,
                    description="Esia Authorization error.",
                    details=response.json()
                )

    def _handle_login_response(self, response: Response, json: dict) -> str | EnterSmsCode:
        for error in json.get("errors", []):
            match error["code"]:
                case "invalid_credentials":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="InvalidCredentials",
                        description="Invalid credentials",
                        details=json
                    )
                case "pswd_method_temp_locked":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="TemporarilyBlocked",
                        description="Account is temporarily blocked",
                        details=json
                    )
                case "no_subject_found":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="NotFound",
                        description="The account with the passed login was not found",
                        details=json
                    )
                case "no_attempts":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="NoAttempts",
                        description="Number of code verification attempts has expired",
                        details=json
                    )
                case "expired":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="CodeExpired",
                        description="Code verification has expired",
                        details=json
                    )
                case "invalid_otp":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="InvalidOTP",
                        description="Invalid OTP code",
                        details=json
                    )
                case _:
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types=error["code"],
                        details=json
                    )


        for item in json.get("items", []):
            match item["inquire"]:
                case "ask_to_send_sms" | "go_to_web":
                    resp = self.session.post(
                        BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/login/methods/headless/sms/bind",
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )
                    return self._handle_login_response(resp, resp.json())


        if json.get("inquire", None) == "enter_sms_code":
            json["api_class"] = self
            return EnterSmsCode.model_validate(json)
        elif json.get("trust_code", None):
            self.trust_code = json["trust_code"]
            auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
            resp = self.session.post(
                self.init_params(
                    url=BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/oauth/te",
                    params={
                        "grant_type": "authorization_code",
                        "code": self.trust_code,
                        "redirect_uri": "dnevnik-mes://oauth2redirect",
                        "code_verifier": self.code_verifier
                    }
                ),
                headers={"Authorization": f"Basic {auth_header}"}
            ).json()
            self.token_for_refresh = resp["refresh_token"]
            access_token = resp["access_token"]
            self.token = self.session.post(
                BaseURL(type=URLTypes.SCHOOL, system=Systems.MES) + "/v3/auth/sudir/auth",
                json={
                    "user_authentication_for_mobile_request": {
                        "mos_access_token": access_token
                    }
                }
            ).json()["user_authentication_for_mobile_response"]["mesh_access_token"]
            return self.token
        elif response.status_code == 200 and (token := dict_from_cookiejar(response.cookies).get("aupd_token")):
            return token

        return None

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
                url=BaseURL(type=URLTypes.DNEVNIK, system=Systems.MYSCHOOL) + "/v3/auth/esia/login",
                allow_redirects=False
            )
        ).text
        self.__login_request(self.session.get(re.findall(r"0\;url\=(.*?)\">", one)[0], cookies=self.__cookies))
        self.__login_request(self.session.get(BaseURL(type=URLTypes.AUTH, system=Systems.MYSCHOOL) + "/aas/oauth2/config", cookies=self.__cookies))
        login = self.__login_request(self.session.post(
            BaseURL(type=URLTypes.AUTH, system=Systems.MYSCHOOL) + "/aas/oauth2/api/login",
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
                url=BaseURL(type=URLTypes.AUTH, system=Systems.MYSCHOOL) + f"/aas/oauth2/api/login/{mfa_method}/verify?code={code}",
                cookies=self.__cookies
            )
        )
        enter_mfa_json = enter_mfa.json()
        return self.handle_action(
            response=enter_mfa,
            action=enter_mfa_json.get("action", None),
            failed=enter_mfa_json.get("failed", None)
        )

    def get_users_profile_info(self) -> list[UsersProfilesInfo]:
        """
        Retrieves the profiles information of multiple users.

        Returns:
            A list of `UsersProfilesInfo` objects representing the profiles information of multiple users.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(
                type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK,
                system=self.system
            ),
            path="/acl/api/users/profile_info",
            custom_headers={
                "partner-source-id": "MOBILE"
            },
            model=UsersProfilesInfo,
            is_list=True
        )

    def get_family_profile(self, profile_id: int) -> FamilyProfile:
        """
        Get the family profile for a specific person.

        Args:
            profile_id (int): The ID of the person.

        Returns:
            FamilyProfile: The family profile of the person.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/profile",
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            model=FamilyProfile
        )

    def get_status(self, profile_id: int, contract_ids: str) -> FamilyStatus:
        """
        Retrieves the status of a family given the profile ID and contract IDs.

        Args:
            profile_id (int): The ID of the profile.
            contract_ids (str): The contract IDs.

        Returns:
            FamilyStatus: The family status object.

        Raises:
            None.
        """
        if self.system != Systems.MES:
            return False

        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/status",
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "contract_ids": contract_ids
            },
            model=FamilyStatus
        )

    def get_user_settings_app(
            self,
            profile_id: int,
            name: str = "settings_group_v1",
            subsystem_id: int = 1
    ) -> UserSettings:
        """
        Get user settings

        Args:
            profile_id (int): The ID of the profile.
            name (str, optional): The name of the settings group. Defaults to "settings_group_v1".
            subsystem_id (int, optional): The ID of the subsystem. Defaults to 1.

        Returns:
            UserSettings: The user settings object.

        Raises:
            None.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK if self.system == Systems.MYSCHOOL else URLTypes.SCHOOL, system=self.system),
            path="/api/usersettings/v1",
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
        Edit user settings

        Args:
            settings (UserSettings): The user settings object.
            profile_id (int): The ID of the profile.
            name (str, optional): The name of the settings group. Defaults to "settings_group_v1".
            subsystem_id (int, optional): The ID of the subsystem. Defaults to 1.
        """
        self.request(
            method="PUT",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/api/usersettings/v1",
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
        """
        Retrieves events for a given person.

        Args:
            person_id (str): The ID of the person for whom to retrieve events.
            mes_role (str): The role of the person in the system.
            begin_date (Optional[date], optional): The start date of the event range. Defaults to None.
            end_date (Optional[date], optional): The end date of the event range. Defaults to None.
            expand (str, optional): The fields to expand in the events response. Defaults to "marks,homework,absence_reason_id,health_status,nonattendance_reason_id".

        Returns:
            EventsResponse: The events response object.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MES else URLTypes.DNEVNIK, system=self.system),
            path="/api/eventcalendar/v1/api/events",
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
            from_date: Optional[date] = None,
            to_date: Optional[date] = None,
            sort_column: str = "date",
            sort_direction: str = "asc",
    ) -> ShortHomeworks:
        """
        Retrieves a list of short homeworks for a given student within a specified date range.

        Args:
            student_id (int): The ID of the student.
            profile_id (int): The ID of the profile.
            from_date (date): The start date of the range.
            to_date (date): The end date of the range.
            sort_column (str, optional): The column to sort the homeworks by. Defaults to "date".
            sort_direction (str, optional): The direction to sort the homeworks in. Defaults to "asc".

        Returns:
            ShortHomeworks: The short homeworks object.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/homeworks/short",
            params={
                "student_id": student_id,
                "from": self.date_to_string(from_date),
                "to": self.date_to_string(to_date),
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
            from_date: Optional[date] = None,
            to_date: Optional[date] = None
    ) -> Marks:
        """
        Get marks for a specific student within a given date range.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.
            from_date (date): The start date of the date range.
            to_date (date): The end date of the date range.

        Returns:
            Marks: The marks for the student within the specified date range.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/marks",
            params={
                "student_id": student_id,
                "from": self.date_to_string(from_date),
                "to": self.date_to_string(to_date),
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
    ) -> list[PeriodsSchedules]:
        """
        Retrieves the periods schedules for a specific profile and student within a given date range.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.
            from_date (date): The start date of the range.
            to_date (date): The end date of the range.

        Returns:
            list[PeriodsSchedules]: A list of PeriodsSchedules objects representing the periods schedules within the specified date range.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/periods_schedules",
            params={
                "student_id": student_id,
                "from": self.date_to_string(from_date),
                "to": self.date_to_string(to_date),
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            },
            model=PeriodsSchedules,
            is_list=True
        )

    def get_subject_marks_short(
            self,
            student_id: int,
            profile_id: int,
    ) -> ShortSubjectMarks:
        """
        Retrieve the short subject marks for a specific student.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.

        Returns:
            ShortSubjectMarks: The short subject marks for the student.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/subject_marks/short",
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
    ) -> Subjects:
        """
        Retrieves the list of subjects for a specific student and profile.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.

        Returns:
            Subjects: An instance of the Subjects class containing the list of subjects.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/subjects/list",
            model=Subjects,
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
        Get parallel curriculum

        Args:
            id (int): The ID of the program.
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.

        Returns:
            ParallelCurriculum: The parallel curriculum.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path=f"/family/mobile/v1/programs/parallel_curriculum/{id}",
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
        Fetches the person data for a given person ID and profile ID.

        Args:
            person_id (str): The ID of the person.
            profile_id (int): The ID of the profile.

        Returns:
            PersonData: The person data.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
            path=f"/api/persondata/mobile/persons/{person_id}",
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
        Get user childrens

        Args:
            person_id (str): The ID of the person.

        Returns:
            UserChildrens: The user childrens.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/v1/user/childrens",
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
        Retrieve a list of notifications for a specific student.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.

        Returns:
            List[Notification]: A list of Notification objects representing the notifications.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/notifications/search",
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
        Get subject marks for subject

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.
            subject_name (int): The name of the subject.

        Returns:
            SubjectMarksForSubject: The subject marks for subject.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/subject_marks/for_subject",
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

    def get_lesson_schedule_item(
            self,
            profile_id: int,
            lesson_id: int,
            student_id: int,
            type: str = "PLAN"
    ) -> LessonScheduleItem:
        """
        Retrieves a schedule item for a given profile, lesson, and student.

        Args:
            profile_id (int): The ID of the profile.
            lesson_id (int): The ID of the lesson.
            student_id (int): The ID of the student.
            type (str, optional): The type of schedule item. Defaults to "PLAN".

        Returns:
            LessonScheduleItem: The retrieved schedule item.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path=f"/family/mobile/v1/lesson_schedule_items/{lesson_id}",
            params={
                "student_id": student_id,
                "type": type
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            model=LessonScheduleItem
        )

    def get_rating_rank_class(
            self,
            profile_id: int,
            person_id: str,
            class_unit_id: int,
            date: Optional[date] = None
    ) -> list[RatingRankClass]:
        """
        Retrieves the class rating

        Args:
            profile_id (int): The ID of the profile.
            person_id (str): The ID of the person.
            class_unit_id (int): The ID of the class unit.
            date (Optional[date], optional): The date of the rating. Defaults to None.

        Returns:
            list[RatingRankClass]: The class rating.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/api/ej/rating/v1/rank/class",
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

    def get_rating_rank_short(
            self,
            profile_id: int,
            person_id: str,
            begin_date: Optional[date] = None,
            end_date: Optional[date] = None
    ) -> list[RatingRankShort]:
        """
        Retrieves the short class rating

        Args:
            profile_id (int): The ID of the profile.
            person_id (str): The ID of the person.
            begin_date (date): The start date of the rating.
            end_date (date): The end date of the rating.

        Returns:
            list[RatingRankShort]: The short class rating.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/api/ej/rating/v1/rank/rankShort",
            model=RatingRankShort, is_list=True,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "personId": person_id,
                "beginDate": self.date_to_string(begin_date),
                "endDate": self.date_to_string(end_date),
            }
        )

    def get_rating_rank_subjects(
            self,
            profile_id: int,
            person_id: str,
            date: Optional[date] = None
    ) -> list[RatingRankSubject]:
        """
        Retrieves the subject rating

        Args:
            profile_id (int): The ID of the profile.
            person_id (str): The ID of the person.
            date (date): The date of the rating.

        Returns:
            list[RatingRankSubject]: The subject rating.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/api/ej/rating/v1/rank/subjects",
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

    def refresh_token(self, token: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> str:
        """
        Refreshes the token and returns the refreshed token as a string.

        Args:
            token (str, optional): The token to refresh. Defaults to None.
            client_id (str, optional): The client id. Defaults to None.
            client_secret (str, optional): The client secret. Defaults to None.

        Returns:
            str: The refreshed token.
        """
        if self.system == Systems.MYSCHOOL:
            token = self.request(
                method="GET",
                base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
                path="/v2/token/refresh",
                return_raw_text=True
            )
        else:
            access_token_resp = self.request(
                method="POST",
                base_url=BaseURL(type=URLTypes.AUTH, system=self.system),
                path="/sps/oauth/te",
                params={
                    "refresh_token": token or getattr(self, "token_for_refresh", ""),
                    "grant_type": "refresh_token"
                },
                custom_headers={
                    "Authorization": "Basic " + base64.b64encode(f"{client_id or getattr(self, 'client_id', '')}:{client_secret or getattr(self, 'client_secret', '')}".encode()).decode()
                },
                required_token=False,
                return_json=True
            )
            self.token_for_refresh = access_token_resp["refresh_token"]
            access_token = access_token_resp["access_token"]
            token = self.request(
                method="POST",
                base_url=BaseURL(type=URLTypes.SCHOOL, system=self.system),
                path="/v3/auth/sudir/auth",
                json={
                    "user_authentication_for_mobile_request": {
                        "mos_access_token": access_token
                    }
                },
                return_json=True,
                required_token=False
            )["user_authentication_for_mobile_response"]["mesh_access_token"]
        self.token = token
        return token

    def get_school_info(self, profile_id: int, school_id: int, class_unit_id: int) -> SchoolInfo:
        """
        Retrieves the information of a school for a specific student.

        Args:
            profile_id (int): The ID of the profile.
            school_id (int): The ID of the school.
            class_unit_id (int): The ID of the class unit.

        Returns:
            SchoolInfo: An object containing the information of the school.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/school_info",
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "school_id": school_id,
                "class_unit_id": class_unit_id
            },
            model=SchoolInfo
        )

    def get_visits(self, profile_id: int, student_id: int, contract_id: str, from_date: date, to_date: date) -> Visits:
        """
        [MES] Retrieves the visits for a specific student within a given date range.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.
            contract_id (str): The ID of the contract.
            from_date (date): The starting date of the range.
            to_date (date): The ending date of the range.

        Returns:
            Visits: The visits for the specified student within the given date range.
        """
        if self.system == Systems.MYSCHOOL:
            return

        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/visits",
            model=Visits,
            params={
                "student_id": student_id,
                "contract_id": contract_id,
                "from": self.date_to_string(from_date),
                "to": self.date_to_string(to_date),
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            }
        )

    def get_meals_clients(self, profile_id: int, contract_id: str):
        """
        Retrieves the meals clients for a specific student and contract.

        Args:
            profile_id (int): The ID of the profile.
            contract_id (str): The ID of the contract.

        Returns:
            MealsClients: The meals clients for the specified student and contract.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK if self.system == Systems.MES else URLTypes.SCHOOL, system=self.system),
            path="/api/meals/v1/clients",
            params={
                "contract_id": contract_id,
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "profile-id": profile_id,
                "client-type": "diary-mobile"
            },
            model=MealsClients
        )

    def get_day_balance_info(self, profile_id: int, contract_id: str, first: int = 14, after: date | None = None) -> DayBalanceInfo:
        """
        Retrieve the day balance information for a specific profile and contract.

        Args:
            profile_id (int): The ID of the profile.
            contract_id (str): The ID of the contract.
            first (int, optional): The number of records to retrieve. Defaults to 14.
            after (date, optional): The date to start retrieving records from. Defaults to None.

        Returns:
            DayBalanceInfo: An object containing the day balance information.
        """
        if self.system == Systems.MYSCHOOL:
            return False

        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/day_balance_info",
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "contract_id": contract_id,
                "first": first,
                **(
                    {
                        "after": self.date_to_string(after)
                    } if after else {}
                )
            },
            model=DayBalanceInfo
        )

    def get_class_members(self, class_unit_id: int, per_page: int = 2147483647, types: str = "student") -> ClassMembers:
        """
        Retrieves the members of a class.

        Args:
            class_unit_id (int): The ID of the class.
            per_page (int, optional): The number of records to retrieve. Defaults to JAVA_MAX_INT(2147483647).
            types (str, optional): The types of members to retrieve. Defaults to "student".
        """

        return (
            self.request(
                method="GET",
                base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
                path="/core/api/profiles",
                params={
                    "class_unit_id": class_unit_id,
                    "per_page": per_page,
                    "types": types
                },
                model=ClassMembers
            )
        ).root

    def get_subjects_marks(self, profile_id: int, student_id: int) -> SubjectsMarks:
        """
        Retrieves the subjects marks for a specific student.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.

        Returns:
            SubjectsMarks: The subjects marks for the specified student.
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL_API, system=self.system),
            path="/family/mobile/v1/subject_marks",
            params={
                "student_id": student_id,
            },
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id,
            },
            model=SubjectsMarks,
        )


class SyncWebAPI(SyncBaseAPI):
    """
    Sync Web API class wrapper.
    """

    def login(self, username: str, password: str) -> str:
        """
        Logs in a user with the given username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            str: The authentication token for the logged-in user.
        """

        if self.system == Systems.MYSCHOOL:
            return (
                self.request(
                    method="get",
                    base_url=BaseURL(type=URLTypes.DNEVNIK, system=Systems.MYSCHOOL),
                    path="/v3/auth/kauth/callback",
                    required_token=False, return_raw_response=True,
                    params={
                        "code": (
                            self.request(
                                method="post",
                                base_url=BaseURL(type=URLTypes.DNEVNIK, system=Systems.MYSCHOOL),
                                path="/lms/api/sessions",
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
        else:
            self.session.cookies = cookielib.CookieJar()

            get_variables = self.session.post(
                BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/oauth/register",
                headers={"Authorization": "Bearer FqzGn1dTJ9BQCHgV0rmMjtYFIgaFf9TrGVEzgtju-zbtIbeJSkIyDcl0e2QMirTNpEqovTT8NvOLZI0XklVEIw"},
                json={
                    "software_id": "dnevnik.mos.ru",
                    "device_type": "android_phone",
                    "software_statement": "eyJ0eXAiOiJKV1QiLCJibGl0ejpraW5kIjoiU09GVF9TVE0iLCJhbGciOiJSUzI1NiJ9.eyJncmFudF90eXBlcyI6WyJhdXRob3JpemF0aW9uX2NvZGUiLCJwYXNzd29yZCIsImNsaWVudF9jcmVkZW50aWFscyIsInJlZnJlc2hfdG9rZW4iXSwic2NvcGUiOiJiaXJ0aGRheSBibGl0el9jaGFuZ2VfcGFzc3dvcmQgYmxpdHpfYXBpX3VzZWNfY2hnIGJsaXR6X3VzZXJfcmlnaHRzIGNvbnRhY3RzIG9wZW5pZCBwcm9maWxlIGJsaXR6X3JtX3JpZ2h0cyBibGl0el9hcGlfc3lzX3VzZXJfY2hnIGJsaXR6X2FwaV9zeXNfdXNlcnMgYmxpdHpfYXBpX3N5c191c2Vyc19jaGcgc25pbHMgYmxpdHpfYXBpX3N5c191c2VjX2NoZyBibGl0el9xcl9hdXRoIiwianRpIjoiYTVlM2NiMGQtYTBmYi00ZjI1LTk3ODctZTllYzRjOTFjM2ZkIiwic29mdHdhcmVfaWQiOiJkbmV2bmlrLm1vcy5ydSIsInNvZnR3YXJlX3ZlcnNpb24iOiIxIiwicmVzcG9uc2VfdHlwZXMiOlsiY29kZSIsInRva2VuIl0sImlhdCI6MTYzNjcyMzQzOSwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5tb3MucnUiLCJyZWRpcmVjdF91cmlzIjpbImh0dHA6Ly9sb2NhbGhvc3QiLCJzaGVsbDovL2F1dGhwb3J0YWwiLCJkbmV2bmlrLW1lczovL29hdXRoMnJlZGlyZWN0IiwiaHR0cHM6Ly9zY2hvb2wubW9zLnJ1L2F1dGgvbWFpbi9jYWxsYmFjayIsImh0dHBzOi8vc2Nob29sLm1vcy5ydS92MS9vYXV0aC9jYWxsYmFjayIsImh0dHBzOi8vZG5ldm5pay5tb3MucnUvc3VkaXIiLCJodHRwczovL3NjaG9vbC5tb3MucnUvYXV0aC9jYWxsYmFjayIsImh0dHA6Ly9kbmV2bmlrLm1vcy5ydS9zdWRpciJdLCJhdWQiOlsiZG5ldm5pay5tb3MucnUiXX0.EERWGw5RGhLQ1vBiGrdG_eJrCyJEyan-H4UWT1gr4B9ZfP58pyJoVw5wTt8YFqzwbvHNQBnvrYfMCzOkHpsU7TxlETJpbWcWbnV5JI-inzXGyKCic2fAVauVCjos3v6AFiP6Uw6ZXIC6b9kQ5WgRVM66B9UwAB2MKTThTohJP7_MNZJ0RiOd8RLlvF4C7yfuqoGU2-KWLwr78ATniTvYFWszl8jAi_SiD9Ai1GWW4mO9-JQ01f4N9umC5Cy2tYiZhxbaz2rOsAQBBjY6rbCCJbCpb1lyGfs2qhhAB-ODGTq7W7r1WBlAm5EXlPpuW_9pi8uxdxiqjkG3d6xy7h7gtQ"
                }
            ).json()

            self.client_id = get_variables["client_id"]
            self.client_secret = get_variables["client_secret"]

            self.code_verifier = "".join(random.choices(string.ascii_letters + string.digits + "_-", k=80))  # noqa: S311
            self.code_challenge = base64.urlsafe_b64encode(
                hashlib.sha256(self.code_verifier.encode()).digest()
            ).decode().replace("=", "")

            proof_of_work = self._resolve_proof_of_work(
                next(
                    item["proofOfWork"]
                    for item in (
                        (
                            self.session.get(
                                self.init_params(
                                    url=BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/oauth/ae",
                                    params={
                                        "response_type": "code",
                                        "scope": "birthday+contacts+openid+profile+snils+blitz_change_password+blitz_user_rights+blitz_qr_auth",
                                        "access_type": "offline",
                                        "display": "script",
                                        "client_id": self.client_id,
                                        "bip_action_hint": "used_sms",
                                        "code_challenge": self.code_challenge,
                                        "code_challenge_method": "S256",
                                        "redirect_uri": "dnevnik-mes%3A%2F%2Foauth2redirect"
                                    }
                                )
                            )
                        ).json()
                    )["items"]
                    if item["inquire"] == "login_with_password"
                )
            )
            resp = self.session.post(
                BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/login/methods/headless/password",
                json={
                    "login": username,
                    "password": password,
                    "proofOfWork": proof_of_work
                }
            )

            return self._handle_login_response(resp, resp.json())

    def handle_action(self, response: Response, action: Optional[str] = None, failed: Optional[str] = None) -> str | bool:
        match failed or action:
            case None:
                return None
            case "DONE":
                self._mfa_details = None
                return dict_from_cookiejar(
                    self.__login_request(self.session.get(url=response.json().get("redirect_url", ""))).cookies
                )["aupd_token"]
            case "GRANT_SCOPE_ACCESS":
                response = self.__login_request(
                    self.session.post(
                        url=BaseURL(type=URLTypes.AUTH, system=Systems.MYSCHOOL) + "/aas/oauth2/api/scope/allow"
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
                    error_types=other_action_or_failed,
                    description="Esia Authorization error.",
                    details=response.json()
                )

    def _handle_login_response(self, response: Response, json: dict) -> str | EnterSmsCode:
        for error in json.get("errors", []):
            match error["code"]:
                case "invalid_credentials":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="InvalidCredentials",
                        description="Invalid credentials",
                        details=json
                    )
                case "pswd_method_temp_locked":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="TemporarilyBlocked",
                        description="Account is temporarily blocked",
                        details=json
                    )
                case "no_subject_found":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="NotFound",
                        description="The account with the passed login was not found",
                        details=json
                    )
                case "no_attempts":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="NoAttempts",
                        description="Number of code verification attempts has expired",
                        details=json
                    )
                case "expired":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="CodeExpired",
                        description="Code verification has expired",
                        details=json
                    )
                case "invalid_otp":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types="InvalidOTP",
                        description="Invalid OTP code",
                        details=json
                    )
                case _:
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_types=error["code"],
                        details=json
                    )


        for item in json.get("items", []):
            match item["inquire"]:
                case "ask_to_send_sms" | "go_to_web":
                    resp = self.session.post(
                        BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/login/methods/headless/sms/bind",
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )
                    return self._handle_login_response(resp, resp.json())


        if json.get("inquire", None) == "enter_sms_code":
            json["api_class"] = self
            return EnterSmsCode.model_validate(json)
        elif json.get("trust_code", None):
            self.trust_code = json["trust_code"]
            auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
            resp = self.session.post(
                self.init_params(
                    url=BaseURL(type=URLTypes.AUTH, system=Systems.MES) + "/sps/oauth/te",
                    params={
                        "grant_type": "authorization_code",
                        "code": self.trust_code,
                        "redirect_uri": "dnevnik-mes://oauth2redirect",
                        "code_verifier": self.code_verifier
                    }
                ),
                headers={"Authorization": f"Basic {auth_header}"}
            ).json()
            self.token_for_refresh = resp["refresh_token"]
            access_token = resp["access_token"]
            self.token = self.session.post(
                BaseURL(type=URLTypes.SCHOOL, system=Systems.MES) + "/v3/auth/sudir/auth",
                json={
                    "user_authentication_for_mobile_request": {
                        "mos_access_token": access_token
                    }
                }
            ).json()["user_authentication_for_mobile_response"]["mesh_access_token"]
            return self.token
        elif response.status_code == 200 and (token := dict_from_cookiejar(response.cookies).get("aupd_token")):
            return token

        return None

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
                url=BaseURL(type=URLTypes.DNEVNIK, system=Systems.MYSCHOOL) + "/v3/auth/esia/login",
                allow_redirects=False
            )
        ).text
        self.__login_request(self.session.get(re.findall(r"0\;url\=(.*?)\">", one)[0], cookies=self.__cookies))
        self.__login_request(self.session.get(BaseURL(type=URLTypes.AUTH, system=Systems.MYSCHOOL) + "/aas/oauth2/config", cookies=self.__cookies))
        login = self.__login_request(self.session.post(
            BaseURL(type=URLTypes.AUTH, system=Systems.MYSCHOOL) + "/aas/oauth2/api/login",
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
                url=BaseURL(type=URLTypes.AUTH, system=Systems.MYSCHOOL) + f"/aas/oauth2/api/login/{mfa_method}/verify?code={code}",
                cookies=self.__cookies
            )
        )
        enter_mfa_json = enter_mfa.json()
        return self.handle_action(
            response=enter_mfa,
            action=enter_mfa_json.get("action", None),
            failed=enter_mfa_json.get("failed", None)
        )

    def get_user_info(self) -> web.UserInfo:
        """
        Get user info

        Returns:
            UserInfo: user info object
        """
        return self.request(
            method="get",
            base_url=BaseURL(type=URLTypes.DNEVNIK if self.system == Systems.MYSCHOOL else URLTypes.SCHOOL, system=self.system),
            path="/v3/userinfo",
            model=web.UserInfo
        )

    def refresh_token(self, token: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> str:
        """
        Refreshes the token and returns the refreshed token as a string.

        Args:
            token (str, optional): The token to refresh. Defaults to None.
            client_id (str, optional): The client id. Defaults to None.
            client_secret (str, optional): The client secret. Defaults to None.

        Returns:
            str: The refreshed token.
        """
        if self.system == Systems.MYSCHOOL:
            token = self.request(
                method="GET",
                base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
                path="/v2/token/refresh",
                return_raw_text=True
            )
        else:
            access_token_resp = self.request(
                method="POST",
                base_url=BaseURL(type=URLTypes.AUTH, system=self.system),
                path="/sps/oauth/te",
                params={
                    "refresh_token": token or getattr(self, "token_for_refresh", ""),
                    "grant_type": "refresh_token"
                },
                custom_headers={
                    "Authorization": "Basic " + base64.b64encode(f"{client_id or getattr(self, 'client_id', '')}:{client_secret or getattr(self, 'client_secret', '')}".encode()).decode()
                },
                required_token=False,
                return_json=True
            )
            self.token_for_refresh = access_token_resp["refresh_token"]
            access_token = access_token_resp["access_token"]
            token = self.request(
                method="POST",
                base_url=BaseURL(type=URLTypes.SCHOOL, system=self.system),
                path="/v3/auth/sudir/auth",
                json={
                    "user_authentication_for_mobile_request": {
                        "mos_access_token": access_token
                    }
                },
                return_json=True,
                required_token=False
            )["user_authentication_for_mobile_response"]["mesh_access_token"]
        self.token = token
        return token

    def get_system_messages(
            self,
            published: bool = True,
            today: bool = True,
            profile_id: Optional[int] = None,
            profile_type: Optional[str] = None,
            pid: Optional[int] = None
    ) -> list:
        """
        Get system messages

        Args:
            published: bool
            today: bool
            profile_id: int
            profile_type: str
            pid: int

        Returns:
            List: List of system messages
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
            path="/acl/api/system_messages",
            custom_headers={
                "Accept": "application/json",
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            params={"pid": pid, "published": published, "today": today},
            return_json=True
        )

    def get_session_info(self) -> web.SessionUserInfo:
        """
        Get session info

        Returns:
            SessionUserInfo
        """
        return self.request(
            method="POST",
            base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
            path="/lms/api/sessions",
            custom_headers={
                "auth_token": self.token,
                "Content-Type": "application/json;charset=utf-8",
            },
            json={"auth_token": self.token},
            model=web.SessionUserInfo,
        )

    def get_academic_years(
            self,
            profile_id: Optional[int] = None,
            profile_type: Optional[str] = None,
            pid: Optional[int] = None
    ) -> list[web.AcademicYear]:
        """
        Get academic years

        Args:
            profile_id: int
            profile_type: str
            pid: int

        Returns:
            list[AcademicYear]: List of academic years
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
            path="/core/api/academic_years",
            custom_headers={
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            params={"pid": pid},
            model=web.AcademicYear,
            is_list=True,
        )

    def get_user(
            self,
            ids: Union[int, list[int]] = 1,
            pid: Optional[int] = None,
            profile_id: Optional[int] = None,
            profile_type: Optional[str] = None
    ) -> Union[web.User, list[web.User]]:
        """
        Get user

        Args:
            ids: int или list[int]
            pid: int
            profile_id: int
            profile_type: str

        Returns:
            User | list[User]
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
            path="/acl/api/users",
            custom_headers={
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            model=web.User,
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
    ) -> Union[web.StudentProfile, list[web.StudentProfile]]:
        """
        Get student profiles

        Args:
            academic_year_id: int
            page: int
            per_page: int
            pid: int
            profile_id: int
            profile_type: str

        Returns:
            StudentProfile | list[StudentProfile]
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.SCHOOL if self.system == Systems.MYSCHOOL else URLTypes.DNEVNIK, system=self.system),
            path="/core/api/student_profiles",
            custom_headers={
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
            },
            model=web.StudentProfile,
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
    ) -> web.WebFamilyProfile:
        """
        Get family web profile

        Args:
            profile_id: int
            profile_type: str
            nocache: bool

        Returns:
            WebFamilyProfile
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/api/family/web/v1/profile",
            custom_headers={
                "Profile-Id": profile_id,
                "Profile-Type": profile_type,
                "X-mes-subsystem": "familyweb",
            },
            model=web.WebFamilyProfile,
            params={
                "nocache": nocache
            }
        )

    def get_person_data(self, person_id: str) -> PersonData:
        """
        Get person data

        Args:
            person_id: str

        Returns:
            PersonData
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path=f"/api/persondata/v1/persons/{person_id}",
            custom_headers={
                "x-mes-subsystem": "headerweb",
            },
            model=PersonData,
        )

    def get_all_roles_global(self) -> list[web.Role]:
        """
        Get all roles global

        Returns:
            list[Role]
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/v1/roles/allGlobal/",
            model=web.Role, is_list=True, required_token=False
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
        Get events

        Args:
            person_id: ID персоны
            mes_role: Роль
            begin_date: Начало расписания
            end_date: Окончание расписания
            expand: Дополнительные поля

        Returns:
            EventsResponse
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/api/eventcalendar/v1/api/events",
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

    def get_children(self, sso_id: str, timeout: int = 10) -> web.UserChildren:
        """
        Get children

        Args:
            sso_id: str
            timeout: int

        Returns:
            UserChildren
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/v1/user/childrens",
            model=web.UserChildren,
            params={
                "sso_id": sso_id,
                "timeout": timeout
            }
        )

    def get_organisations(
            self,
            organization_id: int,
            page: int = 1,
            size: int = 10,
            timeout: int = 20,
    ) -> web.WebOrganizations:
        """
        Get organisations by id

        Args:
            organization_id: int
            page: int
            size: int
            timeout: int

        Returns:
            WebOrganizations
        """
        return self.request(
            method="GET",
            base_url=BaseURL(type=URLTypes.DNEVNIK, system=self.system),
            path="/v1/nsi/organisations",
            model=web.WebOrganizations,
            params={
                "page": page,
                "size": size,
                "organizationId": organization_id,
                "timeout": timeout,
            }
        )

    get_organizations = get_organisations
