#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from datetime import date
from typing import Optional

from aiohttp import ClientResponse, ClientSession
from aiohttp.cookiejar import CookieJar

from octodiary.asyncApi.base import AsyncBaseApi
from octodiary.exceptions import APIError
from octodiary.types.enter_sms_code import EnterSmsCode
from octodiary.types.mes.mobile import (
    DayBalanceInfo,
    EventsResponse,
    FamilyProfile,
    FamilyStatus,
    LessonScheduleItem,
    Marks,
    MealsClients,
    Notification,
    PeriodsSchedules,
    PersonData,
    SchoolInfo,
    ShortHomeworks,
    ShortSubjectMarks,
    Subjects,
    UsersProfilesInfo,
    Visits,
)
from octodiary.urls import MesURLs


class AsyncMobileAPI(AsyncBaseApi):
    """
    Async Mobile API class wrapper.
    """


    async def _handle_login_response(self, response: ClientResponse, json: dict) -> str | EnterSmsCode:
        for error in json.get("errors", []):
            match error["code"]:
                case "invalid_credentials":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
                        error_type="InvalidCredentials",
                        description="Invalid credentials",
                        details=json
                    )
                case "pswd_method_temp_locked":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
                        error_type="TemporarilyBlocked",
                        description="Account is temporarily blocked",
                        details=json
                    )
                case "no_subject_found":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
                        error_type="NotFound",
                        description="The account with the passed login was not found",
                        details=json
                    )
                case "no_attempts":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
                        error_type="NoAttempts",
                        description="Number of code verification attempts has expired",
                        details=json
                    )
                case "expired":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
                        error_type="CodeExpired",
                        description="Code verification has expired",
                        details=json
                    )
                case "invalid_otp":
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
                        error_type="InvalidOTP",
                        description="Invalid OTP code",
                        details=json
                    )
                case _:
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
                        error_type=error["code"],
                        details=json
                    )


        for item in json.get("items", []):
            match item["inquire"]:
                case "ask_to_send_sms":
                    continue
                case "go_to_web":
                    resp = await self._login_info["session"].post(
                        MesURLs.LOGIN.BIND_SMS_CODE,
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )
                    return await self._handle_login_response(resp, await resp.json())


        if json.get("inquire", None) == "enter_sms_code":
            json["api_class"] = self
            return EnterSmsCode.model_validate(json)
        elif response.status == 200 and (token := response.cookies.get("aupd_token")):
            return token.value

        return None

    async def login(self, username: str, password: str) -> str | EnterSmsCode:
        """
        Logs in a user with the given username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            str: The authentication token for the logged-in user.
        """
        cookie = CookieJar()
        self._login_info = {
            "cookie": cookie,
            "session": ClientSession(cookie_jar=cookie, headers=self.headers(False)),
        }
        proof_of_work = self._resolve_proof_of_work(
            next(
                item["proofOfWork"]
                for item in (
                    await (
                        await self._login_info["session"].get(
                            self.init_params(
                                url=MesURLs.LOGIN.AURHORIZATION_ENDPOINT,
                                params={
                                    "response_type": "code",
                                    "scope": "birthday+contacts+openid+profile+snils+blitz_change_password+blitz_user_rights+blitz_qr_auth",
                                    "access_type": "offline",
                                    "display": "script",
                                    "client_id": "dnevnik.mos.ru",
                                    "redirect_uri": "https%3A%2F%2Fschool.mos.ru%2Fv3%2Fauth%2Fsudir%2Fcallback",
                                    "state": ""
                                }
                            )
                        )
                    ).json()
                )["items"]
                if item["inquire"] == "login_with_password"
            )
        )
        resp = await self._login_info["session"].post(
            MesURLs.LOGIN.AUTH_WITH_LOGIN_AND_PASSWORD,
            json={
                "login": username,
                "password": password,
                "proofOfWork": proof_of_work
            }
        )

        return await self._handle_login_response(resp, await resp.json())

    async def get_events(
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
        return await self.get(
            url=MesURLs.EVENTS,
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

    async def get_users_profiles_info(self) -> list[UsersProfilesInfo]:
        """
        Retrieves the profiles information of multiple users.

        Returns:
            A list of `UsersProfilesInfo` objects representing the profiles information of multiple users.
        """
        return await self.get(url=MesURLs.PROFILE_INFO, model=UsersProfilesInfo, is_list=True)

    async def get_family_profile(self, profile_id: int) -> FamilyProfile:
        """
        Get the family profile for a specific person.

        Args:
            profile_id (int): The ID of the person.

        Returns:
            FamilyProfile: The family profile of the person.
        """
        return await self.get(
            url=MesURLs.MOBILE.FAMILY_PROFILE,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            model=FamilyProfile
        )

    async def get_status(self, profile_id: int, contract_ids: str) -> FamilyStatus:
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
        return await self.get(
            url=MesURLs.MOBILE.STATUS,
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

    async def get_periods_schedules(self, profile_id: int, student_id: int, from_date: date, to_date: date) -> list[PeriodsSchedules]:
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
        return await self.get(
            url=MesURLs.MOBILE.PERIODS_SCHEDULES,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "student_id": student_id,
                "from": self.date_to_string(from_date),
                "to": self.date_to_string(to_date),
            },
            model=PeriodsSchedules,
            is_list=True
        )

    async def get_marks(self, profile_id: int, student_id: int, from_date: date, to_date: date) -> Marks:
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
        return await self.get(
            url=MesURLs.MOBILE.MARKS,
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            params={
                "student_id": student_id,
                "from": self.date_to_string(from_date),
                "to": self.date_to_string(to_date),
            },
            model=Marks
        )

    async def get_homeworks_short(
            self,
            profile_id: int,
            student_id: int,
            from_date: date,
            to_date: date,
            sort_column: str = "date",
            sort_direction: str = "asc",
    ) -> ShortHomeworks:
        """
        Retrieves a list of short homeworks for a given student within a specified date range.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.
            from_date (date): The start date of the date range.
            to_date (date): The end date of the date range.
            sort_column (str, optional): The column to sort the homeworks by. Defaults to "date".
            sort_direction (str, optional): The direction to sort the homeworks in. Defaults to "asc".

        Returns:
            ShortHomeworks: A list of short homeworks.

        Raises:
            None.
        """
        return await self.get(
            url=MesURLs.MOBILE.HOMEWORKS_SHORT,
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

    async def get_subject_marks_short(self, profile_id: int, student_id: int) -> ShortSubjectMarks:
        """
        Retrieve the short subject marks for a specific student.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.

        Returns:
            ShortSubjectMarks: The short subject marks for the student.
        """
        return await self.get(
            url=MesURLs.MOBILE.SHORT_SUBJECT_MARKS,
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

    async def get_subjects(self, profile_id: int, student_id: int) -> Subjects:
        """
        Retrieves the list of subjects for a specific student and profile.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.

        Returns:
            Subjects: An instance of the Subjects class containing the list of subjects.

        Raises:
            None.
        """
        return await self.get(
            url=MesURLs.MOBILE.SUBJECTS_LIST,
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

    async def get_visits(self, profile_id: int, student_id: int, contract_id: str, from_date: date, to_date: date) -> Visits:
        """
        Retrieves the visits for a specific student within a given date range.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.
            contract_id (str): The ID of the contract.
            from_date (date): The starting date of the range.
            to_date (date): The ending date of the range.

        Returns:
            Visits: The visits for the specified student within the given date range.
        """
        return await self.get(
            url=MesURLs.MOBILE.VISITS,
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

    async def get_notifications(self, profile_id: int, student_id: int) -> list[Notification]:
        """
        Retrieve a list of notifications for a specific student.

        Args:
            profile_id (int): The ID of the profile.
            student_id (int): The ID of the student.

        Returns:
            List[Notification]: A list of Notification objects representing the notifications.
        """
        return await self.get(
            url=MesURLs.MOBILE.NOTIFICATIONS,
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

    async def get_meals_clients(self, profile_id: int, contract_id: str):
        """
        Retrieves the meals clients for a specific student and contract.

        Args:
            profile_id (int): The ID of the profile.
            contract_id (str): The ID of the contract.

        Returns:
            MealsClients: The meals clients for the specified student and contract.
        """
        return await self.get(
            url=MesURLs.MOBILE.MEALS_CLIENTS,
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

    async def get_day_balance_info(self, profile_id: int, contract_id: str, first: int = 14, after: date | None = None) -> DayBalanceInfo:
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
        return await self.get(
            url=MesURLs.MOBILE.DAY_BALANCE_INFO,
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

    async def get_school_info(self, profile_id: int, school_id: int, class_unit_id: int) -> SchoolInfo:
        """
        Retrieves the information of a school for a specific student.

        Args:
            profile_id (int): The ID of the profile.
            school_id (int): The ID of the school.
            class_unit_id (int): The ID of the class unit.

        Returns:
            SchoolInfo: An object containing the information of the school.
        """
        return await self.get(
            url=MesURLs.MOBILE.SCHOOL_INFO,
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

    async def get_person_data(self, person_id: str, profile_id: int) -> PersonData:
        """
        Fetches the person data for a given person ID and profile ID.

        Args:
            person_id (str): The ID of the person.
            profile_id (int): The ID of the profile.

        Returns:
            PersonData: The person data.
        """
        return await self.get(
            url=MesURLs.MOBILE.PERSON_DATA.format(PERSON_ID=person_id),
            custom_headers={
                "x-mes-subsystem": "familymp",
                "client-type": "diary-mobile",
                "profile-id": profile_id
            },
            model=PersonData
        )

    async def refresh_token(self) -> str:
        """
        Refreshes the token and returns the refreshed token as a string.

        Returns:
            str: The refreshed token.

        """
        return await self.get(
            url=MesURLs.REFRESH,
            return_raw_text=True
        )

    async def get_schedule_item(
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
        return await self.get(
            url=MesURLs.MOBILE.LESSON_SCHEDULE_ITEMS.format(LESSON_ID=lesson_id),
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
