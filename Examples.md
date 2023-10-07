<p align="center">
    <a href="https://github.com/OctoDiary">
        <img src="https://avatars.githubusercontent.com/u/90847608?s=200&v=4" alt="OctoDiary" width="200">
    </a>
    <br>
    <a href="https://github.com/OctoDiary"><b>OctoDiary</b></a>
    •
    <a href="https://t.me/OctoDiary"><b>Telegram-Канал</b></a>
    •
    <a href="https://pypi.org/project/octodiary/"><b>PyPI</b></a>
</p>

---

## <p align="center"><img width="96" height="96" src="https://media.cdnandroid.com/item_images/1390670/imagen-moya-shkola-dnevnik-0ori.jpg" alt="myschool"/></p>


<details>
    <summary><img width="40" height="40" src="https://img.icons8.com/fluency/64/python.png" alt="python"/> <h1>Async</h1></summary>

``` python
import os
from asyncio import run

from octodiary.asyncApi.myschool import AsyncMobileAPI, AsyncWebAPI
from octodiary.types.captcha import Captcha


async def handle_captcha(captcha: Captcha, api: AsyncWebAPI | AsyncMobileAPI):
    if captcha.question:
        answer = input(captcha.question + ": ")
        response = await captcha.async_asnwer_captcha(answer)
        if isinstance(response, bool): # Требуется MFA код
            code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
            return await api.esia_enter_MFA(code=code_mfa)
        else:
            return response
    else:
        with open("captcha.png", "wb") as image:
            image.write(captcha.image_bytes)
        
        answer = input("Решите капчу из файла captcha.png: ")
        response = await captcha.async_verify_captcha(answer)
        os.remove("captcha.png")
        if isinstance(response, bool): # Требуется MFA код
            code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
            return await api.esia_enter_MFA(code=code_mfa)
        else:
            return response


async def login_gosuslugi(
    api: AsyncWebAPI | AsyncMobileAPI,
    login: str,
    password: str
):
    response: bool | Captcha = await api.esia_login(login, password)
    if isinstance(response, bool): # Требуется MFA код
        code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
        response2 = await api.esia_enter_MFA(code=code_mfa)
        TOKEN = response2 if isinstance(response2, str) else await handle_captcha(response2)
    elif isinstance(response, Captcha): # Капча
        TOKEN = await handle_captcha(response)
    
    api.token = TOKEN # сохраняем токен
    return TOKEN


async def web_api():
    """
    API методы и запросы, которые делают web-сайты myschool.mosreg.ru и authedu.mosreg.ru
    """

    api = AsyncWebAPI()

    # получение и сохранение токена по логину и паролю от госуслуг
    await login_gosuslugi(api, "login", "password")

    # получение и сохранение токена по логину и паролю от "Моей Школы"
    api.token = await api.login("login", "password")
    
    # получить информацию о пользователе
    user_info = await api.get_user_info()

    # обновить токен
    api.token = await api.refresh_token()

    # получить системные сообщения за текущий день
    system_messages = await api.get_system_messages()

    # получить информацию о сессии и пользователе
    session_info = await api.get_session_info()

    # получить учебные года (2022-2023 / 2023-2024)
    academic_years = await api.get_academic_years()
    
    # получить информацию о каком-либо пользователе
    # (оставьте пустым для получения информации об владельце токена)
    owner_user = await api.get_user()
    other_user = await api.get_user("<USER-ID>")

    # получить информацию об одном или нескольких профилях студента (ученика)
    # (оставьте пустым для получения информации о текущем учебном году)
    student_profiles_current_academic_year = await api.get_student_profiles()
    ID = 0 # валидный ID
    student_profiles = await api.get_student_profiles(academic_year_id=ID)

    # получить информацию о web-профиле
    # содержит подробную информацию, включая личные данные
    web_profile = await api.get_family_web_profile()

    # получить фулл о пользователе (дада, методов много, но каждый дает свое)
    person_data = await api.get_person_data("PERSON-ID")

    # получить список событий пользователя по параметрам
    from datetime import date

    events = await api.get_events(
        person_id="<PERSON-ID>", # person-id ученика
        mes_role="<role>", # роль пользователя (если родитель - parent)
        begin_date=date(2023, 9, 4), # дата начала
        end_date=date(2023, 9, 10), # дата конца (если не указана - текущий день)
    )

    # получить информацию о всех детях пользователя по параметрам
    # если API TOKEN аккаунта ученика, работать не будет
    childrens = await api.get_childrens(
        sso_id="<SSO-ID>", # sso-id
    )

    # получить информацию о контактах пользователя (email, phone, ...)
    contacts = await api.get_user_contacts()

    # получить информацию об организации
    ID = 0 # валидный ID организации, именно organization_id
    organization = await api.get_organizations(ID)


async def mobile_api():
    """
    API методы и запросы, которые делает приложение "Дневник Моя Школа" для получения данных
    """

    api = AsyncMobileAPI()

    # получение и сохранение токена по логину и паролю от госуслуг
    await login_gosuslugi(api)

    # получить информацию о владельце аккаунта, чей токен мы имеем
    user_profile_info = await api.get_users_profile_info()

    # получить инфо о профиле
    profile = await api.get_profile(profile_id=user_profile_info[0].id)

    # получить сохраненные настройки приложения пользователя (тема и т.д.)
    settings = await api.get_user_settings_app(profile_id=user_profile_info[0].id)

    # редактировать настройки приложения у пользователя
    settings.theme.is_automatic = True
    await api.edit_user_settings_app(profile_id=user_profile_info[0].id, settings=settings)

    # получить расписание событий за определенный промежуток времени
    from datetime import date

    events = await api.get_events(
        person_id=user_profile_info[0].id,
        mes_role="<role>",
        begin_date=date(2023, 9, 4), # начало промежутка времени
        end_date=date(2023, 9, 10) # конец
    )

    # получить краткую информацию о домашних заданиях за определенный промежуток времени
    homeworks_short = await api.get_homeworks_short(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
        from_date=date(2023, 9, 4), # начало промежутка времени
        to_date=date(2023, 9, 10), # конец
    )

    # получить информацию об оценках за определенный промежуток времени
    marks = await api.get_marks(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
        from_date=date(2023, 9, 4), # начало промежутка времени
        to_date=date(2023, 9, 10), # конец
    )

    # Получить информацию о всех днях за определенный промежуток времени:
    #  - какой учебный модуль идет на момент опеределенного дня
    #  - что это: каникулы, выходной, рабочий день
    periods_schedules = await api.get_periods_schedules(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
        from_date=date(2023, 9, 4), # начало промежутка времени
        to_date=date(2023, 9, 10), # конец
    )

    # Получить оценки и ср.баллы по предметам за период времени
    marks_short = await api.get_subject_marks_short(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
    )

    # Получить список предметов
    subjects = await api.get_subjects(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id
    )

    # получить программу обучения на текущий учебный год
    parallel_curriculum = await api.get_programs_parallel_curriculum(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id
    )

    # Получить подробную информацию о профиле
    person_data = await api.get_person_data(
        person_id="<PERSON-ID>",
        profile_id=user_profile_info[0].id
    )

    # получить инфо о детях пользователя, если он является родителем
    childrens = await api.get_user_childrens(
        person_id="<PERSON-ID>",
    )

    # получить уведомления пользователя
    notifications = await api.get_notifications(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id
    )

    # Получить инфо о предмете: оценки и т.д.
    subject_marks_info = await api.get_subject_marks_for_subject(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
        subject_name="<ИМЯ-УРОКА>" # Например: "Русский язык"
    )


async def main():
    await web_api()
    await mobile_api()

run(main())
```

</details>

<details>
    <summary><img width="40" height="40" src="https://img.icons8.com/fluency/64/python.png" alt="python"/> <h1>Sync</h1></summary>

``` python
import os

from octodiary.syncApi.myschool import SyncMobileAPI, SyncWebAPI
from octodiary.types.captcha import Captcha


def handle_captcha(captcha: Captcha, api: SyncWebAPI | SyncMobileAPI):
    if captcha.question:
        answer = input(captcha.question + ": ")
        response = captcha.asnwer_captcha(answer)
        if isinstance(response, bool): # Требуется MFA код
            code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
            return api.esia_enter_MFA(code=code_mfa)
        else:
            return response
    else:
        with open("captcha.png", "wb") as image:
            image.write(captcha.image_bytes)
        
        answer = input("Решите капчу из файла captcha.png: ")
        response = captcha.verify_captcha(answer)
        os.remove("captcha.png")
        if isinstance(response, bool): # Требуется MFA код
            code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
            return api.esia_enter_MFA(code=code_mfa)
        else:
            return response


def login_gosuslugi(
    api: SyncWebAPI | SyncMobileAPI,
    login: str,
    password: str
):
    # если у вас включен вход с подтверждением (MFA):
    response: bool | Captcha | str = api.esia_login(login, password)
    if isinstance(response, bool): # Требуется MFA код
        code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
        response2 = api.esia_enter_MFA(code=code_mfa)
        TOKEN = response2 if isinstance(response2, str) else handle_captcha(response2)
    elif isinstance(response, Captcha): # Капча
        TOKEN = handle_captcha(response)
    else:
        TOKEN = response
    
    api.token = TOKEN # сохраняем токен
    return TOKEN


def web_api():
    """
    API методы и запросы, которые делают web-сайты myschool.mosreg.ru и authedu.mosreg.ru
    """

    api = SyncWebAPI()

    # получение и сохранение токена по логину и паролю от госуслуг
    login_gosuslugi(api, "login", "password")

    # получение и сохранение токена по логину и паролю от "Моей Школы"
    api.token = api.login("login", "password")
    
    # получить информацию о пользователе
    user_info = api.get_user_info()

    # обновить токен
    api.token = api.refresh_token()

    # получить системные сообщения за текущий день
    system_messages = api.get_system_messages()

    # получить информацию о сессии и пользователе
    session_info = api.get_session_info()

    # получить учебные года (2022-2023 / 2023-2024)
    academic_years = api.get_academic_years()
    
    # получить информацию о каком-либо пользователе
    # (оставьте пустым для получения информации об владельце токена)
    owner_user = api.get_user()
    other_user = api.get_user("<USER-ID>")

    # получить информацию об одном или нескольких профилях студента (ученика)
    # (оставьте пустым для получения информации о текущем учебном году)
    student_profiles_current_academic_year = api.get_student_profiles()
    ID = 0 # валидный ID
    student_profiles = api.get_student_profiles(academic_year_id=ID)

    # получить информацию о web-профиле
    # содержит подробную информацию, включая личные данные
    web_profile = api.get_family_web_profile()

    # получить фулл о пользователе (дада, методов много, но каждый дает свое)
    person_data = api.get_person_data("PERSON-ID")

    # получить список событий пользователя по параметрам
    from datetime import date

    events = api.get_events(
        person_id="<PERSON-ID>", # person-id ученика
        mes_role="<role>", # роль пользователя (если родитель - parent)
        begin_date=date(2023, 9, 4), # дата начала
        end_date=date(2023, 9, 10), # дата конца (если не указана - текущий день)
    )

    # получить информацию о всех детях пользователя по параметрам
    # если API TOKEN аккаунта ученика, работать не будет
    childrens = api.get_childrens(
        sso_id="<SSO-ID>", # sso-id
    )

    # получить информацию о контактах пользователя (email, phone, ...)
    contacts = api.get_user_contacts()

    # получить информацию об организации
    ID = 0 # валидный ID организации, именно organization_id
    organization = api.get_organizations(ID)


def mobile_api():
    """
    API методы и запросы, которые делает приложение "Дневник Моя Школа" для получения данных
    """

    api = SyncMobileAPI()

    # получение и сохранение токена по логину и паролю от госуслуг
    login_gosuslugi(api)

    # получить информацию о владельце аккаунта, чей токен мы имеем
    user_profile_info = api.get_users_profile_info()

    # получить инфо о профиле
    profile = api.get_profile(profile_id=user_profile_info[0].id)

    # получить сохраненные настройки приложения пользователя (тема и т.д.)
    settings = api.get_user_settings_app(profile_id=user_profile_info[0].id)

    # редактировать настройки приложения у пользователя
    settings.theme.is_automatic = True
    api.edit_user_settings_app(profile_id=user_profile_info[0].id, settings=settings)

    # получить расписание событий за определенный промежуток времени
    from datetime import date

    events = api.get_events(
        person_id=user_profile_info[0].id,
        mes_role="<role>",
        begin_date=date(2023, 9, 4), # начало промежутка времени
        end_date=date(2023, 9, 10) # конец
    )

    # получить краткую информацию о домашних заданиях за определенный промежуток времени
    homeworks_short = api.get_homeworks_short(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
        from_date=date(2023, 9, 4), # начало промежутка времени
        to_date=date(2023, 9, 10), # конец
    )

    # получить информацию об оценках за определенный промежуток времени
    marks = api.get_marks(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
        from_date=date(2023, 9, 4), # начало промежутка времени
        to_date=date(2023, 9, 10), # конец
    )

    # Получить информацию о всех днях за определенный промежуток времени:
    #  - какой учебный модуль идет на момент опеределенного дня
    #  - что это: каникулы, выходной, рабочий день
    periods_schedules = api.get_periods_schedules(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
        from_date=date(2023, 9, 4), # начало промежутка времени
        to_date=date(2023, 9, 10), # конец
    )

    # Получить оценки и ср.баллы по предметам за период времени
    marks_short = api.get_subject_marks_short(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
    )

    # Получить список предметов
    subjects = api.get_subjects(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id
    )

    # получить программу обучения на текущий учебный год
    parallel_curriculum = api.get_programs_parallel_curriculum(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id
    )

    # Получить подробную информацию о профиле
    person_data = api.get_person_data(
        person_id="<PERSON-ID>",
        profile_id=user_profile_info[0].id
    )

    # получить инфо о детях пользователя, если он является родителем
    childrens = api.get_user_childrens(
        person_id="<PERSON-ID>",
    )

    # получить уведомления пользователя
    notifications = api.get_notifications(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id
    )

    # Получить инфо о предмете: оценки и т.д.
    subject_marks_info = api.get_subject_marks_for_subject(
        student_id=0, # <STUDENT-ID>
        profile_id=user_profile_info[0].id,
        subject_name="<ИМЯ-УРОКА>" # Например: "Русский язык"
    )


def main():
    web_api()
    mobile_api()

if __name__ == "__main__":
    main()
```

</details>

---

## <p align="center"><img width="96" height="96" src="https://is3-ssl.mzstatic.com/image/thumb/Purple114/v4/57/39/7b/57397bea-0eb8-d0d3-ad57-c170359343af/source/200x200bb.jpg" alt="mesh"/></p>
> Скоро...
