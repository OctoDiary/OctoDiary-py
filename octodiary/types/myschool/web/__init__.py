#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from octodiary.types.myschool.web.academicyear import AcademicYear
from octodiary.types.myschool.web.events import EventsResponse
from octodiary.types.myschool.web.persondata import PersonData
from octodiary.types.myschool.web.role import Role
from octodiary.types.myschool.web.sessionuserinfo import SessionUserInfo
from octodiary.types.myschool.web.studentprofile import StudentProfile
from octodiary.types.myschool.web.user import User
from octodiary.types.myschool.web.userchildren import UserChildren
from octodiary.types.myschool.web.usercontact import UserContact
from octodiary.types.myschool.web.userinfo import UserInfo
from octodiary.types.myschool.web.webfamilyprofile import WebFamilyProfile
from octodiary.types.myschool.web.weborganizations import WebOrganizations

__all__ = [
    "UserInfo",
    "SessionUserInfo",
    "AcademicYear",
    "User",
    "StudentProfile",
    "WebFamilyProfile",
    "PersonData",
    "Role",
    "EventsResponse",
    "UserChildren",
    "UserContact",
    "WebOrganizations",
]
