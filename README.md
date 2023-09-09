<p align="center">
    <a href="https://github.com/OctoDiary">
        <img src="https://avatars.githubusercontent.com/u/90847608?s=200&v=4" alt="OctoDiary" width="128">
    </a>
    <br>
    <a href="https://github.com/OctoDiary"><b>OctoDiary</b></a>
    <br>
    <a href="https://t.me/OctoDiary">Telegram-Канал</a>
</p>

# OctoDiary-py
> Неофициальная Python библиотека для использования API: МЭШ / Моя Школа.

<br>

# <img width="30" height="30" src="https://img.icons8.com/external-sbts2018-outline-color-sbts2018/58/external-install-basic-ui-elements-2.3-sbts2018-outline-color-sbts2018.png" alt="external-install-basic-ui-elements-2.3-sbts2018-outline-color-sbts2018"/> Установка

### Установка через GitHub:
``` bash
pip3 install https://github.com/OctoDiary/OctoDiary-py/archive/main.zip --upgrade
```

### Стабильная версия от PyPi:
``` bash
pip3 install octodiary
```
> Для Windows: <s>pip3</s> > <b>pip</b>

<br>

# <img width="40" height="40" src="https://img.icons8.com/fluency/48/python.png" alt="python"/> Использование

<br>

# <img width="45" height="45" src="https://media.cdnandroid.com/item_images/1390670/imagen-moya-shkola-dnevnik-0ori.jpg" alt="myschool"/> Моя Школа

### Async
``` python
from octodiary.asyncApi.myschool import WebAsyncApi
from asyncio import run

api = WebAsyncApi()

async def login_gosuslugi():
    # если у вас выключен вход с подтверждением (MFA):
    TOKEN = await api.esia_login("<LOGIN>", "<PASSWORD>")

    # если у вас включен вход с подтверждением (MFA):
    await api.esia_login("<LOGIN>", "<PASSWORD>", True)
    code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
    TOKEN = await api.esia_enter_MFA(code=code_mfa)
    
    return TOKEN

async def main():
    api.token = await login_gosuslugi() # получения токена по логину и паролю от госуслуг
    
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
    # содержит подробную  информацию, включая личные данные
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

run(main())
```

### Sync
``` python
from octodiary.syncApi.myschool import WebSyncApi

api = WebSyncApi()

def login_gosuslugi():
    # если у вас выключен вход с подтверждением (MFA):
    TOKEN = api.esia_login("<LOGIN>", "<PASSWORD>")

    # если у вас включен вход с подтверждением (MFA):
    api.esia_login("<LOGIN>", "<PASSWORD>", True)
    code_mfa = int(input("MFA Code: ").strip()) # запрашиваем у пользователя код (SMS/TOTP)
    TOKEN = api.esia_enter_MFA(code=code_mfa)
    
    return TOKEN

api.token = login_gosuslugi() # получения токена по логину и паролю от госуслуг


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
# содержит подробную  информацию, включая личные данные
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
```

<br>

# <img width="45" height="45" src="https://is3-ssl.mzstatic.com/image/thumb/Purple114/v4/57/39/7b/57397bea-0eb8-d0d3-ad57-c170359343af/source/200x200bb.jpg" alt="mesh"/> МЭШ

> Скоро...
