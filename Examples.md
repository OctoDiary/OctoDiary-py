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

```python
import os
from asyncio import run
from contextlib import suppress

from octodiary.urls import Systems
from octodiary.apis import AsyncMobileAPI, AsyncWebAPI
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

        answer = input("Введите решение капчи (captcha.png): ")
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
        token = response2 if isinstance(response2, str) else await handle_captcha(response2)
    elif isinstance(response, Captcha): # Капча
        token = await handle_captcha(response)

    return token


async def web_api():
    """
    API методы и запросы, которые делают web-сайты myschool.mosreg.ru и authedu.mosreg.ru
    """

    api = AsyncWebAPI(system=Systems.MYSCHOOL)


    # запрос у пользователя логина и пароля для получения API-Токена
    auth_type = input("Тип авторизации (0 - Логин и пароль, 1 - Госуслуги): ")
    if auth_type == "1": # Авторизация через Госуслуги
        login = input("[Госуслуги] Логин: ")
        password = input("[Госуслуги] Пароль: ")

        api.token = await login_gosuslugi(api, login, password) # получение и сохранение API-Токена
    else:
        login = input("Логин: ")
        password = input("Пароль: ")

        api.token = await api.login(login, password) # получение и сохранение API-Токена

    # получить информацию о пользователе
    user_info = await api.get_user_info()

    # обновить токен
    api.token = await api.refresh_token()

    # получить системные сообщения за текущий день
    system_messages = await api.get_system_messages()

    # получить информацию о сессии и пользователе
    session_info = await api.get_session_info()

    # получить список учебных годов (2022-2023 / 2023-2024)
    academic_years = await api.get_academic_years()


    # получить информацию об одном или нескольких профилях студента (ученика)
    # (оставьте пустым для получения информации о текущем учебном году)
    student_profiles_current_academic_year = await api.get_student_profiles()
    ID = 0 # валидный ID учебного года
    student_profiles = await api.get_student_profiles(academic_year_id=ID) # ID нужно брать из списка учебных годов (см. выше)

    # получить информацию о каком-либо пользователе
    # (оставьте пустым для получения информации о себе)
    owner_user = await api.get_user()
    other_user = await api.get_user("<USER-ID>")


    # получить информацию о web-профиле
    # содержит подробную информацию, включая личные данные
    web_profile = await api.get_family_web_profile()

    # получить полную подробную информацию о пользователе
    person_data = await api.get_person_data("PERSON-ID")

    # получить список событий пользователя
    from datetime import date, timedelta

    events = await api.get_events(
        person_id=web_profile.children[0].contingent_guid, # person-id ученика (contingent_guid)
        mes_role=web_profile.profile.type, # роль пользователя (student, parent)
        begin_date=date.today(), # дата начала (если не указана - текущий день)
        end_date=date.today() + timedelta(days=7), # дата конца (если не указана - текущий день)
    )

    # получить информацию о всех детях пользователя
    # требуется аккаунт родителя
    with suppress(ModuleNotFoundError, ImportError):
        import jwt  # библиотека для декодирования API-токена (pip install pyjwt)

        sso_id = jwt.decode(api.token, verify=False).get("sso")
        childrens = await api.get_children(
            sso_id=sso_id
        )

    # получить информацию об организации
    ID = person_data.education[0].organization_id # валидный ID организации, именно organization_id
    organization = await api.get_organizations(ID)


async def mobile_api():
    """
    API методы и запросы, которые делает приложение "Дневник Моя Школа" для получения необходимых данных
    """

    api = AsyncMobileAPI(system=Systems.MYSCHOOL)


    # запрос у пользователя логина и пароля для получения API-Токена
    auth_type = input("Тип авторизации (0 - Логин и пароль, 1 - Госуслуги): ")
    if auth_type == "1": # Авторизация через Госуслуги
        login = input("[Госуслуги] Логин: ")
        password = input("[Госуслуги] Пароль: ")

        api.token = await login_gosuslugi(api, login, password) # получение и сохранение API-Токена
    else:
        login = input("Логин: ")
        password = input("Пароль: ")

        api.token = await api.login(login, password) # получение и сохранение API-Токена

    # получить информацию о владельце аккаунта, чей токен мы имеем
    user_profile_info = await api.get_users_profile_info()

    # получить инфо о профиле
    profile = await api.get_family_profile(profile_id=user_profile_info[0].id)

    # получить сохраненные настройки приложения пользователя (тема и т.д.)
    settings = await api.get_user_settings_app(profile_id=user_profile_info[0].id)

    # редактировать настройки приложения у пользователя
    settings.theme.is_automatic = not settings.theme.is_automatic
    await api.edit_user_settings_app(profile_id=user_profile_info[0].id, settings=settings)

    # получить расписание событий
    from datetime import date, timedelta

    events = await api.get_events( # получить расписание событий на 7 дней вперед
        person_id=profile.children[0].contingent_guid, # person-id ученика (contingent_guid)
        mes_role=profile.profile.type, # роль пользователя (student, parent)
        begin_date=date.today(), # начало промежутка времени
        end_date=date.today() + timedelta(days=7), # конец
    )

    # получить краткую информацию о домашних заданиях на 7 дней вперед
    homeworks_short = await api.get_homeworks_short(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id, # <PROFILE-ID>
        from_date=date.today(), # начало промежутка времени
        to_date=date.today() + timedelta(days=7), # конец
    )

    # получить информацию об оценках за последние 7 дней
    marks = await api.get_marks(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id, # <PROFILE-ID>
        from_date=date.today() - timedelta(days=7), # начало промежутка времени
        to_date=date.today(), # конец
    )

    # Получить информацию о днях в периоде времени:
    #  - какой учебный модуль идет на момент опеределенного дня
    #  - что это за день: каникулы, выходной, учебный день
    periods_schedules = await api.get_periods_schedules( # информация по дням на 30 дней вперед
        student_id=profile.children[0].id,              # <STUDENT-ID>
        profile_id=user_profile_info[0].id,             # <PROFILE-ID>
        from_date=date.today(),                         # начало промежутка времени
        to_date=date.today() + timedelta(days=30),      # конец
    )

    # Получить оценки и средние баллы по предметам за период времени
    marks_short = await api.get_subject_marks_short(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id # <PROFILE-ID>
    )

    # Получить список предметов
    subjects = await api.get_subjects(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id # <PROFILE-ID>
    )

    # получить программу обучения на текущий учебный год
    parallel_curriculum = await api.get_programs_parallel_curriculum(
        id=profile.children[0].parallel_curriculum_id, # <PARALLEL-CURRICULUM-ID>
        student_id=profile.children[0].id,             # <STUDENT-ID>
        profile_id=user_profile_info[0].id             # <PROFILE-ID>
    )

    # Получить подробную информацию о профиле
    person_data = await api.get_person_data(
        person_id=profile.children[0].contingent_guid, # person-id ученика (contingent_guid)
        profile_id=user_profile_info[0].id             # <PROFILE-ID>
    )

    # получить уведомления ученика
    notifications = await api.get_notifications(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id # <PROFILE-ID>
    )

    # Получить инфо о предмете: оценки и т.д.
    subject_marks_info = await api.get_subject_marks_for_subject(
        student_id=profile.children[0].id,   # <STUDENT-ID>
        profile_id=user_profile_info[0].id,  # <PROFILE-ID>
        subject_name="<ИМЯ-ПРЕДМЕТА>"        # Например: "Алгебра"
    )


async def main():
    type = input("Enter type of api (1 - web, 2 - mobile): ")

    if type == "1":
        await web_api()
    else:
        await mobile_api()

if __name__ == "__main__":
    run(main())
```

</details>

<details>
    <summary><img width="40" height="40" src="https://img.icons8.com/fluency/64/python.png" alt="python"/> <h1>Sync</h1></summary>

``` python
import os
from contextlib import suppress

from octodiary.apis import AsyncMobileAPI, AsyncWebAPI
from octodiary.urls import Systems
from octodiary.types.captcha import Captcha


def handle_captcha(captcha: Captcha, api: AsyncWebAPI | AsyncMobileAPI):
    if captcha.question:
        answer = input(captcha.question + ": ")
        response = captcha.async_asnwer_captcha(answer)
        if isinstance(response, bool): # Требуется MFA код
            code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
            return api.esia_enter_MFA(code=code_mfa)
        else:
            return response
    else:
        with open("captcha.png", "wb") as image:
            image.write(captcha.image_bytes)

        answer = input("Введите решение капчи (captcha.png): ")
        response = captcha.async_verify_captcha(answer)
        os.remove("captcha.png")
        if isinstance(response, bool): # Требуется MFA код
            code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
            return api.esia_enter_MFA(code=code_mfa)
        else:
            return response


def login_gosuslugi(
    api: AsyncWebAPI | AsyncMobileAPI,
    login: str,
    password: str
):
    response: bool | Captcha = api.esia_login(login, password)
    if isinstance(response, bool): # Требуется MFA код
        code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
        response2 = api.esia_enter_MFA(code=code_mfa)
        token = response2 if isinstance(response2, str) else handle_captcha(response2)
    elif isinstance(response, Captcha): # Капча
        token = handle_captcha(response)

    return token


def web_api():
    """
    API методы и запросы, которые делают web-сайты myschool.mosreg.ru и authedu.mosreg.ru
    """

    api = AsyncWebAPI(system=Systems.MYSCHOOL)


    # запрос у пользователя логина и пароля для получения API-Токена
    auth_type = input("Тип авторизации (0 - Логин и пароль, 1 - Госуслуги): ")
    if auth_type == "1": # Авторизация через Госуслуги
        login = input("[Госуслуги] Логин: ")
        password = input("[Госуслуги] Пароль: ")

        api.token = login_gosuslugi(api, login, password) # получение и сохранение API-Токена
    else:
        login = input("Логин: ")
        password = input("Пароль: ")

        api.token = api.login(login, password) # получение и сохранение API-Токена

    # получить информацию о пользователе
    user_info = api.get_user_info()

    # обновить токен
    api.token = api.refresh_token()

    # получить системные сообщения за текущий день
    system_messages = api.get_system_messages()

    # получить информацию о сессии и пользователе
    session_info = api.get_session_info()

    # получить список учебных годов (2022-2023 / 2023-2024)
    academic_years = api.get_academic_years()


    # получить информацию об одном или нескольких профилях студента (ученика)
    # (оставьте пустым для получения информации о текущем учебном году)
    student_profiles_current_academic_year = api.get_student_profiles()
    ID = 0 # валидный ID учебного года
    student_profiles = api.get_student_profiles(academic_year_id=ID) # ID нужно брать из списка учебных годов (см. выше)

    # получить информацию о каком-либо пользователе
    # (оставьте пустым для получения информации о себе)
    owner_user = api.get_user()
    other_user = api.get_user("<USER-ID>")


    # получить информацию о web-профиле
    # содержит подробную информацию, включая личные данные
    web_profile = api.get_family_web_profile()

    # получить полную подробную информацию о пользователе
    person_data = api.get_person_data("PERSON-ID")

    # получить список событий пользователя
    from datetime import date, timedelta

    events = api.get_events(
        person_id=web_profile.children[0].contingent_guid, # person-id ученика (contingent_guid)
        mes_role=web_profile.profile.type, # роль пользователя (student, parent)
        begin_date=date.today(), # дата начала (если не указана - текущий день)
        end_date=date.today() + timedelta(days=7), # дата конца (если не указана - текущий день)
    )

    # получить информацию о всех детях пользователя
    # требуется аккаунт родителя
    with suppress(ModuleNotFoundError, ImportError):
        import jwt  # библиотека для декодирования API-токена (pip install pyjwt)

        sso_id = jwt.decode(api.token, verify=False).get("sso")
        childrens = api.get_children(
            sso_id=sso_id
        )

    # получить информацию об организации
    ID = person_data.education[0].organization_id # валидный ID организации, именно organization_id
    organization = api.get_organizations(ID)


def mobile_api():
    """
    API методы и запросы, которые делает приложение "Дневник Моя Школа" для получения необходимых данных
    """

    api = AsyncMobileAPI(system=Systems.MYSCHOOL)


    # запрос у пользователя логина и пароля для получения API-Токена
    auth_type = input("Тип авторизации (0 - Логин и пароль, 1 - Госуслуги): ")
    if auth_type == "1": # Авторизация через Госуслуги
        login = input("[Госуслуги] Логин: ")
        password = input("[Госуслуги] Пароль: ")

        api.token = login_gosuslugi(api, login, password) # получение и сохранение API-Токена
    else:
        login = input("Логин: ")
        password = input("Пароль: ")

        api.token = api.login(login, password) # получение и сохранение API-Токена

    # получить информацию о владельце аккаунта, чей токен мы имеем
    user_profile_info = api.get_users_profile_info()

    # получить инфо о профиле
    profile = api.get_family_profile(profile_id=user_profile_info[0].id)

    # получить сохраненные настройки приложения пользователя (тема и т.д.)
    settings = api.get_user_settings_app(profile_id=user_profile_info[0].id)

    # редактировать настройки приложения у пользователя
    settings.theme.is_automatic = not settings.theme.is_automatic
    api.edit_user_settings_app(profile_id=user_profile_info[0].id, settings=settings)

    # получить расписание событий
    from datetime import date, timedelta

    events = api.get_events( # получить расписание событий на 7 дней вперед
        person_id=profile.children[0].contingent_guid, # person-id ученика (contingent_guid)
        mes_role=profile.profile.type, # роль пользователя (student, parent)
        begin_date=date.today(), # начало промежутка времени
        end_date=date.today() + timedelta(days=7), # конец
    )

    # получить краткую информацию о домашних заданиях на 7 дней вперед
    homeworks_short = api.get_homeworks_short(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id, # <PROFILE-ID>
        from_date=date.today(), # начало промежутка времени
        to_date=date.today() + timedelta(days=7), # конец
    )

    # получить информацию об оценках за последние 7 дней
    marks = api.get_marks(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id, # <PROFILE-ID>
        from_date=date.today() - timedelta(days=7), # начало промежутка времени
        to_date=date.today(), # конец
    )

    # Получить информацию о днях в периоде времени:
    #  - какой учебный модуль идет на момент опеределенного дня
    #  - что это за день: каникулы, выходной, учебный день
    periods_schedules = api.get_periods_schedules( # информация по дням на 30 дней вперед
        student_id=profile.children[0].id,              # <STUDENT-ID>
        profile_id=user_profile_info[0].id,             # <PROFILE-ID>
        from_date=date.today(),                         # начало промежутка времени
        to_date=date.today() + timedelta(days=30),      # конец
    )

    # Получить оценки и средние баллы по предметам за период времени
    marks_short = api.get_subject_marks_short(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id # <PROFILE-ID>
    )

    # Получить список предметов
    subjects = api.get_subjects(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id # <PROFILE-ID>
    )

    # получить программу обучения на текущий учебный год
    parallel_curriculum = api.get_programs_parallel_curriculum(
        id=profile.children[0].parallel_curriculum_id, # <PARALLEL-CURRICULUM-ID>
        student_id=profile.children[0].id,             # <STUDENT-ID>
        profile_id=user_profile_info[0].id             # <PROFILE-ID>
    )

    # Получить подробную информацию о профиле
    person_data = api.get_person_data(
        person_id=profile.children[0].contingent_guid, # person-id ученика (contingent_guid)
        profile_id=user_profile_info[0].id             # <PROFILE-ID>
    )

    # получить уведомления ученика
    notifications = api.get_notifications(
        student_id=profile.children[0].id, # <STUDENT-ID>
        profile_id=user_profile_info[0].id # <PROFILE-ID>
    )

    # Получить инфо о предмете: оценки и т.д.
    subject_marks_info = api.get_subject_marks_for_subject(
        student_id=profile.children[0].id,   # <STUDENT-ID>
        profile_id=user_profile_info[0].id,  # <PROFILE-ID>
        subject_name="<ИМЯ-ПРЕДМЕТА>"        # Например: "Алгебра"
    )


def main():
    type = input("Enter type of api (1 - web, 2 - mobile): ")

    if type == "1":
        web_api()
    else:
        mobile_api()

if __name__ == "__main__":
    main()
```

</details>

---

## <p align="center"><img width="96" height="96" src="https://is3-ssl.mzstatic.com/image/thumb/Purple114/v4/57/39/7b/57397bea-0eb8-d0d3-ad57-c170359343af/source/200x200bb.jpg" alt="mesh"/></p>
>


<details>
    <summary><img width="40" height="40" src="https://img.icons8.com/fluency/64/python.png" alt="python"/> <h1>Async</h1></summary>

``` python
from asyncio import run

from octodiary.apis import AsyncMobileAPI
from octodiary.types.enter_sms_code import EnterSmsCode
from octodiary.urls import Systems


async def mobile_api():
    """
    API методы и запросы, которые делает приложение "Дневник МЭШ" для получения данных
    """

    api = AsyncMobileAPI(system=Systems.MES)

    # авторизовываемся, получаем токен и сохраняем его
    login = input("Логин: ")
    password = input("Пароль: ")

    sms_code: EnterSmsCode = await api.login(username=login, password=password)
    code = input("SMS-Code: ")
    api.token = await sms_code.async_enter_code(code)

    # получаем ID профиля
    profile_id = (await api.get_users_profiles_info())[0].id

    # Получаем инфо о профиле и сохраняем некоторые важные данные, которые будут нужны
    profile = await api.get_family_profile(profile_id=profile_id)
    mes_role = profile.profile.type                      # тип пользователя
    person_id = profile.children[0].contingent_guid      # person-id ученика
    student_id = profile.children[0].id                  # <STUDENT-ID>
    contract_id = profile.children[0].contract_id        # <CONTRACT-ID>

    # получить сохраненные настройки приложения пользователя (тема и т.д.)
    settings = await api.get_user_settings_app(profile_id=profile_id)

    # редактировать настройки приложения у пользователя
    settings.theme.is_automatic = not settings.theme.is_automatic
    await api.edit_user_settings_app(profile_id=profile_id, settings=settings)

    # получить расписание событий
    from datetime import date, timedelta

    events = await api.get_events( # получить расписание событий на 7 дней вперед
        person_id=person_id,                            # person-id ученика (contingent_guid)
        mes_role=mes_role,                              # роль пользователя (student, parent)
        begin_date=date.today(),                        # начало промежутка времени
        end_date=date.today() + timedelta(days=7),      # конец
    )

    # получить краткую информацию о домашних заданиях на 7 дней вперед
    homeworks_short = await api.get_homeworks_short(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id,                          # <PROFILE-ID>
        from_date=date.today(),                         # начало промежутка времени
        to_date=date.today() + timedelta(days=7),       # конец
    )

    # получить информацию об оценках за последние 7 дней
    marks = await api.get_marks(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id,                          # <PROFILE-ID>
        from_date=date.today() - timedelta(days=7),     # начало промежутка времени
        to_date=date.today(),                           # конец
    )

    # Получить информацию о днях в периоде времени:
    #  - какой учебный модуль идет на момент опеределенного дня
    #  - что это за день: каникулы, выходной, учебный день
    periods_schedules = await api.get_periods_schedules( # информация по дням на 30 дней вперед
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id,                          # <PROFILE-ID>
        from_date=date.today(),                         # начало промежутка времени
        to_date=date.today() + timedelta(days=30),      # конец
    )

    # Получить список предметов
    subjects = await api.get_subjects(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id                           # <PROFILE-ID>
    )

    # получить программу обучения на текущий учебный год
    parallel_curriculum = await api.get_programs_parallel_curriculum(
        id=profile.children[0].parallel_curriculum_id,  # <PARALLEL-CURRICULUM-ID>
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id                           # <PROFILE-ID>
    )

    # Получить подробную информацию о профиле
    person_data = await api.get_person_data(
        person_id=person_id,                            # person-id ученика (contingent_guid)
        profile_id=profile_id                           # <PROFILE-ID>
    )

    # получить уведомления ученика
    notifications = await api.get_notifications(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id                           # <PROFILE-ID>
    )

    # Получить инфо о предмете: оценки и т.д.
    subject_marks_info = await api.get_subject_marks_for_subject(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id,                          # <PROFILE-ID>
        subject_name="<ИМЯ-ПРЕДМЕТА>"                   # Например: "Алгебра"
    )

    # Получим подробную информацию об уроке или занятии (в данном случае о первом занятии в списке)
    lesson_info = await api.get_lesson_schedule_item(
        profile_id=profile_id,                          # <PROFILE-ID>
        lesson_id=events.response[0].id,                # <LESSON-ID>
        student_id=student_id,                          # <STUDENT-ID>
        type=events.response[0].source                  # <TYPE>
    )


    # Получаем инфо о балансе
    balance_info = await api.get_status(
        profile_id=profile_id,                          # <PROFILE-ID>
        contract_id=contract_id                         # <CONTRACT-ID>
    )
    print("Баланс:", balance_info.students[0].balance / 100, "₽")

    # Информация об оценках и средних баллам по предметам
    subject_marks = await api.get_subject_marks_short(
        profile_id=profile_id,                          # <PROFILE-ID>
        student_id=student_id                           # <STUDENT-ID>
    )

    # Информация о посещениях (время входа, выхода, и т.д.) за последние 7 дней
    visits = await api.get_visits(
        profile_id=profile_id,                          # <PROFILE-ID>
        student_id=student_id,                          # <STUDENT-ID>
        contract_id=contract_id,                        # <CONTRACT-ID>
        from_date=date.today() - timedelta(days=7),     # начало промежутка времени
        to_date=date.today(),                           # конец
    )

    # Информация о покупках в школе, буфете, и т.д.
    day_balance_info = await api.get_day_balance_info(
        profile_id=profile_id,                          # <PROFILE-ID>
        contract_id=contract_id,                        # <CONTRACT-ID>
    )

    # Получить информацию о школе
    school_info = await api.get_school_info(
        profile_id=profile_id,                          # <PROFILE-ID>
        school_id=profile.children[0].school.id,        # <SCHOOL-ID>
        class_unit_id=profile.children[0].class_unit_id # <CLASS-UNIT-ID>
    )


async def main():
    await mobile_api()

if __name__ == "__main__":
    run(main())
```

</details>


<details>
    <summary><img width="40" height="40" src="https://img.icons8.com/fluency/64/python.png" alt="python"/> <h1>Sync</h1></summary>

``` python
from octodiary.apis import AsyncMobileAPI
from octodiary.types.enter_sms_code import EnterSmsCode
from octodiary.urls import Systems


def mobile_api():
    """
    API методы и запросы, которые делает приложение "Дневник МЭШ" для получения данных
    """

    api = AsyncMobileAPI(system=Systems.MES)

    # авторизовываемся, получаем токен и сохраняем его
    login = input("Логин: ")
    password = input("Пароль: ")

    sms_code: EnterSmsCode = api.login(username=login, password=password)
    code = input("SMS-Code: ")
    api.token = sms_code.async_enter_code(code)

    # получаем ID профиля
    profile_id = (api.get_users_profiles_info())[0].id

    # Получаем инфо о профиле и сохраняем некоторые важные данные, которые будут нужны
    profile = api.get_family_profile(profile_id=profile_id)
    mes_role = profile.profile.type                      # тип пользователя
    person_id = profile.children[0].contingent_guid      # person-id ученика
    student_id = profile.children[0].id                  # <STUDENT-ID>
    contract_id = profile.children[0].contract_id        # <CONTRACT-ID>

    # получить сохраненные настройки приложения пользователя (тема и т.д.)
    settings = api.get_user_settings_app(profile_id=profile_id)

    # редактировать настройки приложения у пользователя
    settings.theme.is_automatic = not settings.theme.is_automatic
    api.edit_user_settings_app(profile_id=profile_id, settings=settings)

    # получить расписание событий
    from datetime import date, timedelta

    events = api.get_events( # получить расписание событий на 7 дней вперед
        person_id=person_id,                            # person-id ученика (contingent_guid)
        mes_role=mes_role,                              # роль пользователя (student, parent)
        begin_date=date.today(),                        # начало промежутка времени
        end_date=date.today() + timedelta(days=7),      # конец
    )

    # получить краткую информацию о домашних заданиях на 7 дней вперед
    homeworks_short = api.get_homeworks_short(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id,                          # <PROFILE-ID>
        from_date=date.today(),                         # начало промежутка времени
        to_date=date.today() + timedelta(days=7),       # конец
    )

    # получить информацию об оценках за последние 7 дней
    marks = api.get_marks(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id,                          # <PROFILE-ID>
        from_date=date.today() - timedelta(days=7),     # начало промежутка времени
        to_date=date.today(),                           # конец
    )

    # Получить информацию о днях в периоде времени:
    #  - какой учебный модуль идет на момент опеределенного дня
    #  - что это за день: каникулы, выходной, учебный день
    periods_schedules = api.get_periods_schedules( # информация по дням на 30 дней вперед
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id,                          # <PROFILE-ID>
        from_date=date.today(),                         # начало промежутка времени
        to_date=date.today() + timedelta(days=30),      # конец
    )

    # Получить список предметов
    subjects = api.get_subjects(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id                           # <PROFILE-ID>
    )

    # получить программу обучения на текущий учебный год
    parallel_curriculum = api.get_programs_parallel_curriculum(
        id=profile.children[0].parallel_curriculum_id,  # <PARALLEL-CURRICULUM-ID>
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id                           # <PROFILE-ID>
    )

    # Получить подробную информацию о профиле
    person_data = api.get_person_data(
        person_id=person_id,                            # person-id ученика (contingent_guid)
        profile_id=profile_id                           # <PROFILE-ID>
    )

    # получить уведомления ученика
    notifications = api.get_notifications(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id                           # <PROFILE-ID>
    )

    # Получить инфо о предмете: оценки и т.д.
    subject_marks_info = api.get_subject_marks_for_subject(
        student_id=student_id,                          # <STUDENT-ID>
        profile_id=profile_id,                          # <PROFILE-ID>
        subject_name="<ИМЯ-ПРЕДМЕТА>"                   # Например: "Алгебра"
    )

    # Получим подробную информацию об уроке или занятии (в данном случае о первом занятии в списке)
    lesson_info = api.get_lesson_schedule_item(
        profile_id=profile_id,                          # <PROFILE-ID>
        lesson_id=events.response[0].id,                # <LESSON-ID>
        student_id=student_id,                          # <STUDENT-ID>
        type=events.response[0].source                  # <TYPE>
    )


    # Получаем инфо о балансе
    balance_info = api.get_status(
        profile_id=profile_id,                          # <PROFILE-ID>
        contract_id=contract_id                         # <CONTRACT-ID>
    )
    print("Баланс:", balance_info.students[0].balance / 100, "₽")

    # Информация об оценках и средних баллам по предметам
    subject_marks = api.get_subject_marks_short(
        profile_id=profile_id,                          # <PROFILE-ID>
        student_id=student_id                           # <STUDENT-ID>
    )

    # Информация о посещениях (время входа, выхода, и т.д.) за последние 7 дней
    visits = api.get_visits(
        profile_id=profile_id,                          # <PROFILE-ID>
        student_id=student_id,                          # <STUDENT-ID>
        contract_id=contract_id,                        # <CONTRACT-ID>
        from_date=date.today() - timedelta(days=7),     # начало промежутка времени
        to_date=date.today(),                           # конец
    )

    # Информация о покупках в школе, буфете, и т.д.
    day_balance_info = api.get_day_balance_info(
        profile_id=profile_id,                          # <PROFILE-ID>
        contract_id=contract_id,                        # <CONTRACT-ID>
    )

    # Получить информацию о школе
    school_info = api.get_school_info(
        profile_id=profile_id,                          # <PROFILE-ID>
        school_id=profile.children[0].school.id,        # <SCHOOL-ID>
        class_unit_id=profile.children[0].class_unit_id # <CLASS-UNIT-ID>
    )


def main():
    mobile_api()

if __name__ == "__main__":
    main()
```

</details>
