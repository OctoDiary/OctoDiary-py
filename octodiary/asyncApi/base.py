#    ____       _        _____  _                  
#   / __ \     | |      |  __ \(_)                 
#  | |  | | ___| |_ ___ | |  | |_  __ _ _ __ _   _ 
#  | |  | |/ __| __/ _ \| |  | | |/ _` | '__| | | |
#  | |__| | (__| || (_) | |__| | | (_| | |  | |_| |
#   \____/ \___|\__\___/|_____/|_|\__,_|_|   \__, |
#                                             __/ |
#                                            |___/ 
# 
#                 © Copyright 2023
#        🔒 Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Optional

import aiohttp

from octodiary.exceptions import APIError
from octodiary.syncApi.base import SyncBaseApi, Type


class AsyncBaseApi(SyncBaseApi):
    """
    Basic class for async using API.
    """

    @staticmethod
    async def _check_response(response: aiohttp.ClientResponse):
        if response.status > 400:
            if response.content_type == "text/html":
                error_html = await response.text()
                if "502" in error_html:
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
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
                    status_code=response.status,
                    error_type="HTMLError",
                    description=error_text
                )
            
            try:
                json_response = await response.json()

                if isinstance(json_response, dict):
                    raise APIError(
                        url=str(response.url),
                        status_code=response.status,
                        error_type=json_response.get("type", "?"),
                        description=json_response.get("description", None),
                        details=json_response.get("details", None),
                    )
            except:
                raise APIError(
                    url=str(response.url),
                    status_code=response.status,
                    error_type="ServerError & JSONError",
                    description=(await response.text()),
                    details=None
                )
    
    async def get(
        self,
        url: str,
        custom_headers: Optional[dict] = None,
        model: Optional[Type] = None,
        is_list: bool = False,
        return_json: bool = False,
        return_raw_text: bool = False,
        required_token: bool = True,
        return_raw_response: bool = False,
        **kwargs
    ):
        params = kwargs.pop("params", {})
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.init_params(url, params),
                headers=self.headers(required_token, custom_headers),
                **kwargs
            ) as response:
                await self._check_response(response)
                RAW_TEXT = await response.text()
                
                return (
                    response
                    if return_raw_response
                    else await response.json()
                    if return_json
                    else RAW_TEXT
                    if return_raw_text
                    else self.parse_list_models(model, RAW_TEXT)
                    if is_list
                    else model.model_validate_json(RAW_TEXT)
                    if model
                    else RAW_TEXT
                )
    
    async def post(
        self,
        url: str,
        custom_headers: Optional[dict] = None,
        json = None,
        data = None,
        model: Optional[Type] = None,
        is_list: bool = False,
        return_json: bool = False,
        return_raw_text: bool = False,
        required_token: bool = True,
        return_raw_response: bool = False,
        **kwargs
    ):
        params = kwargs.pop("params", {})
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.init_params(url, params),
                headers=self.headers(required_token, custom_headers),
                json=json, data=data, **kwargs
            ) as response:
                await self._check_response(response)
                RAW_TEXT = await response.text()
                
                return (
                    response
                    if return_raw_response
                    else await response.json()
                    if return_json
                    else RAW_TEXT
                    if return_raw_text
                    else self.parse_list_models(model, RAW_TEXT)
                    if is_list
                    else model.model_validate_json(RAW_TEXT)
                    if model
                    else RAW_TEXT
                )

    async def put(
        self,
        url: str,
        custom_headers: Optional[dict] = None,
        json = None,
        data = None, 
        model: Optional[Type] = None,
        is_list: bool = False,
        return_json: bool = False,
        return_raw_text: bool = False,
        required_token: bool = True,
        return_raw_response: bool = False,
        **kwargs
    ):
        params = kwargs.pop("params", {})
        async with aiohttp.ClientSession() as session:
            async with session.put(
                url=self.init_params(url, params),
                headers=self.headers(required_token, custom_headers),
                json=json, data=data, **kwargs
            ) as response:
                await self._check_response(response)
                RAW_TEXT = await response.text()
                
                return (
                    response
                    if return_raw_response
                    else await response.json()
                    if return_json
                    else RAW_TEXT
                    if return_raw_text
                    else self.parse_list_models(model, RAW_TEXT)
                    if is_list
                    else model.model_validate_json(RAW_TEXT)
                    if model
                    else RAW_TEXT
                )
    
    async def delete(
        self,
        url: str,
        custom_headers: Optional[dict] = None,
        json = None,
        data = None,
        model: Optional[Type] = None,
        is_list: bool = False,
        return_json: bool = False,
        return_raw_text: bool = False, 
        required_token: bool = True,
        return_raw_response: bool = False,
        **kwargs
    ):
        params = kwargs.pop("params", {})
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url=self.init_params(url, params),
                headers=self.headers(required_token, custom_headers),
                json=json, data=data, **kwargs
            ) as response:
                await self._check_response(response)
                RAW_TEXT = await response.text()
                
                return (
                    response
                    if return_raw_response
                    else await response.json()
                    if return_json
                    else RAW_TEXT
                    if return_raw_text
                    else self.parse_list_models(model, RAW_TEXT)
                    if is_list
                    else model.model_validate_json(RAW_TEXT)
                    if model
                    else RAW_TEXT
                )
    