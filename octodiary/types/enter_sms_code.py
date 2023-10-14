#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any

from aiohttp.formdata import FormData

from octodiary.exceptions import APIError
from octodiary.types.model import Type
from octodiary.urls import MesURLs


class EnterSmsCode(Type):
    inquire: str = "enter_sms_code"
    contact: str
    ttl: int = 300
    remain_attempts: int = 3
    api_class: Any

    async def async_enter_code(self, code: str) -> bool:
        resp = await self.api_class._login_info["session"].post(
            MesURLs.LOGIN.BIND_SMS_CODE,
            data=FormData({"sms-code": code}),
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        if "<title>Доверять этому браузеру?</title>" in await resp.text():
            resp = await self.api_class._login_info["session"].post(
                MesURLs.LOGIN.TRUST,
                data=FormData({"trust": "true"}),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            return await self.api_class._handle_login_response(resp, {})


        try:
            return await self.api_class._handle_login_response(resp, await resp.json())
        except Exception as e:
            if isinstance(e, APIError):
                raise e

            raise APIError(
                url=str(resp.url),
                status_code=resp.status,
                error_type="?",
                details=resp
            ) from e

    def enter_code(self, code: str) -> bool:
        resp = self.api_class.session.post(
            MesURLs.LOGIN.BIND_SMS_CODE,
            data={"sms-code": code},
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        if "<title>Доверять этому браузеру?</title>" in resp.text():
            resp = self.api_class.session.get(
                MesURLs.LOGIN.TRUST,
                data={"trust": "true"},
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            return self.api_class._handle_login_response(resp, {})

        try:
            return self.api_class._handle_login_response(resp, resp.json())
        except Exception as e:
            raise APIError(
                url=str(resp.url),
                status_code=resp.status_code,
                error_type="?",
                details=resp
            ) from e
