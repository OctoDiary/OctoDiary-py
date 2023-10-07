#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary


class URLs:
    """URLs for methods"""

    API_SESSIONS = "https://authedu.mosreg.ru/lms/api/sessions"
    PROFILE_INFO = "https://myschool.mosreg.ru/acl/api/users/profile_info"
    USER_SETTINGS = "https://authedu.mosreg.ru/api/usersettings/v1"
    EVENTS = "https://authedu.mosreg.ru/api/eventcalendar/v1/api/events"
    CHILDRENS = "https://authedu.mosreg.ru/v1/user/childrens"
    RATING_RANK_CLASS = "https://authedu.mosreg.ru/api/ej/rating/v1/rank/class"
    RATING_RANK_SHORT = "https://authedu.mosreg.ru/api/ej/rating/v1/rank/rankShort"
    RATING_RANK_SUBJECTS = "https://authedu.mosreg.ru/api/ej/rating/v1/rank/subjects"
    USER_INFO = "https://authedu.mosreg.ru/v3/userinfo"
    REFRESH_TOKEN = "https://authedu.mosreg.ru/v2/token/refresh"
    SYSTEM_MESSAGES = "https://myschool.mosreg.ru/acl/api/system_messages"
    API_SESSIONS2 = "https://myschool.mosreg.ru/lms/api/sessions"
    ACADEMIC_YEARS = "https://myschool.mosreg.ru/core/api/academic_years"
    USER = "https://myschool.mosreg.ru/acl/api/users"
    STUDENT_PROFILES = "https://myschool.mosreg.ru/core/api/student_profiles"
    PERSON_DATA = "https://authedu.mosreg.ru/api/persondata/v1/persons/{person_id}"
    USER_CONTACTS = "https://authedu.mosreg.ru/v1/user/contacts"
    ROLES = "https://authedu.mosreg.ru/v1/roles/allGlobal/"
    ORGANIZATIONS = "https://authedu.mosreg.ru/v1/nsi/organisations"


    class LOGIN:
        """URLs for login"""

        AUTH_CALLBACK = "https://authedu.mosreg.ru/v3/auth/kauth/callback"
        FILL_MFA = "https://esia.gosuslugi.ru/aas/oauth2/api/login/promo-mfa/fill-mfa?decision=false"
        ALLOW_SCOPE = "https://esia.gosuslugi.ru/aas/oauth2/api/scope/allow"
        AUTHEDU_ESIA_LOGIN = "https://authedu.mosreg.ru/v3/auth/esia/login"
        GOSUSLUGI_OAUTH2_CONFIG = "https://esia.gosuslugi.ru/aas/oauth2/config"
        GOSUSLUGI_API_LOGIN = "https://esia.gosuslugi.ru/aas/oauth2/api/login"
        ENTER_MFA = "https://esia.gosuslugi.ru/aas/oauth2/api/login/{METHOD}/verify?code={CODE}"


    class MOBILE:
        """Mobile API urls"""

        FAMILY_PROFILE = "https://api.myschool.mosreg.ru/family/mobile/v1/profile"
        HOMEWORKS_SHORT = "https://api.myschool.mosreg.ru/family/mobile/v1/homeworks/short"
        MARKS = "https://api.myschool.mosreg.ru/family/mobile/v1/marks"
        PERIODS_SCHEDULES = "https://api.myschool.mosreg.ru/family/mobile/v1/periods_schedules"
        SUBJECT_MARKS_SHORT = "https://api.myschool.mosreg.ru/family/mobile/v1/subject_marks/short"
        SUBJECTS_LIST = "https://api.myschool.mosreg.ru/family/mobile/v1/subjects/list"
        PROGRAMS_PARALLEL_CURRICULUM = "https://api.myschool.mosreg.ru/family/mobile/v1/programs/parallel_curriculum/162269"
        PERSON_DATA = "https://myschool.mosreg.ru/api/persondata/mobile/persons/{person_id}"
        NOTIFICATIONS = "https://api.myschool.mosreg.ru/family/mobile/v1/notifications/search"
        SUBJECT_MARKS = "https://api.myschool.mosreg.ru/family/mobile/v1/subject_marks/for_subject"
        LESSON_SCHEDULE_ITEMS = "https://api.myschool.mosreg.ru/family/mobile/v1/lesson_schedule_items/{lesson_id}"


    class WEB:
        """Web API urls"""

        FAMILY_PROFILE = "https://authedu.mosreg.ru/api/family/web/v1/profile"
