#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary


class MySchoolURLs:
    """URLs for methods in system "Моя Школа" """

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
        """URLs for login process"""

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
        PROGRAMS_PARALLEL_CURRICULUM = "https://api.myschool.mosreg.ru/family/mobile/v1/programs/parallel_curriculum/{ID}"
        PERSON_DATA = "https://myschool.mosreg.ru/api/persondata/mobile/persons/{person_id}"
        NOTIFICATIONS = "https://api.myschool.mosreg.ru/family/mobile/v1/notifications/search"
        SUBJECT_MARKS = "https://api.myschool.mosreg.ru/family/mobile/v1/subject_marks/for_subject"
        LESSON_SCHEDULE_ITEMS = "https://api.myschool.mosreg.ru/family/mobile/v1/lesson_schedule_items/{lesson_id}"


    class WEB:
        """Web API urls"""

        FAMILY_PROFILE = "https://authedu.mosreg.ru/api/family/web/v1/profile"

class MesURLs:
    """URLs for methods in system "МЭШ" """

    PROFILE_INFO = "https://dnevnik.mos.ru/acl/api/users/profile_info"
    EVENTS = "https://school.mos.ru/api/eventcalendar/v1/api/events"
    REFRESH = "https://school.mos.ru/v2/token/refresh"

    class LOGIN:
        """URLs for login process"""

        AURHORIZATION_ENDPOINT = "https://login.mos.ru/sps/oauth/ae"
        AUTH_WITH_LOGIN_AND_PASSWORD = "https://login.mos.ru/sps/login/methods/headless/password"
        BIND_SMS_CODE = "https://login.mos.ru/sps/login/methods/headless/sms/bind"
        TRUST = "https://login.mos.ru/sps/login/ur/askToTrust"


    class MOBILE:
        """Mobile API urls"""

        FAMILY_PROFILE = "https://school.mos.ru/api/family/mobile/v1/profile"
        PROFILE = "https://school.mos.ru/api/family/mobile/v1/profile"
        STATUS = "https://school.mos.ru/api/family/mobile/v1/status"
        PERIODS_SCHEDULES = "https://school.mos.ru/api/family/mobile/v1/periods_schedules"
        SUBJECTS_LIST = "https://school.mos.ru/api/family/mobile/v1/subjects/list"
        MARKS = "https://school.mos.ru/api/family/mobile/v1/marks"
        HOMEWORKS_SHORT = "https://school.mos.ru/api/family/mobile/v1/homeworks/short"
        SHORT_SUBJECT_MARKS = "https://school.mos.ru/api/family/mobile/v1/subject_marks/short"
        VISITS = "https://school.mos.ru/api/family/mobile/v1/visits"
        NOTIFICATIONS = "https://school.mos.ru/api/family/mobile/v1/notifications/search"
        MEALS_CLIENTS = "https://dnevnik.mos.ru/api/meals/v1/clients"
        DAY_BALANCE_INFO = "https://school.mos.ru/api/family/mobile/v1/day_balance_info"
        SCHOOL_INFO = "https://school.mos.ru/api/family/mobile/v1/school_info"
        PERSON_DATA = "https://school.mos.ru/api/persondata/mobile/persons/{PERSON_ID}"
        LESSON_SCHEDULE_ITEMS = "https://school.mos.ru/api/family/mobile/v1/lesson_schedule_items/{LESSON_ID}"
