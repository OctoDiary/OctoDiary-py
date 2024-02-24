#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from contextlib import suppress
from typing import Any

from aiohttp.formdata import FormData

from octodiary.exceptions import APIError
from octodiary.types.model import Type
from octodiary.urls import BaseURL, Systems, URLTypes


class EnterSmsCode(Type):
    inquire: str = "enter_sms_code"
    contact: str
    ttl: int = 300
    remain_attempts: int = 3
    api_class: Any

    async def async_enter_code(self, code: str) -> bool:
        resp = await self.api_class._login_info["session"].post(
            BaseURL(URLTypes.AUTH, system=Systems.MES) + "/sps/login/methods/headless/sms/bind",
            data=FormData({"sms-code": code}), allow_redirects=False,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        if "<title>Доверять этому браузеру?</title>" in await resp.text():
            resp = await self.api_class._login_info["session"].post(
                BaseURL(URLTypes.AUTH, system=Systems.MES) + "/sps/login/ur/askToTrust",
                data=FormData({"trust": "true"}),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }, allow_redirects=False
            )

            return await self.api_class._handle_login_response(resp, {
                "trust_code": resp.headers["Location"].split("?")[-1].split("=")[-1]
            })

        if (trust_code := resp.headers["Location"].split("?")[-1].split("=")[-1]):
            return await self.api_class._handle_login_response(resp, {
                "trust_code": trust_code
            })

        try:
            return await self.api_class._handle_login_response(resp, await resp.json())
        except Exception as e:
            if isinstance(e, APIError):
                raise e

            raise APIError(
                url=str(resp.url),
                status_code=resp.status,
                error_types="?",
                details=resp
            ) from e

    def enter_code(self, code: str) -> bool:
        resp = self.api_class.session.post(
            BaseURL(URLTypes.AUTH, system=Systems.MES).url + "/sps/login/methods/headless/sms/bind",
            data={"sms-code": code},
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }, allow_redirects=False
        )
        if "<title>Доверять этому браузеру?</title>" in resp.text():
            resp = self.api_class.session.get(
                BaseURL(URLTypes.AUTH, system=Systems.MES) + "/sps/login/ur/askToTrust",
                data={"trust": "true"},
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }, allow_redirects=False
            )

            return self.api_class._handle_login_response(resp, {
                "trust_code": resp.headers["Location"].split("?")[-1].split("=")[-1]
            })

        if (trust_code := resp.headers["Location"].split("?")[-1].split("=")[-1]):
            return self.api_class._handle_login_response(resp, {
                "trust_code": trust_code
            })

        try:
            return self.api_class._handle_login_response(resp, resp.json())
        except Exception as e:
            raise APIError(
                url=str(resp.url),
                status_code=resp.status_code,
                error_types="?",
                details=resp
            ) from e
