#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

import hashlib
from datetime import date as Date
from datetime import datetime
from typing import Optional, TypeVar, Union

import requests
from fake_useragent.fake import UserAgent

from octodiary.exceptions import APIError
from octodiary.types import Type

_type = TypeVar("_type")


class SyncBaseApi:
    """
    Basic class for sync use API.
    """

    @property
    def user_agent(self) -> str:
        return UserAgent().random

    def headers(self, require_token: bool = True, custom_headers: Optional[dict] = None):
        if custom_headers:
            for key, value in custom_headers.copy().items():
                if value is None:
                    del custom_headers[key]
                elif not isinstance(value, str):
                    custom_headers[key] = str(value)

        HEADERS = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        if not self.token and require_token:
            msg = "Token is required!"
            raise ValueError(msg)
        elif require_token:
            HEADERS.update({
                "Authorization": f"Bearer {self.token}",
                "Auth-Token": self.token,
                "Cookie": "aupdtoken=" + self.token + "; aupd_token=" + self.token + (
                    f"; {custom_headers.pop('Cookie')}"
                    if custom_headers
                       and "Cookie" in custom_headers
                    else ""
                )
            })

        HEADERS.update(custom_headers or {})
        return HEADERS


    @staticmethod
    def _resolve_proof_of_work(proof_of_work: str) -> str:
        """
        Resolves and returns a hashcash stamp.

        Args:
            nbits: Number of leading zero bits the stamp must have.
            hcheader: Pre-baked hashcash header sans counter field eg,
                1:15:231012184839:63685480-9484-45cd-87b4-19a87bded3f6::VO5fn4nNM0zHZfSoJ1XBaA==:

        Returns:
            Hashcash stamp string.
        """
        def check_hash_for_cash(digest_bytes, zero_bits):
            bit_counter = 0

            for hash_byte in digest_bytes:
                if bit_counter >= zero_bits:
                    return True
                bits_remain = zero_bits - bit_counter
                if bits_remain >= 8:
                    if hash_byte == 0x00:
                        bit_counter += 8
                        continue
                    else:
                        return False
                else:
                    for bit in range(bits_remain - 1, -1, -1):
                        bit_counter += 1
                        mask = 0x80 >> bit
                        if hash_byte & mask:
                            return False

            return True

        counter = 0
        header_bytes = proof_of_work.encode()

        while True:
            counter_string = hex(counter)[2:]

            if check_hash_for_cash(
                hashlib.sha1(
                    header_bytes + counter_string.encode()
                ).digest(), 15
            ):
                break
            counter += 1

        return proof_of_work + counter_string


    @staticmethod
    def init_params(url: str, params: dict) -> str:
        boolean = {True: "true", False: "false"}
        return (
                f"{url}?" + "&".join(
            [
                f"{X}={Y}" for X, Y in {
                    X: Y
                    if isinstance(Y, (str, float, int))
                    else boolean[Y]
                    if isinstance(Y, bool)
                    else "null"
                    if Y is None
                    else str(Y)
                    for X, Y in params.items()
                }.items()
            ]
        )
        ) if params else url

    def __init__(
            self,
            token: Optional[str] = None,
    ) -> None:
        self.token = token
        self.session = requests.Session()

    @staticmethod
    def datetime_to_string(dt: Optional[Union[datetime, Date]] = None) -> str:
        """Сконвертировать ``datetime.datetime`` объект в строку(``str``) для использования в URL (METHOD)\n~~~"""
        if not dt:
            dt = datetime.now()
        return (
            f"{dt.year}-{dt.month:02}-{dt.day:02}T{dt.hour:02}:{dt.minute:02}:{dt.second:02}"
            if isinstance(dt, datetime)
            else f"{dt.year}-{dt.month:02}-{dt.day:02}"
        )

    @staticmethod
    def date_to_string(date: Optional[Union[datetime, Date]] = None) -> str:
        """Сконвертировать ``datetime.date`` объект в строку(``str``) для использования в URL (METHOD)\n~~~"""
        if not date:
            date = Date.today()
        return f"{date.year}-{date.month:02}-{date.day:02}"

    @staticmethod
    def parse_list_models(model: _type, response: str) -> list[_type]:
        class ListModels(Type):
            listik: list[model]

        return ListModels.model_validate_json('{"listik": ' + response.replace("'", '"') + "}").listik

    @staticmethod
    def _check_response(response: requests.Response):
        if response.status_code > 400:
            if response.headers.get("Content-Type") == "text/html":
                error_html = response.text
                if "502" in error_html:
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_type="HTMLError",
                        description=error_html
                    )

                error_text = " ".join(
                    word
                    for word in error_html.split('<div class="error__description">')[-1]
                                .split("<p>")[1]
                                .strip()[:-4]
                                .split()
                )
                raise APIError(
                    url=str(response.url),
                    status_code=response.status_code,
                    error_type="HTMLError",
                    description=error_text
                )

            try:
                json_response = response.json()

                if isinstance(json_response, dict):
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status_code,
                        error_type=json_response.get("type", "?"),
                        description=json_response.get("description", None),
                        details=json_response.get("details", None),
                    )
            except requests.exceptions.JSONDecodeError as e:
                raise APIError(
                    url=str(response.url),
                    status_code=response.status_code,
                    error_type="JSONError",
                    description=response.text,
                    details=None
                ) from e

    def get(
            self,
            url: str,
            custom_headers: Optional[dict] = None,
            model: Optional[type[Type]] = None,
            is_list: bool = False,
            return_json: bool = False,
            return_raw_text: bool = False,
            required_token: bool = True,
            return_raw_response: bool = False,
            **kwargs
    ):
        params = kwargs.pop("params", {})
        response = self.session.get(url=self.init_params(url, params),
                                    headers=self.headers(required_token, custom_headers), **kwargs)
        self._check_response(response)
        RAW_TEXT = response.text

        return (
            response
            if return_raw_response
            else response.json()
            if return_json
            else RAW_TEXT
            if return_raw_text
            else self.parse_list_models(model, RAW_TEXT)
            if is_list
            else model.model_validate_json(RAW_TEXT)
            if model
            else RAW_TEXT
        )

    def post(
            self,
            url: str,
            custom_headers: Optional[dict] = None,
            json=None,
            data=None,
            model: Optional[type[Type]] = None,
            is_list: bool = False,
            return_json: bool = False,
            return_raw_text: bool = False,
            required_token: bool = True,
            return_raw_response: bool = False,
            **kwargs
    ):
        params = kwargs.pop("params", {})
        response = self.session.post(url=self.init_params(url, params),
                                     headers=self.headers(required_token, custom_headers), json=json, data=data,
                                     **kwargs)
        self._check_response(response)
        RAW_TEXT = response.text

        return (
            response
            if return_raw_response
            else response.json()
            if return_json
            else RAW_TEXT
            if return_raw_text
            else self.parse_list_models(model, RAW_TEXT)
            if is_list
            else model.model_validate_json(RAW_TEXT)
            if model
            else RAW_TEXT
        )

    def put(
            self,
            url: str,
            custom_headers: Optional[dict] = None,
            json=None,
            data=None,
            model: Optional[type[Type]] = None,
            is_list: bool = False,
            return_json: bool = False,
            return_raw_text: bool = False,
            required_token: bool = True,
            return_raw_response: bool = False,
            **kwargs
    ):
        params = kwargs.pop("params", {})
        response = self.session.put(url=self.init_params(url, params),
                                    headers=self.headers(required_token, custom_headers), json=json, data=data,
                                    **kwargs)
        self._check_response(response)
        RAW_TEXT = response.text

        return (
            response
            if return_raw_response
            else response.json()
            if return_json
            else RAW_TEXT
            if return_raw_text
            else self.parse_list_models(model, RAW_TEXT)
            if is_list
            else model.model_validate_json(RAW_TEXT)
            if model
            else RAW_TEXT
        )

    def delete(
            self,
            url: str,
            custom_headers: Optional[dict] = None,
            json=None,
            data=None,
            model: Optional[type[Type]] = None,
            is_list: bool = False,
            return_json: bool = False,
            return_raw_text: bool = False,
            required_token: bool = True,
            return_raw_response: bool = False,
            **kwargs
    ):
        params = kwargs.pop("params", {})
        response = self.session.delete(url=self.init_params(url, params),
                                       headers=self.headers(required_token, custom_headers), json=json, data=data,
                                       **kwargs)
        self._check_response(response)
        RAW_TEXT = response.text

        return (
            response
            if return_raw_response
            else response.json()
            if return_json
            else RAW_TEXT
            if return_raw_text
            else self.parse_list_models(model, RAW_TEXT)
            if is_list
            else model.model_validate_json(RAW_TEXT)
            if model
            else RAW_TEXT
        )
