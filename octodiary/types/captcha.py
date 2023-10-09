#                 © Copyright 2023
#          Licensed under the MIT License
#        https://opensource.org/licenses/MIT
#           https://github.com/OctoDiary

from typing import Any

from octodiary.types.model import Type


class Captcha(Type):
    gosuslugi_type: str
    guid: str
    image_bytes: bytes | None = None
    question: str | None = None
    api: Any
    api_session: Any

    _type: str = None
    _session: str = None

    __ANSWER_URL__ = "https://esia.gosuslugi.ru/aas/oauth2/api/anomaly/question/answer"
    __QUESTION_URL__ = "https://esia.gosuslugi.ru/anomaly-resolver/api/reaction/question?guid={guid}"
    __CAPTCHA_TYPE_URL__ = "https://esia.gosuslugi.ru/captcha/api/public/v2/type"
    __CAPTCHA_IMAGE_URL__ = "https://esia.gosuslugi.ru/captcha/api/public/v2/image"
    __CAPTCHA_ENTER_URL__ = "https://esia.gosuslugi.ru/captcha/api/public/v2/verify"
    __CAPTCHA_RENEW_URL__ = "https://esia.gosuslugi.ru/captcha/api/public/v2/renew"
    __CAPTCHA_VOICE_URL__ = "https://esia.gosuslugi.ru/captcha-audio-service/api/public/v2/voice"
    __CAPTCHA_VERIFY_URL__ = "https://esia.gosuslugi.ru/aas/oauth2/api/anomaly/captcha/verify?guid={guid}&verify_token={verify_token}"


    async def async_asnwer_captcha(self, answer: str):
        """
        Asynchronously answers a captcha.

        Args:
            answer (str): The answer to the captcha.

        Returns:
            The response from the server after answering the captcha.
        """
        answer_captcha = await self.api_session.post(
            url=self.__ANSWER_URL__,
            json={
                "answer": answer,
                "guid": self.guid
            }
        )
        response_json = await answer_captcha.json()
        return await self.api.handle_action(
            response=answer_captcha,
            action=response_json.get("action", None),
            failed=response_json.get("failed", None)
        )

    def answer_captcha(self, answer: str):
        """
        Answer a captcha.

        Args:
            answer (str): The answer to the captcha.

        Returns:
            The result of the API action.
        """
        answer_captcha = self.api.__login_request(
            self.api.session.post(
                url=self.__ANSWER_URL__,
                json={
                    "answer": answer,
                    "guid": self.guid
                },
                cookies=self.api.__cookies
            )
        )
        response_json = answer_captcha.json()
        return self.api.handle_action(
            response=answer_captcha,
            action=response_json.get("action", None),
            failed=response_json.get("failed", None)
        )

    async def async_renew_image_captcha(self) -> "Captcha":
        """
        Asynchronously renews the image captcha.

        Returns:
            Captcha: The renewed captcha object.
        """
        renew = await self.api_session.get(
            url=self.__CAPTCHA_RENEW_URL__,
            headers={
                "captchasession": self._session
            }
        )
        response_json = await renew.json()
        self._session = response_json.get("captchaSession", None)
        self._type = response_json.get("captchaType", "esiacaptcha")
        self.image_bytes = await self.async_get_captcha_image()
        return self

    def renew_image_captcha(self) -> "Captcha":
        """
        Renews the image captcha.

        :return: A `Captcha` object representing the renewed captcha.
        """
        renew = self.api.__login_request(
            self.api.session.get(
                url=self.__CAPTCHA_RENEW_URL__,
                headers={
                    "captchasession": self._session
                },
                cookies=self.api.__cookies
            )
        )
        response_json = renew.json()
        self._session = response_json.get("captchaSession", None)
        self._type = response_json.get("captchaType", "esiacaptcha")
        self.image_bytes = self.get_captcha_image()
        return self

    async def async_get_voice(self) -> bytes:
        """
        Asynchronously retrieves the voice data for the captcha.

        :return: The voice data as bytes.
        """
        return await (
            await self.api_session.get(
                url=self.__CAPTCHA_VOICE_URL__,
                headers={
                    "captchasession": self._session
                }
            )
        ).content.read()

    def get_voice(self) -> bytes:
        """
        Retrieves the voice captcha from the API.

        :return: The voice captcha as bytes.
        :rtype: bytes
        """
        return self.api.__login_request(
            self.api.session.get(
                url=self.__CAPTCHA_VOICE_URL__,
                headers={
                    "captchasession": self._session
                },
                cookies=self.api.__cookies
            )
        ).content

    async def async_get_captcha_image(self) -> bytes:
        """
        Retrieves the captcha image asynchronously.

        Returns:
            bytes: The captcha image content as bytes.
        """
        if not self._type:
            captcha_type_response = await self.api_session.get(
                url=self.__CAPTCHA_TYPE_URL__,
            )
            captcha_type_response_json = await captcha_type_response.json()
            self._type = captcha_type_response_json.get("captchaType", "esiacaptcha")
            self._session = captcha_type_response_json.get("captchaSession", None)

        return await (await self.api_session.get(
            url=self.__CAPTCHA_IMAGE_URL__,
            headers={
                "captchasession": self._session
            }
        )).content.read()

    def get_captcha_image(self) -> bytes:
        """
        Retrieves the captcha image from the server.

        :return: The captcha image as bytes.
        """
        if not self._type:
            captcha_type_response = self.api.__login_request(
                self.api.session.get(
                    url=self.__CAPTCHA_TYPE_URL__,
                    cookies=self.api.__cookies
                )
            )
            captcha_type_response_json = captcha_type_response.json()
            self._type = captcha_type_response_json.get("captchaType", "esiacaptcha")
            self._session = captcha_type_response_json.get("captchaSession", None)

        return self.api.__login_request(
            self.api.session.get(
                url=self.__CAPTCHA_IMAGE_URL__,
                cookies=self.api.__cookies,
                headers={
                    "captchasession": self._session
                }
            )
        ).content

    async def async_verify_captcha(self, answer: str):
        """
        Verify the captcha by sending the answer to the server.

        Args:
            answer (str): The answer to the captcha challenge.

        Returns:
            Coroutine: A coroutine that handles the action based on the server response.
        """
        step_one = await self.api_session.post(
            url=self.__CAPTCHA_ENTER_URL__,
            json={
                "answer": answer,
                "captchaType": self._type,
            },
            headers={
                "captchaSession": self._session
            }
        )
        json = await step_one.json()

        verify = await self.api_session.post(
            url=self.__CAPTCHA_VERIFY_URL__.format(guid=self.guid, verify_token=json.get("verify_token")),
            json={
                "verify_token": json.get("verify_token"),
                "guid": self.guid
            }
        )
        verify_json = await verify.json()
        return await self.api.handle_action(
            response=verify,
            action=verify_json.get("action", None),
            failed=verify_json.get("failed", None)
        )

    def verify_captcha(self, answer: str):
        """
        Verify the captcha using the provided answer.

        Args:
            answer (str): The answer to the captcha.

        Returns:
            The result of the captcha verification.
        """
        step_one = self.api.__login_request(
            self.api_session.post(
                url=self.__CAPTCHA_ENTER_URL__,
                json={
                    "answer": answer,
                    "captchaType": self._type,
                },
                cookies=self.api.__cookies
            )
        )
        json = step_one.json()
        verify = self.api.__login_request(
            self.api_session.post(
                url=self.__CAPTCHA_VERIFY_URL__.format(guid=self.guid, verify_token=json.get("verify_token")),
                json={
                    "verify_token": json.get("verify_token"),
                    "guid": self.guid
                },
                cookies=self.api.__cookies
            )
        )
        verify_json = verify.json()
        return self.api.handle_action(
            response=verify,
            action=None,
            failed=verify_json.get("failed", None)
        )

    async def async_get_question(self) -> str:
        """
        Asynchronously retrieves a question from the API.

        Returns:
            str: The text of the question, or None if no question is found.
        """
        return (
            await (
                await self.api_session.get(
                    url=self.__QUESTION_URL__.format(guid=self.guid)
                )
            ).json()
        ).get("question_text", None)

    def get_question(self) -> str:
        """
        Retrieves a question from the API.

        :return: A string representing the question text, or None if no question is available.
        """
        return (
            self.api.__login_request(
                self.api_session.get(
                    url=self.__QUESTION_URL__.format(guid=self.guid),
                    cookies=self.api.__cookies
                )
            ).json().get("question_text", None)
        )


async def async_generate_captcha_class(api: Any, response_json: dict, api_session: Any) -> Captcha:
    captcha = Captcha(
        gosuslugi_type=response_json.get("reaction_details", {}).get("type", None),
        guid=response_json.get("reaction_details", {}).get("guid", None),
        api=api, api_session=api_session
    )
    match captcha.gosuslugi_type:
        case "О.ЗД1":
            captcha.image_bytes = await captcha.async_get_captcha_image()
        case "О.ЗИ1":
            captcha.question = await captcha.async_get_question()
    return captcha


def generate_captcha_class(api: Any, response_json: dict, api_session: Any) -> Captcha:
    captcha = Captcha(
        gosuslugi_type=response_json.get("reaction_details", {}).get("type", None),
        guid=response_json.get("reaction_details", {}).get("guid", None),
        api=api, api_session=api_session
    )
    match captcha.gosuslugi_type:
        case "О.ЗД1":
            captcha.image_bytes = captcha.get_captcha_image()
        case "О.ЗИ1":
            captcha.question = captcha.get_question()
    return captcha
